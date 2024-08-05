# Endometriosis_Question_Answering
Overview
This project implements a document query system using FastAPI, a modern web framework for building APIs with Python 3.7+ based on standard Python-type hints. The system leverages a pre-trained model from the Sentence Transformers library to provide semantic search capabilities. Users can query documents, and the system returns the most relevant answers based on the query.

Key Components
Libraries and Environment Setup

os: For setting environment variables.
nest_asyncio: To apply asyncio event loops for Jupyter notebooks.
fastapi: To create the web application.
pydantic: For data validation.
Jinja2Templates: For rendering HTML templates.
sentence_transformers: For semantic search and sentence embeddings.
torch: For tensor operations and model deployment.
glob: For file path management.
docx: For reading .docx files.
re: For regular expression operations.
asyncio: For asynchronous programming.
Environment Configuration

Disables UVLoop extensions to ensure compatibility with the nest_asyncio library.
Applies nest_asyncio to enable nested event loops.
FastAPI App Initialization

Creates a FastAPI application instance.
Sets up Jinja2 templates directory.
Data Model

Defines a Pydantic model QueryModel to validate incoming queries.
Utility Functions

remove_timestamps(text): Removes timestamps from text using regular expressions.
get_documents(doc_paths): Reads .docx files, extracts question-answer pairs, and returns a list of documents.
Document Processing

Uses glob to find all .docx files in a specified directory.
Processes these documents to extract question-answer pairs and store them in bio_docs.
Model Loading and Embeddings

Loads the Sentence Transformer model (msmarco-bert-base-dot-v5).
Encodes the documents into embeddings using the model and stores these embeddings for future queries.
Runs the model loading and encoding asynchronously to improve performance.
