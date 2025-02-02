# from typing import List
# import os
# # from groq import Groq
from dotenv import load_dotenv
from litellm import completion
import instructor
from openai import OpenAI
from parsers import RelevanceAnswer
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaLLM


load_dotenv()



class LLMClient:

    def __init__(self, client_type: str = "ollama", model_name: str = "llama3.2:1b"):
        
        
        self.client_type = client_type
        self.model_name = model_name
        self.instructor_client = None
        self.model = f"{client_type}/{model_name}"

    
    def llm_output(self, query: str, evaluation_prompt: str = "You are a helpful assistant."):

        response = None

        messages = [
            {"role": "system", "content": evaluation_prompt},
            {"role": "user", "content": query},
        ]

        try: 
        
            response = completion(model=self.model, messages=messages)
            if response is not None:
                return response.choices[0].message.content
        except Exception as e:
            print(f"something went wrong")
            print(e)

        return response.choices[0].message.content
    
    
    def output_with_tool(self, query: str, custom_response_model, evaluation_prompt: str = "You are a helpful assistant."):

        response = None

        messages = [
            {"role": "system", "content": evaluation_prompt},
            {"role": "user", "content": query},
        ]

        try:

            instructor_client = instructor.from_openai(OpenAI(base_url="http://localhost:11434/v1", api_key="ollama"),mode=instructor.Mode.JSON) #
            response = instructor_client.chat.completions.create(model=self.model_name,
                                                                messages=messages, 
                                                                response_model=custom_response_model,
                                                                )
            
            return response

        except Exception as e:
            print(f"Something wrong with Ollama client: {e}")
            print(e)


        return response


if __name__ == "__main__":

    llm_client = LLMClient(client_type="ollama", model_name="llama3.2:1b")

    response = llm_client.llm_output(query="Why is the sky blue?")

    print(f"response: {response}")