# prompt_templates.py
# Contains definitions for prompt templates used in our project.

from pydantic import BaseModel
from beeai_framework.utils.templates import PromptTemplate

# RAG Template for generating concise answers
class RAGTemplateInput(BaseModel):
    question: str
    context: str

rag_template: PromptTemplate = PromptTemplate(
    schema=RAGTemplateInput,
    template="""
Context: {{context}}
Question: {{question}}

Provide a concise answer based on the context. Avoid phrases such as 'Based on the context'.""",
)

# Search Query Template for generating effective web search queries
class QuestionInput(BaseModel):
    question: str

search_query_template: PromptTemplate = PromptTemplate(
    schema=QuestionInput,
    template="""Convert the following question into a concise, effective web search query:
Question: {{question}}""",
)

# Search RAG Template for generating answers from search results
class SearchRAGInput(BaseModel):
    question: str
    search_results: str

search_rag_template: PromptTemplate = PromptTemplate(
    schema=SearchRAGInput,
    template="""Search results:
{{search_results}}

Question: {{question}}
Provide a concise answer based on these results. If insufficient, say 'I don't know.'""",
)
