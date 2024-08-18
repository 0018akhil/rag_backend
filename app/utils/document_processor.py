import requests
from fastapi import HTTPException
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from ..core.config import settings
import time

class DocumentProcessor:
    def __init__(self):
        self.unstructured_api_url = "https://api.unstructuredapp.io/general/v0/general"
        self.embeddings = HuggingFaceEmbeddings()
        self.pinecone = Pinecone(api_key=settings.PINECONE_API_KEY)

    def parse_document(self, file):
        headers = {
            "Accept": "application/json",
            "unstructured-api-key": settings.UNSTRUCTURED_API_KEY
        }

        files = {"files": (file.filename, file.file, file.content_type)}

        response = requests.post(self.unstructured_api_url, headers=headers, files=files)

        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Error parsing document")

    def process_and_index_documents(self, elements, index_name):
        documents = self._create_documents(elements)
        self._create_pinecone_index(index_name)
        return self._index_documents(documents, index_name)

    def _create_documents(self, elements):
        return [
            Document(
                page_content=element['text'],
                metadata={
                    'type': element['type'],
                    'page_number': element['metadata']['page_number'],
                    'filename': element['metadata']['filename']
                }
            )
            for element in elements
            if element['type'] in ['Title', 'NarrativeText']
        ]

    def _create_pinecone_index(self, index_name):
        self.pinecone.create_index(
            name=index_name,
            dimension=768,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        while not self.pinecone.describe_index(index_name).status["ready"]:
            time.sleep(1)

    def _index_documents(self, documents, index_name):
        docsearch = PineconeVectorStore.from_documents(documents, self.embeddings, index_name=index_name)
        return bool(docsearch)