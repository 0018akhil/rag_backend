from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
import requests
from .. import crud, models, schemas
from ..dependencies import get_current_user, get_db
from ..s3_utils import upload_file_to_s3
import uuid
from dotenv import load_dotenv
import os
import time
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

load_dotenv()

router = APIRouter()


def parse_document(file: UploadFile):
    unstructured_api_url = "https://api.unstructuredapp.io/general/v0/general"
    api_key = os.getenv("UNSTRUCTURED_API_KEY")

    headers = {
        "Accept": "application/json",
        "unstructured-api-key": api_key
    }

    files = {"files": (file.filename, file.file, file.content_type)}

    response = requests.post(unstructured_api_url,
                             headers=headers, files=files)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code,
                            detail="Error parsing document")


def process_and_index_documents(elements, index_name):
    documents = []
    for element in elements:
        if element['type'] in ['Title', 'NarrativeText']:
            doc = Document(
                page_content=element['text'],
                metadata={
                    'type': element['type'],
                    'page_number': element['metadata']['page_number'],
                    'filename': element['metadata']['filename']
                }
            )
            documents.append(doc)

    embeddings = HuggingFaceEmbeddings()
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

    pc.create_index(
        name=index_name,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)

    docsearch = PineconeVectorStore.from_documents(documents, embeddings, index_name=index_name)

    if not docsearch:
        return False
    
    return True

@router.post("/documents/", response_model=schemas.Document)
async def create_document(
    title: str = Form(...),
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    s3_object_key = str(uuid.uuid4())
    document = schemas.DocumentCreate(title=title)
    parsed_document = parse_document(file)
    index_document = process_and_index_documents(
        parsed_document, index_name=s3_object_key)
    if not index_document:
        raise HTTPException(
            status_code=500, detail="Error processing document")

    return crud.create_document(db=db, document=document, user_id=current_user.id, s3_object_key=s3_object_key)


@router.get("/documents/", response_model=list[schemas.Document])
def read_documents(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    documents = crud.get_documents(
        db, user_id=current_user.id, skip=skip, limit=limit)
    return documents
