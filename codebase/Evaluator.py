import json
import os
import random

from dotenv import load_dotenv
from groq import Groq
from opik import track

from LLMClient import LLMClient

import evaluation_prompts
import parsers
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY")) 


EVALUATION_MODEL = "llama-3.3-70b-versatile"


class Evaluator:

    def __init__(self, client_type: str= "groq", model="llama-3.3-70b-versatile") -> None:
        self.model = model
        self.client_type = client_type
        self.client = LLMClient(client_type=self.client_type, model_name=self.model)
                
    def evaluate_all(self, input_str) -> tuple:

        result = {}

        result['relevance_score'], result['relevance_explanation'] = self.relevance_metric(input_str)
        result['accuracy_score'], result['accuracy_explanation'] = self.accuracy_metric(input_str)
        result['hallucination_score'], result['hallucination_explanation'] = self.hallucination_metric(input_str)

        return result

    @staticmethod
    def calculate_score(total_score):
        pass

    # @track
    def relevance_metric(self, input_str) -> str:
        
        total_score = 0

        # response = self.client.structured_output_query(query=input_str, custom_response_model=parsers.RelevanceAnswer, evaluation_prompt=evaluation_prompts.relevance_prompt)
        response = self.client.ollama_output_query(query=input_str, custom_response_model=parsers.RelevanceAnswer, evaluation_prompt=evaluation_prompts.relevance_prompt)
        
        explanation = None

        if response is not None:

            factual_accuracy = response.factual_accuracy
            completeness = response.completeness
            clarity = response.completeness
            # politeness = response.politeness
            explanation = response.explanation
            
            total_score = (factual_accuracy +  completeness +  clarity) / 100

            # if total_score > 1:
            #     total_score = (factual_accuracy +  completeness +  clarity) / 100                


        return total_score, explanation

    # @track
    def accuracy_metric(self, input_str) -> str:

        total_score = 0
        explanation = None

        # response = self.client.structured_output_query(query=input_str, custom_response_model=parsers.AccuracyAnswer, evaluation_prompt=evaluation_prompts.accuracy_prompt)
        response = self.client.ollama_output_query(query=input_str, custom_response_model=parsers.AccuracyAnswer, evaluation_prompt=evaluation_prompts.accuracy_prompt)

        # print(f"accuracy response: {response}")
        if response is not None:

            factual_correctness = response.factual_correctness
            relevance = response.relevance
            completeness = response.completeness
            clarity = response.clarity
            # logical_consistency = response.logical_consistency
            explanation = response.explanation

            total_score = (factual_correctness + relevance + completeness + clarity) / 100

        return total_score, explanation

    
    # @track
    def hallucination_metric(self, input_str):
        
        total_score = 0
        explanation = None

        # response = self.client.structured_output_query(query=input_str, custom_response_model=parsers.HallucinationAnswer, evaluation_prompt=evaluation_prompts.hallucination_score)
        response = self.client.ollama_output_query(query=input_str, custom_response_model=parsers.HallucinationAnswer, evaluation_prompt=evaluation_prompts.hallucination_score)

        if response is not None:

            factual_accuracy = response.factual_accuracy
            logical_consistency = response.logical_consistency
            relevance = response.relevance
            # clarity = response.clarity
            explanation = response.explanation

            total_score = (factual_accuracy + logical_consistency + relevance ) / 100

        return total_score, explanation


if __name__ == "__main__":

    llm_evaluator = Evaluator(client_type="ollama", model="llama3.1:latest")


    question = "why is the sky blue"

    answer = """The sky appears blue to us because of a phenomenon called scattering, which occurs when sunlight interacts with tiny molecules of gases in the atmosphere. Here's why:

**Short answer:**

When sunlight enters Earth's atmosphere, it encounters tiny molecules of gases like nitrogen (N2) and oxygen (O2). These molecules scatter the light in all directions, but they scatter shorter (blue) 
wavelengths more than longer (red) wavelengths. This is known as Rayleigh scattering. As a result, our eyes see the blue light scattered in every direction, making the sky appear blue.

**A bit more detail:**

Here's what happens when sunlight hits the atmosphere:

1. **Solar radiation**: The sun emits a wide range of electromagnetic radiation, including visible light, ultraviolet (UV) radiation, and X-rays.
2. **Entry into atmosphere**: When this solar radiation enters Earth's atmosphere, it encounters tiny molecules of gases like N2 and O2.
3. **Scattering**: These gas molecules scatter the light in all directions, but they scatter shorter wavelengths more efficiently than longer wavelengths. This is because smaller molecules interact with 
the electric field component of shorter wavelengths (like blue) more effectively than with the electric field component of longer wavelengths (like red).
4. **Blue dominance**: As a result of this scattering effect, the sky appears blue to us because our eyes are sensitive to blue light and it's scattered in all directions.
5. **Red light absorption**: Meanwhile, red light is not scattered as much, so it travels through the atmosphere with less interference. However, some red light is absorbed by atmospheric gases like water 
vapor and pollutants.

**Other factors that influence sky color:**

While scattering is the main reason for the blue sky, other factors can affect its appearance:

* **Time of day**: During sunrise and sunset, the angle of the sun relative to our line of sight changes. This leads to longer paths through the atmosphere, scattering more red light and making the sky 
appear reddish-orange.
* **Air pollution**: Tiny particles in polluted air scatter light in a way that's similar to gas molecules, but with different wavelengths being emphasized. This can result in a hazy or grayish appearance 
of the sky.
* **Clouds**: Clouds reflect and absorb sunlight, which can alter the apparent color of the sky.

Now you know why the sky is blue!"""

    question1 = "A man with blonde hair and brown shirt is drinking water from the fountain"
    answer1 = "The alps are magnificent"

    query = f"""question: {question1} answer: {answer1}"""
    

    print(query)

    # relevance_evaluation = llm_evaluator.relevance_metric(query)
    # accuracy_evaluation = llm_evaluator.accuracy_metric(query)
    # hallucination_evaluation = llm_evaluator.hallucination_metric(query)
    # print(f"relevancy: {relevance_evaluation}\t accracy: {accuracy_evaluation}\t hallucination: {hallucination_evaluation}")

    llm_evaluator.evaluate_all(query)






    