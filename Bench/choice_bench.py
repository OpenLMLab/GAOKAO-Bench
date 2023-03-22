from bench_function import choice_test, get_api_key, export_distribute_json, export_union_json
import os
import json
import time

if __name__ == "__main__":
    with open("客观题prompt.json", "r") as f:
        data = json.load(f)
    f.close()
    for i in range(4, 5):
        # 生成分散的json文件
        api_key_filename = "zxt.txt"
        api_key_list = get_api_key(api_key_filename, start_num=0, end_num = 2)
        model_name = "gpt-3.5-turbo"
        temperature = 0.3
        directory = "./2010-2018全国卷全科题目"
        keyword = data['examples'][i]['keyword']
        question_type = data['examples'][i]['type']
        zero_shot_prompt_text = data['examples'][i]['prefix_prompt']

        export_distribute_json(api_key_list, model_name, temperature, directory, keyword, zero_shot_prompt_text, question_type)


        # 将分散的json文件合并成一个文件，并计算准确率
        export_union_json(model_name,keyword,zero_shot_prompt_text,question_type)
        print(f"客观题|{keyword}|完成")
        print('-'*100)


