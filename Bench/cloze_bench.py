import sys
import os
parent_path = os.path.dirname(sys.path[0])
if parent_path not in sys.path:
    sys.path.append(parent_path)

from models.Moss import MossAPI
from models.Openai import OpenaiAPI

from bench_function import get_api_key, export_distribute_json, export_union_json
import json
import time

if __name__ == "__main__":
    # Load the FBQ_prompt.json file
    with open("FBQ_prompt.json") as f:
        data = json.load(f)['examples']

    # Iterate through the examples in the data
    for i in range(len(data)):
        directory = "../data/Fill-in-the-blank_Questions"

        openai_api_key_file = "your openai api key list"
        openai_api_key_list = get_api_key(openai_api_key_file, start_num=0, end_num=1)
        # moss_api_key_list = [""]
    
        model_name = 'gpt-3.5-turbo'
        model_api = OpenaiAPI(openai_api_key_list, model_name='gpt-3.5-turbo')
        # model_name = 'moss'
        # model_api = MossAPI(moss_api_key_list)
        
        keyword = data[i]['keyword']
        question_type = data[i]['type']
        zero_shot_prompt_text = data[i]['prefix_prompt']
        print(keyword)
        print(question_type)

        export_distribute_json(
            model_api, 
            model_name, 
            directory, 
            keyword, 
            zero_shot_prompt_text, 
            question_type, 
            parallel_num=5, 
        )

        export_union_json(
            directory, 
            model_name, 
            keyword,
            zero_shot_prompt_text,
            question_type
        )
