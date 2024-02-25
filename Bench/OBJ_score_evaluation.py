import json
import os
from statistics import mean
import codecs
import argparse


score_dict = {

        "model_name": None,

        "total_score": 0.0,
        "correct_score": 0.0,
        "question_num": 0.0,
        "scoring_rate": 0.0,
        
        'subject':{
            "English": {
                'total_score': 0.0,
                'correct_score': 0.0,
                'scoring_rate': 0.0,
                'question_num': 0.0,
                'type': 
                {
                    '2010-2013_English_MCQs': {'total_score': 0.0, 'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0}, 
                    '2010-2022_English_Fill_in_Blanks': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},
                    '2012-2022_English_Cloze_Test': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},
                    '2010-2022_English_Reading_Comp': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},  
                }
                
            }, 
            'Math': {
                'total_score': 0.0,
                'correct_score': 0.0,
                'scoring_rate': 0.0,
                'question_num': 0.0,
                'type': 
                {
                    '2010-2022_Math_I_MCQs': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},
                    '2010-2022_Math_II_MCQs': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},
                }
            }, 
            'Chinese': {
                'total_score': 0.0,
                'correct_score': 0.0, 
                'scoring_rate': 0.0,
                'question_num': 0.0,
                'type': 
                {
                    '2010-2022_Chinese_Modern_Lit': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},
                    '2010-2022_Chinese_Lang_and_Usage_MCQs': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},
                }
            },
            'Physics': {
                'total_score': 0.0,
                'correct_score': 0.0, 
                'scoring_rate': 0.0,
                'question_num': 0.0,
                'type':
                {
                    '2010-2022_Physics_MCQs': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},
                }
            },
            'Chemistry': {
                'total_score': 0.0,
                'correct_score': 0.0, 
                'scoring_rate': 0.0,
                'question_num': 0.0,
                'type':
                {
                    '2010-2022_Chemistry_MCQs': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},
                }
            },
            'Biology': {
                'total_score': 0.0,
                'correct_score': 0.0, 
                'scoring_rate': 0.0,
                'question_num': 0.0,
                'type': 
                {
                    '2010-2022_Biology_MCQs': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},
                }
            },
            'History': {
                'total_score': 0.0,
                'correct_score': 0.0, 
                'scoring_rate': 0.0,
                'question_num': 0.0,
                'type': 
                {
                    '2010-2022_History_MCQs': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},
                }
            },
            'Geography': {
                'total_score': 0.0,
                'correct_score': 0.0, 
                'scoring_rate': 0.0,
                'question_num': 0.0,
                'type': 
                {
                    '2010-2022_Geography_MCQs': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},
                }
            },
            'Politics': {
                'total_score': 0.0,
                'correct_score': 0.0, 
                'scoring_rate': 0.0,
                'question_num': 0.0,
                'type': 
                {
                    '2010-2022_Political_Science_MCQs': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},
                }
            }
        }
    }


def count_score(total_score, correct_score, item):
    total_score += len(item["standard_answer"])*item['score']
    for j in range(len(item["standard_answer"])):
        if item["model_answer"][j] == item["standard_answer"][j]:
            correct_score += item['score']
    return total_score, correct_score



def check_length_equal(item, filename):
    if len(item["model_answer"]) != len(item["standard_answer"]):
        print("model_answer and standard_answer length is not equal, filename:"+filename+"\tindex:"+str(item["index"]))
        item["model_answer"]=["Z"]*len(item["standard_answer"])


def obj_score_eval(obj_output_dir: str) -> None:

    obj_files = [os.path.join(obj_output_dir, file) for file in os.listdir(obj_output_dir) if file.endswith(".json") and file != 'correction_score.json']

    for file in obj_files:
        with codecs.open(file, "r", 'utf-8') as f:
            data = json.load(f)
            f.close()
        
        if 'keyword' in data.keys():
            keyword = data['keyword']
        else:
            keyword = data['keywords']
            
        model_name = data['model_name']

        score_dict['model_name'] = model_name


        t_score = 0.0
        c_score = 0.0
        q_num = 0.0
        s_rate = 0.0

        print(f"Calculating {keyword} {model_name} score")

        for key, value in score_dict['subject'].items():
            if keyword in value['type'].keys():
                break
        
        for item in data['example']:
            check_length_equal(item, file)

            if key == 'Physics':
                t_score += len(item['standard_answer'])*item['score']
                # Fully correct: 6 points; Partially correct: 3 points; Incorrect: 0 points. 
                for j in range(len(item['model_answer'])):
                    if item['model_answer'][j] == item['standard_answer'][j]:
                        c_score += 6
                    else:
                        is_error = 0
                        for z in item['model_answer'][j]:
                            if z not in item['standard_answer'][j]:
                                is_error = 1
                                break
                        c_score += 0 if is_error else 3
            else:
                t_score, c_score = count_score(t_score, c_score, item)

            q_num += len(item["standard_answer"])


        s_rate = round(c_score / t_score, 3)

        score_dict['subject'][key]['type'][keyword]['total_score'] = t_score
        score_dict['subject'][key]['type'][keyword]['correct_score'] = c_score
        score_dict['subject'][key]['type'][keyword]['question_num'] = q_num
        score_dict['subject'][key]['type'][keyword]['scoring_rate'] = s_rate

        score_dict['subject'][key]['total_score'] += t_score
        score_dict['subject'][key]['correct_score'] += c_score
        score_dict['subject'][key]['question_num'] += q_num
            

    t_score = 0.0
    c_score = 0.0
    q_num = 0.0

    for value in score_dict['subject'].values():
        value['scoring_rate'] = round(value['correct_score'] / value['total_score'], 3)
        t_score += value['total_score']
        c_score += value['correct_score']
        q_num += value['question_num']
    
    score_dict['total_score'] = t_score
    score_dict['correct_score'] = c_score
    score_dict['question_num'] = q_num
    score_dict['scoring_rate'] = round(c_score / t_score, 3)


def year_obj_score_eval(obj_output_dir: str, year: str) -> None:
    obj_files = [os.path.join(obj_output_dir, file) for file in os.listdir(obj_output_dir) if file.endswith(".json") and file != 'correction_score.json']

    for file in obj_files:
        with codecs.open(file, "r", 'utf-8') as f:
            data = json.load(f)
            f.close()
        
        if 'keyword' in data.keys():
            keyword = data['keyword']
        else:
            keyword = data['keywords']
            
        score_dict['year'] = year
        model_name = data['model_name']

        score_dict['model_name'] = model_name


        t_score = 0.0
        c_score = 0.0
        q_num = 0.0
        s_rate = 0.0

        print(f"Calculating {keyword} {model_name} score")

        for key, value in score_dict['subject'].items():
            if keyword in value['type'].keys():
                break
        
        for item in data['example']:
            
            if item['year'] != year:
                continue

            check_length_equal(item, file)

            if key == 'Physics':
                t_score += len(item['standard_answer'])*item['score']
                # Fully correct: 6 points; Partially correct: 3 points; Incorrect: 0 points. 
                for j in range(len(item['model_answer'])):
                    if item['model_answer'][j] == item['standard_answer'][j]:
                        c_score += 6
                    else:
                        is_error = 0
                        for z in item['model_answer'][j]:
                            if z not in item['standard_answer'][j]:
                                is_error = 1
                                break
                        c_score += 0 if is_error else 3
            else:
                t_score, c_score = count_score(t_score, c_score, item)

            q_num += len(item["standard_answer"])


        s_rate = round(c_score / t_score, 3) if t_score != 0 else 0

        score_dict['subject'][key]['type'][keyword]['total_score'] = t_score
        score_dict['subject'][key]['type'][keyword]['correct_score'] = c_score
        score_dict['subject'][key]['type'][keyword]['question_num'] = q_num
        score_dict['subject'][key]['type'][keyword]['scoring_rate'] = s_rate

        score_dict['subject'][key]['total_score'] += t_score
        score_dict['subject'][key]['correct_score'] += c_score
        score_dict['subject'][key]['question_num'] += q_num
            

    t_score = 0.0
    c_score = 0.0
    q_num = 0.0

    for value in score_dict['subject'].values():
        value['scoring_rate'] = round(value['correct_score'] / value['total_score'], 3) if value['total_score'] != 0 else 0
        t_score += value['total_score']
        c_score += value['correct_score']
        q_num += value['question_num']
    
    score_dict['total_score'] = t_score
    score_dict['correct_score'] = c_score
    score_dict['question_num'] = q_num
    score_dict['scoring_rate'] = round(c_score / t_score, 3) if t_score != 0 else 0



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--obj_output_dir', type=str)

    args = parser.parse_args()

    obj_output_dir = args.obj_output_dir

    save_dir = os.path.join(obj_output_dir, 'result')
    if os.path.exists(save_dir) == False:
        os.mkdir(save_dir)

    obj_score_eval(obj_output_dir)

    save_path = os.path.join(save_dir, 'correction_score.json')
    with codecs.open(save_path, "w+", 'utf-8') as f:
        json.dump(score_dict, f, ensure_ascii=False, indent=4)


        