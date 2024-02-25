import sys
import os
parent_path = os.path.dirname(sys.path[0])
if parent_path not in sys.path:
    sys.path.append(parent_path)

from Models.openai_gpt4 import OpenaiAPI
from bench_function import subjective_grade
import json
import argparse

teacher_prompt_template_wo_marking_criterion = "【题目】{question}\n【分析过程】{analysis}\n【标准答案】{standard_answer}\n【分值】{score}\n【学生分析与答案】{model_output}\n"


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--openai_api_key', type=str)
    args = parser.parse_args()
    openai_api_key = args.openai_api_key

    teacher_model_name = 'gpt-4-1106-preview'
    teacher_model_api = OpenaiAPI([openai_api_key], model_name=teacher_model_name, temperature=0.0, max_tokens=4096)
    result_directory = "../Results/gpt_4_sub"
    

    w_marking_criterion = False
    teacher_prompt_template = teacher_prompt_template_wo_marking_criterion

    with open("./Sub_Grade_Prompt_wo_marking_criterion.json", "r") as f:
        data = json.load(f)['examples']
        f.close()

    for i in range(len(data)):
        keyword = data[i]['keyword']

        question_type = data[i]['type']
        zero_shot_prompt_text = data[i]['prefix_prompt']
        
        print(f"Using {teacher_model_name} to correct {keyword} ")

        assert question_type in ['cloze', 'subjective', 'correction'], "question_type must be subjective or cloze or correction"
        subjective_grade(
            teacher_model_api,
            teacher_model_name,
            keyword,
            zero_shot_prompt_text,
            w_marking_criterion,
            teacher_prompt_template,
            result_directory, 
            marking_criterion_directory=None
        )





    

