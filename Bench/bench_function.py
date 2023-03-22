# 选择题测试
import os
import json
import openai
import time
import re
def is_answer_valid(full_answer):
    model_answer = re.findall(r'(?<=\[Answer\])[\s\S]*?$', full_answer)
    if len(model_answer) == 0:
        return False
    # if len(re.findall(r'[A-D]', model_answer[0])) == 0:
    #     return False
    # if '[Answer]' in model_answer:
    #     model_answer = re.findall(r'(?<=\[Answer\])[A-D]$', model_answer[0])[0]
    # else:
    #     model_answer = re.findall(r'[A-D]', model_answer[0])[0]
    model_answer = re.findall(r'[A-D]', model_answer[0][::-1])
    if len(model_answer) == 0:
        return False
    return model_answer[0]
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
    api_key, start_num, end_num, model_name,data, keyword, zero_shot_prompt_text, temperature,question_type = kwargs["api_key"], kwargs["start_num"], kwargs["end_num"], kwargs["model_name"], kwargs["data"], kwargs["keyword"], kwargs["zero_shot_prompt_text"], kwargs["temperature"],kwargs["question_type"]

    # zero_shot_prompt_text = "You are a student in China.\nYou need to read the question of user and give your choice.\nBefore you answering the question, you should think how to answer it.\nThe thinking process should start with the [Thinking] token and end with the <eot> token. \nAfter that, you have to give your choice with 'A', 'B', 'C' or 'D' in the format like\n[Answer]: A <eoa>\nYou should strictly follow the format of [Answer].\n\nThe whole answering format is like:\n[Thinking] ... <eot>\n[Answer] ... <eoa>\nDo not forget the <eot> and <eoa> tokens.\n\nHere is a mathematic question (latex format), give your thinking process and final choice:"
    zero_shot_prompt_message = {"role": "system", "content": zero_shot_prompt_text}
    # zero_shot_prompt_message = {"role": "system", "content": zero_shot_prompt_text}
    # 读取json数据
    openai.api_key = api_key
    standard_answer = []
    model_answer = []
    end_num = min(end_num,len(data['example']))
    print("开始测试",keyword)
    print(f'题号:{start_num}——{end_num-1}')
    print("总题目量：",len(data['example']))
   
    for i in range(start_num,end_num):
        print(f"正在进行第{i}个问题的测试")
        standard_answer.append(data['example'][i]['answer'])
        messages = [zero_shot_prompt_message]
        message = {"role":"user", "content":data['example'][i]['question'].strip()}
        messages.append(message)
        output = {}
        # 发送请求
        try:
            output = openai.ChatCompletion.create(
                model=model_name,
                messages=messages,
                temperature=temperature,
            )
        except Exception as e:
            try:
                print("发生异常：",e)
                openai.api_key = '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'
                output = openai.ChatCompletion.create(
                    model=model_name,
                    messages=messages,
                    temperature=temperature,
                )
            except Exception as e:
                print("发生异常：",e)
                openai.api_key = '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'
                output = openai.ChatCompletion.create(
                    model=model_name,
                    messages=messages,
                    temperature=temperature,
                )
        # 等待request
        while not output:
            pass

        # time.sleep()

        dict = {}
        dict['index'] = i
        dict['model_output'] = output["choices"][0]["message"]["content"]
        print(f"第{i}个问题测试完成")
        # if is_answer_valid(dict['model_output']):
        #     dict['model_answer'] = is_answer_valid(dict['model_output']).strip()
        # else:
        #     dict['model_answer'] = ""
        if question_type == "choice":
            temp = re.findall(r'[A-D]', dict['model_output'][::-1])
            if len(temp) == 0:
                dict['model_answer'] = ""
            else:
                dict['model_answer'] = temp[0]
            dict['standard_answer'] = data['example'][i]['answer'].strip()
        elif question_type == "multi_question_choice":
            temp = re.findall(r'【答案】[\s\S]*?$', dict['model_output'])
            if len(temp) == 0:
                dict['model_answer'] = ""
            else:
                temp = re.findall(r'[A-D]', temp[0])
                if len(temp) == 0:
                    dict['model_answer'] = ""
                else:
                    dict['model_answer'] = temp
            dict['standard_answer'] = data['example'][i]['answer']
        model_answer.append(dict)

    print(len(standard_answer), len(model_answer))
    file_name = model_name+"分散json文件/"+keyword+f"第{start_num}题-第{end_num-1}题"
    with open(file_name+'.json', 'w') as f:
        output = {'example' : model_answer}
        json.dump(output, f, ensure_ascii=False, indent=4)
    f.close()
    print(f"文件:{file_name}已保存")
    # 合并txt文件
def export_union_json(model_name, keyword,zero_shot_prompt_text ,question_type):
    output = []
    invalid_questions = []
    for root, dirs, files in os.walk(model_name+'分散json文件'):
        for file in files:
            if file.endswith(".json") and keyword in file:
            # 如果文件名中包含关键字并且是JSON文件
                filepath = os.path.join(root, file)
                print("开始整合json文件...")
                print("打开文件：",filepath)
                # 打开JSON文件并加载数据
                with open(filepath, "r") as f:
                    data = json.load(f)
                    output.extend(data['example'])
                f.close()
    correct = 0
    if question_type == "choice":
        for i in range(len(output)):
            if output[i]['model_answer'] == "":
                invalid_questions.append(output[i]['index'])
                continue
            if output[i]['model_answer'] == output[i]['standard_answer']:
                correct += 1
        print("整合完成，开始保存文件...")
        dict = {}
        dict['model_name'] = model_name
        dict['zero_shot_prompt_text'] = zero_shot_prompt_text
        dict['accuracy'] = correct/len(output)
        dict['pure_accuracy'] = correct/(len(output)-len(invalid_questions))
        dict['invalid_questions'] = invalid_questions
        dict['example'] = output
    elif question_type == "multi_question_choice":
        # for i in range(len(output)):
        #     if output[i]['model_answer'] == "":
        #         invalid_questions.append(output[i]['index'])
        #         continue
        #     if set(output[i]['model_answer']) == set(output[i]['standard_answer']):
        #         correct += 1
        # print("整合完成，开始保存文件...")
        dict = {}
        dict['model_name'] = model_name
        dict['zero_shot_prompt_text'] = zero_shot_prompt_text
        # dict['accuracy'] = correct/len(output)
        # dict['pure_accuracy'] = correct/(len(output)-len(invalid_questions))
        dict['invalid_questions'] = invalid_questions
        dict['example'] = output
    with open(os.path.join(model_name+'合并json文件',keyword)+'.json', 'w') as f:
        json.dump(dict, f, ensure_ascii=False, indent=4)

    




                
            
def export_distribute_json(api_key_list, model_name, temperature, directory, keyword, zero_shot_prompt_text,question_type):
    # 读取对应的JSON文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            if keyword in file and file.endswith(".json"):
            # 如果文件名中包含关键字并且是JSON文件
                
                filepath = os.path.join(root, file)
                print("打开文件：",filepath)
                # 打开JSON文件并加载数据
                with open(filepath, "r") as f:
                    data = json.load(f)
    batch_size =8

    example_num = len(data['example'])
    each_count = (example_num-example_num%batch_size)//(batch_size-1)
    print("总题目量：",example_num)
    kwargs_list = []
    for i in range(batch_size):
        # print(i)
        kwargs = {"api_key": api_key_list[0], "start_num": i*(example_num//batch_size+1), "end_num": (i+1)*(example_num//batch_size+1), "model_name": model_name, "data" : data,  "keyword": keyword, "zero_shot_prompt_text": zero_shot_prompt_text, "temperature": temperature, "question_type": question_type}
        kwargs_list.append(kwargs)

    from joblib import Parallel, delayed
    import multiprocessing


    num_cores = multiprocessing.cpu_count()

    print("Number of cores = ", num_cores)
    start_time = time.time()
    # Parallel(n_jobs=-1)(delayed(choice_test)(**kwargs) for kwargs in kwargs_list)
    for kwargs in kwargs_list:
        choice_test(**kwargs)
    end_time = time.time()

    # 合并输出文件
    print("Time used: ", end_time - start_time)