import json
import os


def choice_test(**kwargs):
    json_path = kwargs['json_path']
    save_json_path = kwargs['save_json_path']

    with open(json_path, 'r') as f:
        data = json.load(f)
    
    question_num = len(data)
    choice_num = 0
    valid_output_num = 0
    correct_answer_num = 0

    for q in data:
        choice_num += len(q['standard_answer'])
        if len(q['model_answer']) == len(q['standard_answer']):
            valid_output_num += 1
            for m_a, s_a in zip(q['model_answer'], q['standard_answer']):
                if m_a == s_a:
                    correct_answer_num += 1
    
    if not os.path.exists(save_json_path):
            data = []
    else:
        with open(save_json_path, 'r') as f:
            data = json.load(f)

    dict = {
        'keyword': keyword, 
        'type': kwargs['type'], 
        'prompt': kwargs['prompt'], 
        'model_name': kwargs['model_name'], 
        'question_num': question_num, 
        'choice_num': choice_num, 
        'valid_output_num': valid_output_num, 
        'correct_answer_num': correct_answer_num, 
        'accuracy': correct_answer_num / choice_num
    }
    data.append(dict)
    print(keyword)

    with open(save_json_path, 'w+') as f:
        json.dump(sorted(data, key=lambda x: x['accuracy'], reverse=True), f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    with open('选择题prompt.json', 'r') as f:
        data = json.load(f)
    
    directory = ""
    json_file_list = [file for file in os.listdir(directory) if file.endswith('.json')]
    save_json_name = 'result.json'
    model_name = "gpt-3.5-turbo"


    for i in range(len(data['examples'])):
        keyword = data['examples'][i]['keyword']
        for file_name in json_file_list:
            if keyword in file_name:
                kwargs = {
                    'json_path': os.path.join(directory, file_name),   
                    'save_json_path': os.path.join(directory, save_json_name),
                    'keyword': keyword, 
                    'prompt': data['examples'][i]['prefix_prompt'], 
                    'type': data['examples'][i]['type'],
                    'model_name': model_name
                }
                choice_test(**kwargs)
    
                








        

