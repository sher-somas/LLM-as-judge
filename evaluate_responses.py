import pandas as pd 
from Evaluator import Evaluator
import tqdm
import os

evaluator = Evaluator(client_type="ollama", model="llama3.1:8b")

responses = ['llama3.2-1b-responses.xlsx', 'deepseek-r1-1.5b-responses.xlsx']


def read_responses(filename):

    responses = pd.read_excel('llama3.2-1b-responses.xlsx', usecols=["prompt", "responses"])

    return responses[:100]

def run_evlautions():

    for model_response in responses:

        result = []

        excel_file = read_responses(model_response)

        for _, row in tqdm.tqdm(excel_file.iterrows()):
            
            prompt = row['prompt']
            response = row['responses']

            query = f"""
                    prompt: {prompt} response: {response}"""
            
            scores = evaluator.evaluate_all(query)
            scores['prompt'] = prompt
            scores['responses'] = response

            result.append(scores)

        df = pd.DataFrame(result)

        save_name = os.path.join('evaluations', model_response.split('-responses.xlsx')[0] + '-evaluations.xlsx')

        df.to_excel(save_name,index=False)
        df.to_csv(save_name,index=False)


run_evlautions()
