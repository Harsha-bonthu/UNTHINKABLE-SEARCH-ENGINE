import os
from typing import List, Tuple, Dict, Any
import asyncio
import logging
import openai
from openai import AsyncOpenAI
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMService:
    """Service for generating responses using Large Language Models"""

    def __init__(self):
        self.openai_client = None
        self.use_openai = False

        # Check if OpenAI API key is available
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if openai_api_key:
            self.openai_client = AsyncOpenAI(api_key=openai_api_key)
            self.use_openai = True
            logger.info("OpenAI client initialized")
        else:
            logger.info("No OpenAI API key found, using fallback response generator")

    async def generate_response(self, 
                              query: str, 
                              context_chunks: List[Tuple[str, Dict[str, Any], float]]) -> str:
        """Generate a response based on query and retrieved context"""

        if not context_chunks:
            return "I couldn't find relevant information to answer your question."

        # Prepare context from retrieved chunks
        context = self._prepare_context(context_chunks)

        if self.use_openai:
            return await self._generate_openai_response(query, context)
        else:
            return await self._generate_fallback_response(query, context, context_chunks)

    def _prepare_context(self, context_chunks: List[Tuple[str, Dict[str, Any], float]]) -> str:
        """Prepare context string from retrieved chunks"""

        context_parts = []
        for i, (text, metadata, score) in enumerate(context_chunks[:5]):  # Limit to top 5
            source = metadata.get('source', 'Unknown')
            chunk_id = metadata.get('chunk_id', 0)

            context_parts.append(f"[Source {i+1}: {source}, Chunk {chunk_id}]\n{text}\n")

        return "\n".join(context_parts)

    async def _generate_openai_response(self, query: str, context: str) -> str:
        """Generate response using OpenAI API"""

        system_prompt = """You are a helpful AI assistant that answers questions based on provided context. 

        Instructions:
        - Answer the question based ONLY on the provided context
        - If the context doesn't contain enough information, say so clearly
        - Be concise but comprehensive
        - Cite specific sources when making claims
        - If asked about something not in the context, politely decline and explain what information is available
        """

        user_prompt = f"""Context:
{context}

Question: {query}

Please provide a detailed answer based on the context above."""

        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return f"Sorry, I encountered an error generating the response: {str(e)}"

    async def _generate_fallback_response(self, 
                                        query: str, 
                                        context: str, 
                                        context_chunks: List[Tuple[str, Dict[str, Any], float]]) -> str:
        """Generate a fallback response using simple text processing"""

        # Simple keyword-based response generation for demo purposes
        query_lower = query.lower()

        # Find the most relevant chunk
        if context_chunks:
            best_chunk, best_metadata, best_score = context_chunks[0]

            # Extract key sentences from the best chunk
            sentences = [s.strip() for s in best_chunk.split('.') if s.strip()]

            # Find sentences that contain query keywords
            query_words = set(query_lower.split())
            relevant_sentences = []

            for sentence in sentences:
                sentence_words = set(sentence.lower().split())
                if query_words.intersection(sentence_words):
                    relevant_sentences.append(sentence)

            if relevant_sentences:
                response = "Based on the available information:\n\n"
                response += ". ".join(relevant_sentences[:3])  # Top 3 relevant sentences
                response += f"\n\nSource: {best_metadata.get('source', 'Unknown document')}"
                response += f" (Relevance: {best_score:.2f})"
            else:
                response = f"I found information related to your query in {best_metadata.get('source', 'the document')}, "
                response += f"but I couldn't extract specific details. Here's what I found:\n\n"
                response += best_chunk[:300] + "..." if len(best_chunk) > 300 else best_chunk
                response += f"\n\n(Relevance: {best_score:.2f})"
        else:
            response = "I couldn't find relevant information to answer your question in the uploaded documents."

        # Add information about multiple sources if available
        if len(context_chunks) > 1:
            sources = [metadata.get('source', 'Unknown') for _, metadata, _ in context_chunks[:3]]
            unique_sources = list(set(sources))
            if len(unique_sources) > 1:
                response += f"\n\nInformation was found across {len(unique_sources)} sources: {', '.join(unique_sources)}"

        return response

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model configuration"""
        return {
            'using_openai': self.use_openai,
            'model': 'gpt-3.5-turbo' if self.use_openai else 'fallback-text-processor',
            'api_key_configured': bool(os.getenv('OPENAI_API_KEY')),
        }