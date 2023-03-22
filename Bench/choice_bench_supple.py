from bench_function import choice_test, get_api_key, export_distribute_json, export_union_json
import json
import os
# 取自zxh.txt最后一个
API_KEY = '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'
keyword = "英语全国卷完形填空"
question_type = "multi_question_choice"
zero_shot_prompt_text = ""
directory = "./2010-2018全国卷全科题目"
model_name  = "gpt-3.5-turbo"

for root, dirs, files in os.walk(directory):
    for file in files:
        if keyword in file and file.endswith(".json"):
        # 如果文件名中包含关键字并且是JSON文件
            
            filepath = os.path.join(root, file)
            print("打开文件：",filepath)
            # 打开JSON文件并加载数据
            with open(filepath, "r") as f:
                data = json.load(f)

dict = {
    "api_key": API_KEY,
    "start_num": 0,
    "end_num": 5,
    "model_name": model_name,
    "data": data,
    "keyword": keyword,
    "zero_shot_prompt_text":zero_shot_prompt_text,
    "temperature":0.3,
    "question_type":question_type
}

choice_test(**dict)


# export_union_json(model_name,keyword,zero_shot_prompt_text)
