# RAG (Retrieval-Augmented Generation) Application

This is a Flask-based RAG application that uses Chroma DB for vector storage and Groq for language model processing.

## Features

- Processes and indexes PDF, DOCX, and TXT files
- Uses OpenAI embeddings for document vectorization
- Implements a RAG pipeline for answering questions based on the indexed documents
- Provides a simple API endpoint for querying the system

## Efficient Use of Chroma DB

Our application leverages Chroma DB as a vector store for efficient management and querying of document embeddings. Here's how we optimize its usage:

1. **Smart Initialization**: The application checks for an existing vector store before creating a new one, avoiding unnecessary reprocessing of documents.

2. **Persistence**: We use Chroma's persistence capabilities, storing the vector database in a dedicated directory. This allows the knowledge base to be maintained across multiple runs of the application.

3. **Load if Exists, Create if Not**: On startup, the application first attempts to load an existing vector store. If none exists, only then does it create a new one by processing the documents.

4. **Efficient Document Processing**: When creating a new vector store, documents are processed once, split into chunks, and embedded. This chunking strategy allows for more precise similarity searches.

5. **One-Time Embedding Creation**: Document embeddings are created only once and then persisted, significantly reducing startup time for subsequent runs.

6. **Optimized Similarity Search**: We leverage Chroma DB's built-in similarity search functionality for efficient querying of relevant document chunks.

7. **Scalability**: This approach scales well with increasing numbers of documents, as new documents can be added to the existing vector store without reprocessing previously embedded documents.

8. **Memory Efficiency**: By using persistent storage, the application can handle larger document collections than what might fit in memory.

9. **Consistency**: The persistence of the vector store ensures consistency in search results across application restarts.

10. **Flexibility for Updates**: While the current implementation focuses on initial creation and subsequent loading, the structure allows for future enhancements such as incremental updates to the vector store.

This implementation achieves a balance between performance, efficiency, and scalability, providing fast query responses and maintaining a persistent, updateable knowledge base for enhanced question-answering capabilities.


## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. Create a virtual environment and activate it:
   Windows:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
   Linux or MacOS:
   ```
   python3 -m venv .venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your environment variables by creating a `.env` file in the root directory with the following content:
   ```
   GROQ_API_KEY=your_groq_api_key
   OPENAI_API_KEY=your_openai_api_key
   DOCUMENTS_DIRECTORY=data
   VECTOR_STORE_PATH=vector_store
   ```

## Usage

1. Place your documents (PDF, DOCX, TXT) in the `data` directory.

2. Run the application:
   ```
   python main.py
   ```

3. The application will start and create/load the vector store as necessary.

4. To query the system, send a POST request to `http://localhost:5000/api/query` with a JSON body:
   ```json
   {
     "question": "Your question here"
   }
   ```

## Project Structure

- `main.py`: Entry point of the application
- `src/`: Contains the main application code
  - `app.py`: Flask application setup
  - `api/`: API endpoints
  - `services/`: Business logic
  - `repositories/`: Data access layer
  - `utils/`: Utility functions
  - `config.py`: Configuration management
  - `constants.py`: Constant values used across the application
- `data/`: Directory for storing documents to be processed
- `vector_store/`: Directory where the Chroma vector store is persisted

