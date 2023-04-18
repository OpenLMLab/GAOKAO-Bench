from bench_function import get_api_key, export_distribute_json, export_union_json
import os
import json
import time

if __name__ == "__main__":
    # Load the FBQ_prompt.json file
    with open("FBQ_prompt.json") as f:
        data = json.load(f)

    # Iterate through the examples in the data
    for i in range(len(data['examples'])):
        directory = ""  # Specify the directory to save the results

        api_key_filename = ""  # Specify the filename containing API keys
        api_key_list = get_api_key(api_key_filename, start_num=0, end_num=1)

        model_name = 'moss'
        temperature = 0.3

        keyword = data['examples'][i]['keyword']
        question_type = data['examples'][i]['type']
        zero_shot_prompt_text = data['examples'][i]['prefix_prompt']
        print(keyword)
        print(question_type)

        # Distribute the examples and process them with the specified model
        export_distribute_json(
            api_key_list,
            model_name,
            temperature,
            directory,
            keyword,
            zero_shot_prompt_text,
            question_type,
            parallel_num=5
        )

        # Merge the processed examples into a single JSON file
        export_union_json(
            directory,
            model_name,
            keyword,
            zero_shot_prompt_text,
            question_type
        )
