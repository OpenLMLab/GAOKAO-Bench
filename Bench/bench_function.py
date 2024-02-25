
import os
import json
import time
import re
from random import choice
import requests
from typing import List, Union, Dict
# from joblib import Parallel, delayed
import codecs

from tqdm import  tqdm



def get_api_key(filename: str, start_num: int, end_num: int) -> List[str]:
    """
    Retrieves API keys from a file.

    :param filename: Name of the file containing API keys
    :param start_num: Starting line number for reading the file
    :param end_num: Ending line number for reading the file
    :return: List of API keys
    """
    with codecs.open(filename, 'r', 'utf-8') as file:
        lines = file.readlines()
    
    pattern = re.compile(r'sk-[\s\S]*?(?=\s*\n)')
    api_key_list = []
    
    for i in range(start_num, end_num):
        api_key = pattern.findall(lines[i])
        if len(api_key) != 0:
            api_key_list.append(api_key[0])
    
    return api_key_list


def extract_choice_answer(model_output, question_type, answer_lenth=None):
    """
    Extract choice answer from model output

    Format of model_output that is expected:
    'single_choice': choice answer should be the last Capital Letter of the model_output, e.g.: "...【答案】 A <eoa>"
    'multi_question_choice': "...【答案】A ... 【答案】C ..." or write the choice answers at the beginning of the model_output, e.g. "A C D E F...."
    'multi_choice': "...【答案】 ABD " or write the choice answers at the end of the model_output, e.g. "... ACD"
    'five_out_of_seven': choice answers should be the first five Capital Letters of the model_output, e.g. "A C D F B ...."
    """
    if question_type == 'single_choice':
        model_answer = []
        temp = re.findall(r'[A-D]', model_output[::-1])
        if len(temp) != 0:
            model_answer.append(temp[0])

    elif question_type == 'multi_question_choice':
        model_answer = []
        temp = re.findall(r"【答案】\s*[:：]*\s*[A-Z]", model_output)
            
        if len(temp) == answer_lenth:
            for t in temp:
                model_answer.append(re.findall(r'[A-Z]', t)[0])
        else:
            temp = re.findall(r"[A-Z]", model_output)
            if len(temp) > 0:
                for k in range(min(len(temp), answer_lenth)):
                    model_answer.append(temp[k])

    elif question_type == 'multi_choice':
        model_answer = []
        answer = ''
        content = re.sub(r'\s+', '', model_output)
        answer_index = content.find('【答案】')
        if answer_index > 0:
            temp = content[answer_index:]
            if len(re.findall(r'[A-D]', temp)) > 0:
                for t in re.findall(r'[A-D]', temp):
                    answer += t
        else:
            temp = content[-10:]
            if len(re.findall(r'[A-D]', temp)) > 0:
                for t in re.findall(r'[A-D]', temp):
                    answer += t
        if len(answer) != 0:
            model_answer.append(answer)
    
    elif question_type == 'five_out_of_seven':
        model_answer = []
        temp = re.findall(r'[A-G]', model_output)
        if len(temp) > 0:
            for k in range(min(5, len(temp))):
                model_answer.append(temp[k])

    return model_answer

def choice_test(**kwargs):
    """
    
    Get answers of the Choice Questions
    
    """


    model_api = kwargs['model_api']
    model_name = kwargs['model_name']
    start_num = kwargs['start_num']
    end_num = kwargs['end_num']
    data = kwargs['data']['example']
    keyword = kwargs['keyword']
    prompt = kwargs['prompt']
    question_type = kwargs['question_type']
    save_directory = kwargs['save_directory']
   
    model_answer_dict = []
    for i in tqdm(range(start_num, end_num)):

        index = data[i]['index']
        question = data[i]['question'].strip() + '\n'
        year = data[i]['year']
        category = data[i]['category']
        score = data[i]['score']
        standard_answer = data[i]['standard_answer']
        answer_lenth = len(standard_answer)
        analysis = data[i]['analysis']

        model_output = model_api(prompt, question)
        model_answer = extract_choice_answer(model_output, question_type, answer_lenth)
        # TODO: which content of temp we expect

        dict = {
            'index': index, 
            'year': year, 
            'category': category,
            'score': score,
            'question': question, 
            'standard_answer': standard_answer,
            'analysis': analysis,
            'model_answer': model_answer,
            'model_output': model_output
        }
        model_answer_dict.append(dict)

        time.sleep(5)

    file_name = model_name+"_seperate_"+keyword+f"_{start_num}-{end_num-1}.json"
    file_path = os.path.join(save_directory, file_name)
    with codecs.open(file_path, 'w', 'utf-8') as f:
        output = {
            'keyword': keyword, 
            'example' : model_answer_dict
            }
        json.dump(output, f, ensure_ascii=False, indent=4)
        f.close()

def subjective_test(**kwargs):
    """
    
    Get answers of the Subjective Questions

    """

    model_api = kwargs['model_api']
    model_name = kwargs['model_name']
    start_num = kwargs['start_num']
    end_num = kwargs['end_num']
    data = kwargs['data']['example']
    keyword = kwargs['keyword']
    prompt = kwargs['prompt']
    question_type = kwargs['question_type']
    save_directory = kwargs['save_directory']
   
    model_answer_dict = []
    for i in tqdm(range(start_num, end_num)):

        index = data[i]['index']
        question = data[i]['question'].strip() + '\n'
        year = data[i]['year']
        category = data[i]['category']
        score = data[i]['score']
     

        standard_answer = data[i]['standard_answer']
        analysis = data[i]['analysis']

        model_output = model_api(prompt, question)

        dict = {
            'index': index, 
            'year': year, 
            'category': category,
            'score': score,
            'question': question, 
            'standard_answer': standard_answer,
            'analysis': analysis,
            'model_output': model_output
        }
        model_answer_dict.append(dict)

        time.sleep(20)

    file_name = model_name+"_seperate_"+keyword+f"_{start_num}-{end_num-1}.json"
    file_path = os.path.join(save_directory, file_name)
    with codecs.open(file_path, 'w', 'utf-8') as f:
        output = {
            'keyword': keyword, 
            'example' : model_answer_dict
            }
        json.dump(output, f, ensure_ascii=False, indent=4)
        f.close()

def extract_correction_answer(model_output):
    """
    Extract correction answer from model_output

    Format of model_output that is expected:
    "【答案】把is改成are， 删去they ... <eoa>" or "【答案】把is改成are， 删去they ... "
    """
    model_answer = []
        
    start_idx = model_output.find('【答案】')
    end_idx = model_output.find('<eoa>')

    if start_idx >= 0:
        if end_idx >= 0:
            answer = model_output[start_idx:end_idx]
        else:
            answer = model_output[start_idx:]
    else:
        answer = ""
    if len(answer) != 0:
        model_answer.append(answer)

    return model_answer



def correction_test(**kwargs):
    """

    Get answers of the Correction Questions

    """

    model_api = kwargs['model_api']
    model_name = kwargs['model_name']
    start_num = kwargs['start_num']
    end_num = kwargs['end_num']
    data = kwargs['data']['example']
    keyword = kwargs['keyword']
    prompt = kwargs['prompt']
    save_directory = kwargs['save_directory']
   
    model_answer_dict = []

    for i in tqdm(range(start_num, end_num)):
        index = data[i]['index']
        question = data[i]['question'].strip() + '\n'
        year = data[i]['year']
        category = data[i]['category']
        score = data[i]['score']
        standard_answer = data[i]['standard_answer']
        analysis = data[i]['analysis']

        model_output_1 = model_api(prompt[0], question)
        
        start_idx = model_output_1.find('【答案】')
        end_idx = model_output_1.find('<eoa>')

        article_1 = question.split('不计分。')[1]
                
        if start_idx >= 0:
            if end_idx >= 0:
                article_2 = model_output_1[start_idx+4:end_idx].strip()
            else:
                article_2 = model_output_1[start_idx+4:].strip()
        else:
            article_2 = ""

        model_output_2 = model_api(prompt[1], "Article 1:" +article_1+"\nArticle 2:"+article_2)
        
        model_answer = extract_correction_answer(model_output_2)
        
        dict = {
            'index': index, 
            'year': year, 
            'category': category,
            'score': score,
            'question': question, 
            'standard_answer': standard_answer,
            'analysis': analysis,
            'model_answer': model_answer,
            'model_output': model_output_2
        }
        model_answer_dict.append(dict)

        time.sleep(10)

    file_name = model_name+"_seperate_"+keyword+f"_{start_num}-{end_num-1}.json"
    file_path = os.path.join(save_directory, file_name)
    with codecs.open(file_path, 'w', 'utf-8') as f:
        output = {
            'keyword': keyword, 
            'example' : model_answer_dict
            }
        json.dump(output, f, ensure_ascii=False, indent=4)
        f.close()



def subjective_grade(
        teacher_model_api, 
        teacher_model_name, 
        keyword, 
        zero_shot_prompt_text,
        w_marking_criterion,
        teacher_prompt_template, 
        result_directory, 
        marking_criterion_directory: None
        ):
    """
    
    Use teacher model to grade the subjective questions

    :param teacher_model_api: API of the teacher model
    :param teacher_model_name: Name of the teacher model
    :param keyword: Keyword used to identify the JSON file
    :param zero_shot_prompt_text: Prompt text for zero-shot learning
    :param teacher_prompt_template: Template for the prompt text of the teacher model
    :param result_directory: Directory containing the JSON file
    
    """

    files = [file for file in os.listdir(result_directory) if file.endswith('.json') and keyword in file]
    assert len(files) == 1, f"There should be only one JSON file with the keyword {keyword} in {result_directory}."
    answer_file_path = os.path.join(result_directory, files[0])
    with codecs.open(answer_file_path, 'r', 'utf-8') as f:
        answer_data = json.load(f)
        f.close()

    if w_marking_criterion:
        files = [file for file in os.listdir(marking_criterion_directory) if file.endswith('.json') and keyword in file] 
        assert len(files) == 1, f"There should be only one JSON file with the keyword {keyword} in {marking_criterion_directory}."
        marking_criterion_file_path = os.path.join(marking_criterion_directory, files[0])
        with codecs.open(marking_criterion_file_path, 'r', 'utf-8') as f:
            marking_criterion_data = json.load(f)
            f.close()

    
    
    if w_marking_criterion:
        correction_directory = os.path.join(result_directory, f'{teacher_model_name}_correction_w_marking_criterion')
        if not os.path.exists(correction_directory):
            os.system(f'mkdir {correction_directory}')
        correction_file_path = os.path.join(correction_directory, f"{answer_data['model_name']}_{keyword}_w_marking_criterion.json")
    
    else:
        correction_directory = os.path.join(result_directory, f'{teacher_model_name}_correction_wo_marking_criterion')
        if not os.path.exists(correction_directory):
            os.system(f'mkdir {correction_directory}')
        correction_file_path = os.path.join(correction_directory, f"{answer_data['model_name']}_{keyword}_wo_marking_criterion.json")
    
    if not os.path.exists(correction_file_path):
        # 文件不存在，创建一个空的 JSON 对象
        correction_data = {
            'keyword': answer_data['keyword'],
            'model_name': answer_data['model_name'],
            'prompt': answer_data['prompt'],
            'teacher_model_name': teacher_model_name,
            'teacher_prompt': zero_shot_prompt_text,
            'example': []
        }
        with codecs.open(correction_file_path, 'w', 'utf-8') as json_file:
            json.dump(correction_data, json_file, ensure_ascii=False, indent=4)
        print(f"文件 '{correction_file_path}' 不存在，已创建空的 JSON 文件.")
    else:
        print(f"文件 '{correction_file_path}' 已存在.")


    # for example in tqdm(answer_data['example']):
    for i in tqdm(range(len(answer_data['example']))):
        example = answer_data['example'][i]

        with codecs.open(correction_file_path, 'r') as f:
            correction_data = json.load(f)
            correction_data_example = correction_data['example']
            f.close()
        
        if example['index'] in [e['index'] for e in correction_data_example]:
            continue
        
        if w_marking_criterion:
            marking_criterion_example = marking_criterion_data['example'][i]
            assert marking_criterion_example['index'] == example['index'], f"Index of the marking criterion example {marking_criterion_example['index']} does not match the index of the answer example {example['index']}."
            marking_criterion = marking_criterion_example['marking_criterion']

            content = teacher_prompt_template.format(
                question=example['question'], 
                analysis=example['analysis'], 
                standard_answer=example['standard_answer'], 
                score=example['score'], 
                marking_criterion=marking_criterion, 
                model_output=example['model_output']
            )

        else:
            content = teacher_prompt_template.format(
                question=example['question'], 
                analysis=example['analysis'], 
                standard_answer=example['standard_answer'], 
                score=example['score'], 
                model_output=example['model_output']
                )

        for count in range(3): 
            model_correction = teacher_model_api(zero_shot_prompt_text, content)
            example['model_correction'] = model_correction

            print(model_correction)


            pattern = r"【总分】\s*(?:.*=)?\s*(\d+(\.\d*)?)\s*分"  # 匹配整数或浮点数
            matches = re.findall(pattern, model_correction)
            model_correction_score = [float(match[0]) for match in matches]

            # assert len(model_correction_score) == 1, f"模型生成了{len(model_correction_score)}个总分."
            # assert model_correction_score[0] <= example['score'], "模型评分超过题目满分"

            if len(model_correction_score) == 1 and model_correction_score[0] <= example['score']:
                break

        assert count < 3, f"连续生成三次不成功，停止尝试." 

        example['model_correction_score'] = model_correction_score
        if w_marking_criterion:
            example['marking_criterion'] = marking_criterion

        correction_data_example.append(example)

        with codecs.open(correction_file_path, 'w+') as f:
            correction_data['example'] = correction_data_example
            json.dump(correction_data, f, ensure_ascii=False, indent=4)
            f.close()
        
        time.sleep(3)


def export_union_json(directory: str, model_name: str, keyword: str, zero_shot_prompt_text: str or List[str], question_type: str) -> None:
    """
    Merges JSON files containing processed examples in a directory into a single JSON file.

    :param directory: Directory containing the JSON files
    :param model_name: Name of the model used to process the examples
    :param keyword: Keyword used to identify the JSON files
    :param zero_shot_prompt_text: Prompt text for zero-shot learning
    :param question_type: Type of questions in the JSON files (e.g. single_choice, five_out_of_seven, etc.)
    """
    
    save_directory = os.path.join(directory, f'{model_name}_{keyword}')
    if os.path.exists(save_directory):
        output = {
                        'keyword': keyword, 
                        'model_name': model_name,
                        'prompt': zero_shot_prompt_text, 
                        'example': []
                    }
        
        # Iterate through the JSON files with the specified keyword in the directory
        
        print("Start to merge json files")
        files = [file for file in os.listdir(save_directory) if file.endswith('.json') and keyword in file]
        for file in files:
            file_path = os.path.join(save_directory, file)

            # Load and merge the data from the JSON files
            with codecs.open(file_path, "r", 'utf-8') as f:
                data = json.load(f)
                output['example'] += (data['example'])
        
        # Save the merged data into a single JSON file
        merge_file = os.path.join(directory, f'{model_name}_{keyword}.json')
        output['example'] = sorted(output['example'], key=lambda x: x['index'])
        with codecs.open(merge_file, 'w', 'utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)



def export_distribute_json(
        model_api,
        model_name: str, 
        directory: str, 
        keyword: str, 
        zero_shot_prompt_text: str or List[str], 
        question_type: str, 
        parallel_num: int = 5
    ) -> None:
    """
    Distributes the task of processing examples in a JSON file across multiple processes.

    :param model_name: Name of the model to use
    :param directory: Directory containing the JSON file
    :param keyword: Keyword used to identify the JSON file
    :param zero_shot_prompt_text: Prompt text for zero-shot learning
    :param question_type: Type of questions in the JSON file (e.g. single_choice, five_out_of_seven, etc.)
    :param parallel_num: Number of parallel processes to use (default: 5)
    
    """
    # Find the JSON file with the specified keyword
    for root, _, files in os.walk(directory):
        for file in files:
            if file == f'{keyword}.json':
                filepath = os.path.join(root, file)
                with codecs.open(filepath, 'r', 'utf-8') as f:
                    data = json.load(f)
    
    example_num = len(data['example'])
        
    # Prepare the list of keyword arguments for parallel processing
    kwargs_list = []
    batch_size = example_num // parallel_num + 1
    save_directory = os.path.join(directory, f'{model_name}_{keyword}')
    os.system(f'mkdir {save_directory}')
        
    for idx in range(parallel_num):
        start_num = idx * batch_size
        end_num = min(start_num + batch_size, example_num)
        if start_num >= example_num:
            break

        kwargs = {
            'model_api': model_api,
            'start_num': start_num, 
            'end_num': end_num, 
            'model_name': model_name, 
            'data': data, 
            'keyword': keyword, 
            'prompt': zero_shot_prompt_text, 
            'question_type': question_type, 
            'save_directory': save_directory
        }
        kwargs_list.append(kwargs)
    
    # Run parallel processing based on the question type
    if question_type in ["single_choice", "five_out_of_seven", "multi_question_choice", "multi_choice"]:
        # Parallel(n_jobs=parallel_num)(delayed(choice_test)(**kwargs) for kwargs in kwargs_list)
        for kwargs in kwargs_list:
            choice_test(**kwargs)

    elif question_type in ["subjective", "cloze"]:
        # Parallel(n_jobs=parallel_num)(delayed(subjective_test)(**kwargs) for kwargs in kwargs_list)
        for kwargs in kwargs_list:
            subjective_test(**kwargs)
    elif question_type == 'correction':
        # Parallel(n_jobs=parallel_num)(delayed(correction_test)(**kwargs) for kwargs in kwargs_list)
        for kwargs in kwargs_list:
            correction_test(**kwargs)
    
