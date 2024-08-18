from sqlalchemy.orm import Session
from ..schemas.chat import ChatMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from ..core.config import settings
from ..db.models.document import Document

class ChatService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro", google_api_key=settings.GOOGLE_API_KEY)
        self.embeddings = HuggingFaceEmbeddings()
        self.pinecone = Pinecone(api_key=settings.PINECONE_API_KEY)

    async def process_chat(self, db: Session, chat_message: ChatMessage, current_user):
        prompt = self._create_prompt()
        index_name = self.get_document_index_name(db, chat_message.document_id)
        retriever = self._setup_retriever(index_name)
        rag_chain = self._create_rag_chain(prompt, retriever)
        message = rag_chain.invoke(chat_message.message)
        return {"reply": f"{message}"}

    def _create_prompt(self):
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
        return PromptTemplate(
            input_variables=["context", "user_query"],
            template=prompt_template,
        )

    def _setup_retriever(self, index_name):
        index = self.pinecone.Index(index_name)
        pc = PineconeVectorStore(index=index, embedding=self.embeddings)
        return pc.as_retriever(search_type="similarity", search_kwargs={"k": 4})

    def _create_rag_chain(self, prompt, retriever):
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        return (
            {"context": retriever | format_docs,
                "user_query": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def get_document_index_name(self, db: Session, document_id: int):
        return db.query(Document).filter(Document.id == document_id).first().index_name
