import json
import os
import time
from argparse import ArgumentParser

import litellm
import pandas as pd
import tqdm
from dotenv import load_dotenv
from tqdm import tqdm

from LLMClient import LLMClient

load_dotenv()


def get_json_data(file_name: str):
    with open("data.json", "r") as f:
        data = json.load(f)

    return data


def generate_llm_output(llm_client, data):
    results_list = []

    for data_point in tqdm.tqdm(data):
        results = {}

        prompt = data_point.get("prompt", None)

        llama_response = llm_client.llm_output(query=prompt)

        results["prompt"] = prompt
        results["llama_response"] = llama_response

        results_list.append(results)

    return results_list


def save_results(results, file_name):
    df = pd.DataFrame(results)

    df.to_csv(f"{file_name}.csv", index=False)


if __name__ == "__main__":
    models = ["llama3.2:1b", "deepseek-r1:1.5b"]

    for model in tqdm.tqdm(models):
        llm_client = LLMClient(client_type="ollama", model_name=model)

        data = get_json_data("data.json")

        results = generate_llm_output(llm_client, data)
        print(f"saving results: {model}-responses")

        save_results(results, f"{model}-responses")
