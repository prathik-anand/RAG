from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from src.services.vector_store_manager import VectorStoreManager
from src.config import Config
from src.constants import LLM_MODEL_NAME, LLM_TEMPERATURE, VECTOR_STORE_SIMILARITY_K, RAG_PROMPT_TEMPLATE

class RAGService:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=LLM_TEMPERATURE,
            model_name=LLM_MODEL_NAME,
            api_key=Config.GROQ_API_KEY
        )
        self.vector_store = VectorStoreManager().get_vector_store()

    def query(self, question):
        relevant_docs = self.vector_store.similarity_search(question, k=VECTOR_STORE_SIMILARITY_K)
        context = "\n".join([doc.page_content for doc in relevant_docs])
        prompt = PromptTemplate(template=RAG_PROMPT_TEMPLATE, input_variables=["context", "question"])
        final_prompt = prompt.format(context=context, question=question)
        response = self.llm.invoke([HumanMessage(content=final_prompt)])
        return response.content
