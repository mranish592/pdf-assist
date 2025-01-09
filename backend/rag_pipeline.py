from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from typing import List, Dict
import os

class RAGPipeline:
    def __init__(self):
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="mixtral-8x7b-32768"
        )
        
    def generate_answer(self, query: str, context_docs: List[Dict]) -> str:
        """Generate answer based on retrieved documents."""
        # Prepare context from retrieved documents
        context = "\n".join([
            f"[Page {doc['metadata']['page']}, Line {doc['metadata']['line']}]: {doc['content']}"
            for doc in context_docs
        ])
        
        prompt = PromptTemplate(
            template="""You are a legal assistant. Use the following context to answer the question. 
            Include page and line references in your answer when citing specific information.
            
            Context:
            {context}
            
            Question: {question}
            
            Answer:""",
            input_variables=["context", "question"]
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(context=context, question=query)
        
        return response 