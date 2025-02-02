import pandas as pd 
from Evaluator import Evaluator
import tqdm

llama_responses = pd.read_excel('llama3.2-1b-responses.xlsx', usecols=["prompt", "responses"])

evaluator = Evaluator(client_type="ollama", model="llama3.1:8b")

result = []

for _, row in tqdm.tqdm(llama_responses.iterrows()):
    
    prompt = row['prompt']
    response = row['responses']

    query = f"""
            prompt: {prompt} response: {response}"""
    
    scores = evaluator.evaluate_all(query)


    result.append(scores)

df = pd.DataFrame(result)

df.to_excel('llama_evaluation.xlsx',index=False)
df.to_csv('llama-evaluations.csv',index=False)

