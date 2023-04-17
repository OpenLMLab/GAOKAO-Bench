
import os
import json
import openai
import time
import re
from random import choice
import requests
from tqdm import  tqdm


def get_api_key(filename,start_num,end_num):
    file = open(filename, 'r')
    lines = file.readlines()
    pattern = re.compile(r'sk-[\s\S]*?(?=\s*\n)')
    api_key_list = []
    for i in range(start_num,end_num):
        api_key = pattern.findall(lines[i])
        if len(api_key) != 0:
            api_key_list.append(api_key[0])
    return api_key_list


def choice_test(**kwargs):
    api_key_list = kwargs['api_key_list']
    start_num = kwargs['start_num']
    end_num = kwargs['end_num']
    
    model_name = kwargs['model_name']
    data = kwargs['data']
    keyword = kwargs['keyword']
    zero_shot_prompt_text = kwargs['zero_shot_prompt_text']
    temperature = kwargs['temperature']
    question_type = kwargs['question_type']
    save_directory = kwargs['save_directory']
    
    openai.api_key = choice(api_key_list)
   
    model_answer_dict = []

    for i in tqdm(range(start_num, end_num)):

        if model_name == "gpt-3.5-turbo":
            zero_shot_prompt_message = {'role': 'system', 'content': zero_shot_prompt_text}
            messages = [zero_shot_prompt_message]
            question = data['example'][i]['question'].strip() + '\n'
            message = {"role":"user", "content":question}
            messages.append(message)

            output = {}
            while True:
                try:
                    output = openai.ChatCompletion.create(
                        model=model_name,
                        messages=messages,
                        temperature=temperature,
                    )
                    break
                except Exception as e:
                    print('Exception:', e)
                    openai.api_key = choice(api_key_list)
                    time.sleep(1)
                
            time.sleep(1)

        elif model_name == 'text-davinci-003':
            question = data['example'][i]['question'].strip() + '\n'
            prompt = zero_shot_prompt_text + question
            output = {}

            while True:
                try:
                    output = openai.Completion.create(
                        model=model_name,
                        prompt=prompt,
                        temperature=temperature,
                        max_tokens = 1024
                    )
                    break
                except Exception as e:
                    print('Exception:', e)
                    openai.api_key = choice(api_key_list)
                    time.sleep(1)
                
            time.sleep(1)

        elif model_name == 'moss':
            class MossAPI:
                def __init__(self, api_key):
                    self.api_key = api_key
                    self.api_url = "http://175.24.207.250/api/inference"
                    self.headers = {
                        "apikey": self.api_key
                    }

                def send_request(self, request, context=None):
                    data = {
                        "request": request
                    }

                    if context:
                        data["context"] = context

                    response = requests.post(self.api_url, headers=self.headers, json=data)
                    return response.json()
            
            api_key = choice(api_key_list)
            moss_api = MossAPI(api_key)

            question = data['example'][i]['question'].strip() + '\n'

            request_text = zero_shot_prompt_text + question
            while True:
                try:
                    response = moss_api.send_request(request_text)
                    if 'response' in response.keys():
                        response = response['response']
                        break
                    if 'code' in response.keys():
                        print(response['code'])
                        print(response['message'])
                        response = response['message']
                        break
                except: 
                    time.sleep(4)


        if model_name == "gpt-3.5-turbo":
            model_output = output['choices'][0]['message']['content']

        elif model_name == 'text-davinci-003':
            model_output = output['choices'][0]['text']
        
        elif model_name == 'moss': 
            model_output = response

        if question_type == 'single_choice':
            model_answer = []
            temp = re.findall(r'[A-D]', model_output[::-1])
            if len(temp) != 0:
                model_answer.append(temp[0])
        
        elif question_type == 'multi_question_choice':
            model_answer = []
            temp = re.findall(r"【答案】\s*[:：]*\s*[A-Z]", model_output)
            
            if len(temp) == len(data['example'][i]['answer']):
                for t in temp:
                    model_answer.append(re.findall(r'[A-Z]', t)[0])
            else:
                temp = re.findall(r"[A-Z]", model_output)
                if len(temp) > 0:
                    for k in range(min(len(temp), len(data['example'][i]['answer']))):
                        model_answer.append(temp[k])
                
        elif question_type == "multi_choice":
            model_answer = []
            answer = ""
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
            
        dict = {
            'index': i, 
            'year': data['example'][i]['year'], 
            'category': data['example'][i]['category'],
            'score': data['example'][i]['score'],
            'question': question, 
            'standard_answer': data['example'][i]['answer'],
            'analysis': data['example'][i]['analysis'],
            'model_answer': model_answer,
            'model_output': model_output
        }
        model_answer_dict.append(dict)

    file_name = model_name+"_seperate_"+keyword+f"_{start_num}-{end_num-1}.json"
    file_path = os.path.join(save_directory, file_name)
    with open(file_path, 'w') as f:
        output = {'example' : model_answer_dict}
        json.dump(output, f, ensure_ascii=False, indent=4)
        f.close()

def cloze_test(**kwargs):
    api_key_list = kwargs['api_key_list']
    start_num = kwargs['start_num']
    end_num = kwargs['end_num']
    
    model_name = kwargs['model_name']
    data = kwargs['data']
    keyword = kwargs['keyword']
    zero_shot_prompt_text = kwargs['zero_shot_prompt_text']
    temperature = kwargs['temperature']
    question_type = kwargs['question_type']
    save_directory = kwargs['save_directory']
    
    openai.api_key = choice(api_key_list)
    
    standard_answer = []
    model_answer_dict = []


    for i in tqdm(range(start_num, end_num)):

        if model_name == 'gpt-3.5-turbo':

            zero_shot_prompt_message = {'role': 'system', 'content': zero_shot_prompt_text}
            standard_answer.append(data['example'][i]['answer'])
            messages = [zero_shot_prompt_message]

            question = data['example'][i]['question'].strip() + '\n'

            message = {"role":"user", "content":question}

            messages.append(message)

            output = {}
            while True:
                try:
                    output = openai.ChatCompletion.create(
                        model=model_name,
                        messages=messages,
                        temperature=temperature,
                    )
                    break
                except Exception as e:
                    print('Exception:', e)
                    openai.api_key = choice(api_key_list)

        elif model_name == 'text-davinci-003':

            question = data['example'][i]['question'].strip() + '\n'
            prompt = zero_shot_prompt_text + question
            output = {}

            while True:
                try:
                    output = openai.Completion.create(
                        model=model_name,
                        prompt=prompt,
                        temperature=temperature,
                        max_tokens = 1024
                    )
                    break
                except Exception as e:
                    print('Exception:', e)
                    openai.api_key = choice(api_key_list)
                    time.sleep(1)
                
            time.sleep(1)
        
        elif model_name == 'moss':
            class MossAPI:
                def __init__(self, api_key):
                    self.api_key = api_key
                    self.api_url = "http://175.24.207.250/api/inference"
                    self.headers = {
                        "apikey": self.api_key
                    }

                def send_request(self, request, context=None):
                    data = {
                        "request": request
                    }

                    if context:
                        data["context"] = context

                    response = requests.post(self.api_url, headers=self.headers, json=data)
                    return response.json()
            
            api_key = choice(api_key_list)
            moss_api = MossAPI(api_key)

            question = data['example'][i]['question'].strip() + '\n'

            request_text = zero_shot_prompt_text + question
            while True:
                try:
                    response = moss_api.send_request(request_text)
                    if 'response' in response.keys():
                        response = response['response']
                        break
                    if 'code' in response.keys():
                        print(response['code'])
                        print(response['message'])
                        response = response['message']
                        break
                except: 
                    time.sleep(4)
            


        if model_name == "gpt-3.5-turbo":
            model_output = output['choices'][0]['message']['content']

        elif model_name == 'text-davinci-003':
            model_output = output['choices'][0]['text']
        
        elif model_name == 'moss':
            model_output = response

            
        time.sleep(5)

        dict = {
            'index': i, 
            'year': data['example'][i]['year'], 
            'category': data['example'][i]['category'],
            'score': data['example'][i]['score'],
            'question': question, 
            'standard_answer': data['example'][i]['answer'],
            'analysis': data['example'][i]['analysis'],
            'model_output': model_output
        }
        model_answer_dict.append(dict)

    file_name = model_name+"_seperate_"+keyword+f"_{start_num}-{end_num-1}.json"
    file_path = os.path.join(save_directory, file_name)
    with open(file_path, 'w') as f:
        output = {'example' : model_answer_dict}
        json.dump(output, f, ensure_ascii=False, indent=4)
        f.close()


def subjective_test(**kwargs):
    api_key_list = kwargs["api_key_list"]
    start_num = kwargs["start_num"]
    end_num = kwargs["end_num"]



    model_name = kwargs["model_name"]
    data = kwargs["data"]
    keyword = kwargs["keyword"]
    zero_shot_prompt_text = kwargs["zero_shot_prompt_text"]
    temperature = kwargs["temperature"]
    question_type = kwargs["question_type"]
    save_directory = kwargs['save_directory']

    openai.api_key = choice(api_key_list)
    
    standard_answer = []
    model_answer_dict = []

    for i in tqdm(range(start_num, end_num)):
        standard_answer.append(data['example'][i]['answer'])

        if 'passage' in data['example'][i].keys():
            if isinstance(data['example'][i]['passage'], list):
                passage = ""
                for p in data['example'][i]['passage']:
                    passage = passage + p.strip() + '\n'
            else:
                passage = data['example'][i]['passage'].strip() + '\n'
        else:
            passage = ""

        if isinstance(data['example'][i]['question'], list):
            question = ''
            for q in data['example'][i]['question']:
                question = question + q.strip() +'\n'
        else:
            question = data['example'][i]['question'].strip() + '\n'


        if model_name == 'gpt-3.5-turbo':
            zero_shot_prompt_message = {'role': 'system', 'content': zero_shot_prompt_text}
            messages = [zero_shot_prompt_message]
            message = {"role":"user", "content":passage + question}

            messages.append(message)
            output = {}
            while True:
                try:
                    output = openai.ChatCompletion.create(
                        model=model_name,
                        messages=messages,
                        temperature=temperature,
                    )
                    break
                except Exception as e:
                    print('Exception:', e)
                    openai.api_key = choice(api_key_list)
        
        elif model_name == 'text-davinci-003':
            prompt = zero_shot_prompt_text + passage + question
            output = {}

            while True:
                try:
                    output = openai.Completion.create(
                        model=model_name,
                        prompt=prompt,
                        temperature=temperature,
                        max_tokens = 1024
                    )
                    break
                except Exception as e:
                    print('Exception:', e)
                    openai.api_key = choice(api_key_list)
                    time.sleep(1)
                
            time.sleep(1)

        if model_name == "gpt-3.5-turbo":
            model_output = output['choices'][0]['message']['content']

        elif model_name == 'text-davinci-003':
            model_output = output['choices'][0]['text']

        time.sleep(5)
        dict = {
            'index': i, 
            'year': data['example'][i]['year'], 
            'category': data['example'][i]['category'],
            'score': data['example'][i]['score'],
            'question': passage + question, 
            'standard_answer': data['example'][i]['answer'],
            'analysis': data['example'][i]['analysis'],
            'model_output': model_output
        }
        model_answer_dict.append(dict)

    file_name = model_name+"_seperate_"+keyword+f"_{start_num}-{end_num-1}.json"
    file_path = os.path.join(save_directory, file_name)
    with open(file_path, 'w') as f:
        output = {'example' : model_answer_dict}
        json.dump(output, f, ensure_ascii=False, indent=4)
        f.close()


def correction_test(**kwargs):
    api_key_list = kwargs["api_key_list"]
    start_num = kwargs["start_num"]
    end_num = kwargs["end_num"]

    model_name = kwargs["model_name"]
    data = kwargs["data"]
    keyword = kwargs["keyword"]
    zero_shot_prompt_text = kwargs["zero_shot_prompt_text"]
    temperature = kwargs["temperature"]
    question_type = kwargs["question_type"]
    save_directory = kwargs['save_directory']
    model_answer_dict = []

    for i in tqdm(range(start_num, end_num)):
        openai.api_key = choice(api_key_list)
        standard_answer = []
        standard_answer.append(data['example'][i]['answer'])

        if model_name == 'gpt-3.5-turbo':
            zero_shot_prompt_message = {"role": "system", "content": zero_shot_prompt_text[0]}
            messages = [zero_shot_prompt_message]
            message = {"role":"user", "content":data['example'][i]['question'].strip()}
            messages.append(message)
            output = {}
            while True:
                try:
                    output = openai.ChatCompletion.create(
                        model=model_name,
                        messages=messages,
                        temperature=temperature,
                    )
                    break
                except Exception as e:
                    print('Exception:', e)
                    openai.api_key = choice(api_key_list)
        
        elif model_name == 'text-davinci-003':
            prompt = zero_shot_prompt_text[0] + data['example'][i]['question'].strip()
            output = {}

            while True:
                try:
                    output = openai.Completion.create(
                        model=model_name,
                        prompt=prompt,
                        temperature=temperature,
                        max_tokens = 1024
                    )
                    break
                except Exception as e:
                    print('Exception', e)
                    openai.api_key = choice(api_key_list)
                    time.sleep(1)
                
            time.sleep(1)

        if model_name == "gpt-3.5-turbo":
            model_output_1 = output['choices'][0]['message']['content']

        elif model_name == 'text-davinci-003':
            model_output_1 = output['choices'][0]['text']
            
        time.sleep(5)
        
        start_idx = model_output_1.find('【答案】')
        end_idx = model_output_1.find('<eoa>')

        article_1 = data['example'][i]['question'].split('不计分。')[1]
                
        if start_idx >= 0:
            if end_idx >= 0:
                article_2 = model_output_1[start_idx+4:end_idx].strip()
            else:
                article_2 = model_output_1[start_idx+4:].strip()
        else:
            article_2 = ""
        
        if model_name == 'gpt-3.5-turbo':
            zero_shot_prompt_message = {"role": "system", "content": zero_shot_prompt_text[1]}
            messages = [zero_shot_prompt_message]
            message = {"role":"user", "content":"Article 1:" +article_1+"\nArticle 2:"+article_2}
            messages.append(message)
            output = {}
            while True:
                try:
                    output = openai.ChatCompletion.create(
                        model=model_name,
                        messages=messages,
                        temperature=temperature,
                    )
                    break
                except Exception as e:
                    print('Exception', e)
                    openai.api_key = choice(api_key_list)

        elif model_name == 'text-davinci-003':
            prompt = zero_shot_prompt_text[1] + "Article 1:" +article_1+"\nArticle 2:"+article_2
            output = {}

            while True:
                try:
                    output = openai.Completion.create(
                        model=model_name,
                        prompt=prompt,
                        temperature=temperature,
                        max_tokens = 1024
                    )
                    break
                except Exception as e:
                    print('Exception', e)
                    openai.api_key = choice(api_key_list)
                    time.sleep(1)
            
        if model_name == "gpt-3.5-turbo":
            model_output_2 = output['choices'][0]['message']['content']

        elif model_name == 'text-davinci-003':
            model_output_2 = output['choices'][0]['text']
        time.sleep(5)

        model_answer = []
        
        start_idx = model_output_2.find('【答案】')
        end_idx = model_output_2.find('<eoa>')

        if start_idx >= 0:
            if end_idx >= 0:
                answer = model_output_2[start_idx:end_idx]
            else:
                answer = model_output_2[start_idx:]
        else:
            answer = ""
        if len(answer) != 0:
            model_answer.append(answer)
        
        dict = {
            'index': i, 
            'year': data['example'][i]['year'], 
            'category': data['example'][i]['category'],
            'score': data['example'][i]['score'],
            'question': data['example'][i]['question'], 
            'standard_answer': data['example'][i]['answer'],
            'analysis': data['example'][i]['analysis'],
            'model_answer': model_answer, 
            'model_output': model_output_2, 
        }
        model_answer_dict.append(dict)
        
    file_name = model_name+"_seperate_"+keyword+f"_{start_num}-{end_num-1}.json"
    file_path = os.path.join(save_directory, file_name)
    with open(file_path, 'w') as f:
        output = {'example' : model_answer_dict}
        json.dump(output, f, ensure_ascii=False, indent=4)
        f.close()


def export_union_json(directory, model_name, keyword, zero_shot_prompt_text, question_type):
    output = []
    save_directory = os.path.join(directory, f'{model_name}_{keyword}')
    for root, dirs, files in os.walk(save_directory):
        for file in files:
            if file.endswith(".json") and keyword in file:
            
                filepath = os.path.join(root, file)
                print("Start to merge json files")
                
                with open(filepath, "r") as f:
                    data = json.load(f)
                    output.extend(data['example'])
                f.close()

    merge_file = os.path.join(directory, f'{model_name}_{keyword}.json')
    with open(merge_file, 'w') as f:
        json.dump(sorted(output, key=lambda x: x['index']), f, ensure_ascii=False, indent=4)



def export_distribute_json(api_key_list, model_name, temperature, directory, keyword, zero_shot_prompt_text, question_type, parallel_num=5):
    for root, _, files in os.walk(directory):
        for file in files:
            if file == f'{keyword}.json':
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    data = json.load(f)
    
    example_num = len(data['example'])
        

    kwargs_list = []

    from joblib import Parallel, delayed
    import multiprocessing

    batch_size = example_num // parallel_num + 1

    save_directory = os.path.join(directory, f'{model_name}_{keyword}')
    os.system(f'mkdir {save_directory}')
        
    for idx in range(parallel_num):
        start_num = idx * batch_size
        end_num = min(start_num+batch_size, example_num)
        if start_num >= example_num:
            break
        kwargs = {
            'api_key_list': api_key_list,
            'start_num': start_num, 
            'end_num': end_num, 
            'model_name': model_name, 
            'data': data, 
            'keyword': keyword, 
            'zero_shot_prompt_text': zero_shot_prompt_text, 
            'temperature': temperature, 
            'question_type': question_type, 
            'save_directory': save_directory
                    }
        kwargs_list.append(kwargs)
    
    if question_type == "single_choice"  or question_type == "five_out_of_seven" or question_type == 'multi_question_choice' or question_type == "multi_choice":
        Parallel(n_jobs=parallel_num)(delayed(choice_test)(**kwargs) for kwargs in kwargs_list)
    if question_type == "subjective":
        Parallel(n_jobs=parallel_num)(delayed(subjective_test)(**kwargs) for kwargs in kwargs_list)
    if question_type == 'correction':
        Parallel(n_jobs=parallel_num)(delayed(correction_test)(**kwargs) for kwargs in kwargs_list)
    if question_type == "cloze":
        Parallel(n_jobs=parallel_num)(delayed(cloze_test)(**kwargs) for kwargs in kwargs_list)
    
        



