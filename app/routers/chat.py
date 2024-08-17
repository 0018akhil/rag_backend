from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..dependencies import get_current_user, get_db
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from .. import crud

load_dotenv()

router = APIRouter()


@router.post("/chat", response_model=dict)
async def chat_with_document(
    chat_message: schemas.ChatMessage,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))

    prompt_template = """
You are an AI assistant designed to answer questions based on specific document contexts. You will be provided with relevant information extracted from various document types (CSV, PDF, PPT, etc.) through a vector database search.

Context: {context}

User Query: {user_query}

Instructions:
1. Provide a conversational and informative answer based solely on the given context.
2. If the user's query cannot be answered using the provided context, respond with "I'm sorry, but the answer to your question is out of context of the document provided."
3. Do not invent or assume information beyond what is explicitly stated in the given context.
4. If clarification is needed, ask the user for more details.
5. Maintain a helpful and friendly tone throughout the conversation.
6. If appropriate, suggest related questions the user might find interesting based on the context.

Remember, your knowledge is limited to the context provided. Do not reference external information or personal knowledge.
    """

    prompt = PromptTemplate(
        input_variables=["context", "user_query"],
        template=prompt_template,
    )

    embeddings = HuggingFaceEmbeddings()

    index_name = crud.get_specific_document(db, chat_message.document_id).s3_object_key

    index = Pinecone(api_key=os.getenv("PINECONE_API_KEY")).Index(index_name)

    pc = PineconeVectorStore(index=index, embedding=embeddings)

    retriever = pc.as_retriever(search_type="similarity", search_kwargs={"k": 4})


    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "user_query": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    message = rag_chain.invoke(chat_message.message)

    return {"reply": f"{message}"}
