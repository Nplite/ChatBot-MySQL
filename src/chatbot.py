from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from typing import Dict, List
import os

class SupportChatbot:
    def __init__(self, retriever, model_name: str):
        self.retriever = retriever
        self.model_name = model_name
        
        # Initialize Ollama LLM
        # print(f"Initializing {model_name} model...")
        self.llm = OllamaLLM(
            model=model_name,
            temperature=0.3,  # Lower for more factual responses
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=["question", "context"],
            template="""You are an AI support assistant with access to the company's knowledge base and project information.

                        Answer the user question using ONLY the provided context. Be concise and precise.

                        Context:
                        {context}

                        User Question:
                        {question}

                        Rules:
                        1. Use ONLY the information in the context.
                        2. Do NOT explain, reason, or describe your steps.
                        3. Do NOT invent information.
                        4. If context lacks relevant info, say: 
                        "The provided query does not contain information in the database"
                        5. Keep the answer (2–5 sentences).

                        Answer:

                        """
                                )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
    
    def format_context(self, context: Dict) -> str:
        formatted_parts = []
        
        # Knowledge base
        if context['knowledgebase']:
            kb_text = "\n\nKNOWLEDGE BASE:\n"
            for i, doc in enumerate(context['knowledgebase'][:3], 1):
                kb_text += f"{i}. {doc.page_content[:300]}...\n"
            formatted_parts.append(kb_text)
        
        # Projects
        if context['projects']:
            proj_text = "\n\nRELATED PROJECTS:\n"
            for i, doc in enumerate(context['projects'][:2], 1):
                proj_text += f"{i}. {doc.page_content[:200]}...\n"
            formatted_parts.append(proj_text)
        
        return "\n".join(formatted_parts) if formatted_parts else "No relevant context found."


    def answer_question(self, question: str) -> Dict:
        """Answer user questions using ONLY KB + project info"""
      
        # Retrieve relevant context
        context = self.retriever.retrieve_context(question, k=5)

        # Format context for prompt
        formatted_context = self.format_context(context)
        
        # Generate response
        response = self.chain.invoke({
            "question": question,
            "context": formatted_context
        })
        
        # Extract text
        if isinstance(response, dict):
            response = response.get('text', str(response))
        else:
            response = str(response)

        
        return {
            'answer': response.strip(),
            # 'troubleshooting_steps': suggestions,
            'sources_used': {
                'knowledgebase': len(context['knowledgebase']),
                'projects': len(context['projects']),
            }
        }
    
    def chat(self):

        print("\n" + "="*60)
        print("AI Support Assistant - Ready!")
        # print("Type 'exit' to quit.")
        print("="*60 + "\n")
        
        while True:
            print("-" * 60)
            user_input = input("\n👤 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'exit':
                print("\nGoodbye! 👋")
                break
            
            try:
                result = self.answer_question(user_input)
                
                print(f"\n🤖 Assistant: {result['answer']}\n")
                
                # if result['troubleshooting_steps']:
                #     print("\n💡 Suggested Next Steps:")
                #     for i, step in enumerate(result['troubleshooting_steps'], 1):
                #         print(f"  {i}. {step}")
                
                print(f"📚 Sources: "
                      f"KB({result['sources_used']['knowledgebase']}) | "
                      f"Projects({result['sources_used']['projects']})\n")
    
                
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try rephrasing your question.")
