import os
import nest_asyncio
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
import torch
import glob
from docx import Document
import re
import asyncio

os.environ["UVLOOP_NO_EXTENSIONS"] = "1"
nest_asyncio.apply()

app = FastAPI()
templates = Jinja2Templates(directory="/Users/pridhvipinninti/Downloads/templates")

class QueryModel(BaseModel):
    query: str

def remove_timestamps(text):
    return re.sub(r'\b\d{1,2}:\d{2}\b', '', text).strip()

def get_documents(doc_paths):
    documents = []
    for doc in doc_paths:
        docx_doc = Document(doc)
        qa_pairs = []
        question = None
        answer = ''
        for para in docx_doc.paragraphs:
            text = para.text.strip()
            text = remove_timestamps(text)
            if question is not None and (text.startswith('#') or '?' in text or 'Interviewer' in text):
                qa_pairs.append({'question': question.strip(), 'answer': answer.strip()})
                if '?' in text:
                    parts = text.rsplit('?', 1)
                    question = parts[0].strip() + '?'
                    answer = parts[1].strip() + ' '
                else:
                    question = text
                    answer = ''
            elif question is None and (text.startswith('#') or '?' in text or 'Interviewer' in text):
                if '?' in text:
                    parts = text.rsplit('?', 1)
                    question = parts[0].strip() + '?'
                    answer = parts[1].strip() + ' '
                else:
                    question = text
                    answer = ''
            else:
                answer += text + ' '
        if question is not None:
            qa_pairs.append({'question': question.strip(), 'answer': answer.strip()})
        documents.append(qa_pairs)
    return documents

doc_paths = glob.glob('/Users/pridhvipinninti/Downloads/ENDO_Data/*.docx')
transcript_document_content = get_documents(doc_paths)

bio_docs = []
for doc in transcript_document_content:
    for qa_pair in doc:
        bio_docs.append({'context': qa_pair['answer'], 'question': qa_pair['question']})

model = None
corpus_embeddings = None
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

async def load_model_and_documents():
    global model, corpus_embeddings
    model = SentenceTransformer('msmarco-bert-base-dot-v5')
    corpus_embeddings = model.encode(bio_docs, convert_to_tensor=True, batch_size=32, device=device)

loop = asyncio.get_event_loop()
loop.run_until_complete(load_model_and_documents())

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/query/")
async def query_documents(query: QueryModel, request: Request):
    query_embedding = model.encode(query.query, convert_to_tensor=True, device=device)
    cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=3)

    relevant_context = []
    for score, idx in zip(top_results[0], top_results[1]):
        relevant_context.append({
            'question': bio_docs[idx]['question'],
            'answer': bio_docs[idx]['context'],
            'score': float(score)
        })

    return templates.TemplateResponse("results.html", {"request": request, "results": relevant_context})

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8003, log_level="info")
