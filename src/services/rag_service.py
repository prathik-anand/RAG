from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from src.services.vector_store_manager import VectorStoreManager
from src.config import Config
from src.constants import LLM_MODEL_NAME, LLM_TEMPERATURE, VECTOR_STORE_SIMILARITY_K, RAG_PROMPT_TEMPLATE
from src.repositories.chat_repository import ChatRepository
import logging
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=LLM_TEMPERATURE,
            model_name=LLM_MODEL_NAME,
            api_key=Config.GROQ_API_KEY
        )
        self.vector_store = VectorStoreManager().get_vector_store()
        self.chat_repo = ChatRepository()

    async def get_answer(self, user_id, query_input, ip_address, location, chat_id=None):
        try:
            if chat_id:
                # If chat_id exists, retrieve the existing chat metadata
                chat_metadata = self.chat_repo.get_chat_metadata(chat_id)
                if not chat_metadata:
                    raise ValueError("Chat ID does not exist.")
                
                response = self.query_vector_Store(query_input)

                current_history_count = self.chat_repo.get_chat_history_count(chat_metadata.chat_id)
                sort_order = current_history_count + 1

                # Save chat history in the background
                asyncio.create_task(self.save_chat_history(user_id, query_input, response, chat_metadata.chat_id, sort_order, ip_address, location))

                return chat_metadata.title, response
            else:
                # If chat_id is not provided, create a new chat metadata
                title = self.generate_title(query_input)  # Generate a title for the new chat
                chat_metadata = self.chat_repo.create_chat_metadata(user_id, title)

                response = self.query_vector_Store(query_input)

                # Save chat history in the background
                asyncio.create_task(self.save_chat_history(user_id, query_input, response, chat_metadata.chat_id, 1, ip_address, location))

                return title, response
        except ValueError as ve:
            logger.warning(f"ValueError: {str(ve)}")
            raise ve
        except Exception as e:
            logger.error(f"An error occurred while processing the query: {str(e)}", exc_info=True)
            raise RuntimeError("An error occurred while processing the query: " + str(e))

    def query_vector_Store(self, question):
        try:
            relevant_docs = self.vector_store.similarity_search(question, k=VECTOR_STORE_SIMILARITY_K)
            context = "\n".join([doc.page_content for doc in relevant_docs])
            prompt = PromptTemplate(template=RAG_PROMPT_TEMPLATE, input_variables=["context", "question"])
            final_prompt = prompt.format(context=context, question=question)
            response = self.llm.invoke([HumanMessage(content=final_prompt)])
            logger.info("Successfully queried the vector store.")
            return response.content
        except Exception as e:
            logger.error(f"Error querying the vector store: {str(e)}", exc_info=True)
            raise RuntimeError("Error querying the vector store: " + str(e))

    async def save_chat_history(self, user_id, query_input, response, chat_id, sort_order, ip_address, location):
        try:
            if chat_id:
                self.chat_repo.add_chat_history(chat_id, user_id, query_input, response, sort_order, ip_address, location)
                logger.info(f"Chat history saved for chat_id: {chat_id}, user_id: {user_id}")
            else:
                logger.warning("No chat_id provided for saving chat history.")
        except Exception as e:
            logger.error(f"Error saving chat history: {str(e)}", exc_info=True)

    def generate_title(self, query_input):
        try:
            prompt = f"Generate a meaningful title for a chat based on the following query: '{query_input}', I don't need options, it should be only one, I don't need any suggestion, top result is final"
            response = self.llm.invoke([HumanMessage(content=prompt)])
            title = response.content.strip()
            logger.info("Title generated successfully.")
            return title
        except Exception as e:
            logger.error(f"Error generating title: {str(e)}", exc_info=True)
            raise RuntimeError("Error generating title: " + str(e))
