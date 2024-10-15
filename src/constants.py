# LLM Model Configuration
LLM_MODEL_NAME = "llama3-8b-8192"
LLM_TEMPERATURE = 0.8

# Vector Store Configuration
VECTOR_STORE_SIMILARITY_K = 3

# Prompt Template
RAG_PROMPT_TEMPLATE = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {question}
Answer:"""
