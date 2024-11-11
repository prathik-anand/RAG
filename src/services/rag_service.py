from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from src.services.vector_store_manager import VectorStoreManager
from src.config import Config
from src.constants import LLM_MODEL_NAME, LLM_TEMPERATURE, VECTOR_STORE_SIMILARITY_K, RAG_PROMPT_TEMPLATE
from src.repositories.chat_repository import ChatRepository
from src.utils.log_util import Logger
import asyncio
from langdetect import detect, DetectorFactory
#from googletrans import Translator
DetectorFactory.seed = 0

class RAGService:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=LLM_TEMPERATURE,
            model_name=LLM_MODEL_NAME,
            api_key=Config.GROQ_API_KEY
        )
        self.vector_store = VectorStoreManager.get_vector_store()
        self.chat_repo = ChatRepository()
        #self.translator = Translator() 
        #self.deep_translator = GoogleTranslator()

    def get_answer(self, user_id, query_input, ip_address, location, chat_id=None):
        try:
            # Detect the language of the query
            language = detect(query_input)
            Logger.log_info(f"Detected language: {language}")

            if chat_id:
                Logger.log_info(f"Get answer for query with Chat ID %s and user_id %s" % (chat_id, user_id))
                chat_metadata = self.chat_repo.get_chat_metadata(chat_id)
                if not chat_metadata:
                    Logger.log_error(f"Chat ID does not exist %s" % chat_id)
                    raise ValueError("Chat ID does not exist.")
                
                # Retrieve chat history
                chat_history = self.chat_repo.get_chat_history_by_chat_id_and_user_id(chat_metadata.chat_id, user_id)
                context = self.format_chat_history(chat_history)  # Format the chat history for the prompt

                # Combine context with the current query
                full_prompt = f"{context}\nUser: {query_input}\nAI:"
                response = self.query_vector_store(full_prompt, language)

                current_history_count = self.chat_repo.get_chat_history_count(chat_metadata.chat_id)
                sort_order = current_history_count + 1

                # Save chat history asynchronously
                asyncio.run(self.save_chat_history(user_id, query_input, response, chat_metadata.chat_id, sort_order, ip_address, location))
                Logger.log_info(f"Chat history will be saved for chat_id: {chat_metadata.chat_id}, user_id: {user_id}")
                return chat_metadata.title, response
            else:
                # If chat_id is not provided, create a new chat metadata
                title = self.generate_title(query_input)  # Generate a title for the new chat
                chat_metadata = self.chat_repo.create_chat_metadata(user_id, title)

                # No previous context, just query the vector store
                response = self.query_vector_store(query_input, language)

                # Save chat history asynchronously
                asyncio.run(self.save_chat_history(user_id, query_input, response, chat_metadata.chat_id, 1, ip_address, location))

                return title, response
        except ValueError as ve:
            Logger.log_warning(f"ValueError: {str(ve)}")
            raise ve
        except Exception as e:
            Logger.log_error(f"An error occurred while processing the query: {str(e)}", exc_info=True)
            raise RuntimeError("An error occurred while processing the query: " + str(e))

    def query_vector_store(self, question, language):
        try:
            relevant_docs = self.vector_store.similarity_search(question, k=VECTOR_STORE_SIMILARITY_K)
            context = "\n".join([doc.page_content for doc in relevant_docs])
            
            #translated_context = self.translate_text(context, language)
            
            prompt = PromptTemplate(template=RAG_PROMPT_TEMPLATE, input_variables=["context", "question"])
            final_prompt = prompt.format(context=context, question=question) 
            response = self.llm.invoke([HumanMessage(content=final_prompt)])
            Logger.info("Successfully queried the vector store.")
            return response.content
        except Exception as e:
            Logger.error(f"Error querying the vector store: {str(e)}", exc_info=True)
            raise RuntimeError("Error querying the vector store: " + str(e))

    async def save_chat_history(self, user_id, query_input, response, chat_id, sort_order, ip_address, location):
        try:
            if chat_id:
                self.chat_repo.add_chat_history(chat_id, user_id, query_input, response, sort_order, ip_address, location)
                Logger.log_info(f"Chat history saved for chat_id: {chat_id}, user_id: {user_id}")
            else:
                Logger.log_warning("No chat_id provided for saving chat history.")
        except Exception as e:
            Logger.log_error(f"Error saving chat history: {str(e)}", exc_info=True)

    def generate_title(self, query_input):
        try:
            prompt = f"Generate a meaningful title for a chat based on the following query: '{query_input}', I don't need options, it should be only one, I don't need any suggestion, top result is final"
            response = self.llm.invoke([HumanMessage(content=prompt)])
            title = response.content.strip()
            Logger.info("Title generated successfully.")
            return title
        except Exception as e:
            Logger.error(f"Error generating title: {str(e)}", exc_info=True)
            raise RuntimeError("Error generating title: " + str(e))

    def format_chat_history(self, chat_history):
        """Format the chat history for inclusion in the prompt."""
        formatted_history = []
        for entry in chat_history:
            formatted_history.append(f"User: {entry.request}\nAI: {entry.response}")
        return "\n".join(formatted_history)
    
    #def translate_text(self, text, target_language):
        #translator = GoogleTranslator(target=target_language)
        #translation = translator.translate(text)
        #return translation