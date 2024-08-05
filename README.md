# Endometriosis_Question_Answering
## Overview:
This project implements a document query system using FastAPI, a modern web framework for building APIs with Python 3.7+ based on standard Python-type hints. The system leverages a pre-trained model from the Sentence Transformers library to provide semantic search capabilities. Users can query documents, and the system returns the most relevant answers based on the query.

## Key Components
1.Libraries and Environment Setup

* os: For setting environment variables.
* nest_asyncio: To apply asyncio event loops for Jupyter notebooks.
* fastapi: To create the web application.
* pydantic: For data validation.
* Jinja2Templates: For rendering HTML templates.
* sentence_transformers: For semantic search and sentence embeddings.
* torch: For tensor operations and model deployment.
* docx: For reading .docx files.
* re: For regular expression operations.
* asyncio: For asynchronous programming.

2. Remove_timestamps(text): Removes timestamps from text using regular expressions.
get_documents(doc_paths): Reads .docx files, extracts question-answer pairs, and returns a list of documents.
Document Processing


3. Loads the Sentence Transformer model (msmarco-bert-base-dot-v5).
Encodes the documents into embeddings using the model and stores these embeddings for future queries.
Runs the model loading and encoding asynchronously to improve performance.
