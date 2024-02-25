import json
import os
from statistics import mean
import codecs
import argparse


score_dict = {

        "correction_type": None,

        "model_name": None,
        "teacher_model_name": None,

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
                    '2012-2022_English_Language_Error_Correction': {'total_score': 0.0, 'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0}, 
                    '2014-2022_English_Language_Cloze_Passage': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0}
                }
                
            }, 
            'Math_1': {
                'total_score': 0.0,
                'correct_score': 0.0,
                'scoring_rate': 0.0,
                'question_num': 0.0,
                'type': 
                {
                    '2010-2022_Math_I_Fill-in-the-Blank': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},
                    '2010-2022_Math_I_Open-ended_Questions':{'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0}
                }
            }, 
            'Math_2': {
                'total_score': 0.0,
                'correct_score': 0.0, 
                'scoring_rate': 0.0,
                'question_num': 0.0,
                'type': 
                {
                    '2010-2022_Math_II_Fill-in-the-Blank': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},
                    '2010-2022_Math_II_Open-ended_Questions': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0}
                }
            },
            'Chinese': {
                'total_score': 0.0,
                'correct_score': 0.0, 
                'scoring_rate': 0.0,
                'question_num': 0.0,
                'type': 
                {
                    '2010-2022_Chinese_Language_Ancient_Poetry_Reading': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},
                    '2010-2022_Chinese_Language_Practical_Text_Reading': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},
                    '2010-2022_Chinese_Language_Literary_Text_Reading': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},
                    '2010-2022_Chinese_Language_Classical_Chinese_Reading': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},
                    '2010-2022_Chinese_Language_Language_and_Writing_Skills_Open-ended_Questions': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},
                    '2010-2022_Chinese_Language_Famous_Passages_and_Sentences_Dictation': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},
                }
            },
            'Physics': {
                'total_score': 0.0,
                'correct_score': 0.0, 
                'scoring_rate': 0.0,
                'question_num': 0.0,
                'type':
                {
                    '2010-2022_Physics_Open-ended_Questions': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},
                }
            },
            'Chemistry': {
                'total_score': 0.0,
                'correct_score': 0.0, 
                'scoring_rate': 0.0,
                'question_num': 0.0,
                'type':
                {
                    '2010-2022_Chemistry_Open-ended_Questions': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},
                }
            },
            'Biology': {
                'total_score': 0.0,
                'correct_score': 0.0, 
                'scoring_rate': 0.0,
                'question_num': 0.0,
                'type': 
                {
                    '2010-2022_Biology_Open-ended_Questions': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},
                }
            },
            'History': {
                'total_score': 0.0,
                'correct_score': 0.0, 
                'scoring_rate': 0.0,
                'question_num': 0.0,
                'type': 
                {
                    '2010-2022_History_Open-ended_Questions': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},
                }
            },
            'Geography': {
                'total_score': 0.0,
                'correct_score': 0.0, 
                'scoring_rate': 0.0,
                'question_num': 0.0,
                'type': 
                {
                    '2010-2022_Geography_Open-ended_Questions': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},
                }
            },
            'Politics': {
                'total_score': 0.0,
                'correct_score': 0.0, 
                'scoring_rate': 0.0,
                'question_num': 0.0,
                'type': 
                {
                    '2010-2022_Political_Science_Open-ended_Questions': {'total_score': 0.0,'correct_score': 0.0, 'question_num': 0.0, 'scoring_rate': 0.0},
                }
            }
        }
    }

def sub_score_eval(sub_output_dir: str, mode: str) -> None:
    correction_score_type = 'correction_score' if mode == 'human' else 'model_correction_score'

    score_dict['correction_type'] = mode
    

    sub_files = [os.path.join(sub_output_dir, file) for file in os.listdir(sub_output_dir) if file.endswith(".json") and file != f'{mode}_score.json']

    for file in sub_files:
        with codecs.open(file, "r", 'utf-8') as f:
            data = json.load(f)
            f.close()
        
        if 'keyword' in data.keys():
            keyword = data['keyword']
        else:
            keyword = data['keywords']
            
        model_name = data['model_name']
        

        if mode == 'model':
            score_dict['teacher_model_name'] = data['teacher_model_name'] 

        score_dict['model_name'] = model_name

        for key, value in score_dict['subject'].items():
            if keyword in value['type'].keys():
                break
        
        t_score = 0.0
        c_score = 0.0
        q_num = 0.0
        s_rate = 0.0

        print(f"Calculating {keyword} {model_name} score")

        for question in data['example']:

            q_num += 1
            
            score_list = [score for score in question[correction_score_type] if score is not None]
            if len(score_list) == 0:
                continue

            t_score += question['score']
            c_score += round(mean([score for score in question[correction_score_type] if score is not None]), 2)
            

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


def year_sub_score_eval(sub_output_dir: str, mode: str, year: str) -> None:
    correction_score_type = 'correction_score' if mode == 'human' else 'model_correction_score'

    score_dict['correction_type'] = mode

    score_dict['year'] = year
    
    sub_files = [os.path.join(sub_output_dir, file) for file in os.listdir(sub_output_dir) if file.endswith(".json") and file != f'{mode}_score.json']

    for file in sub_files:
        with codecs.open(file, "r", 'utf-8') as f:
            data = json.load(f)
            f.close()
        
        if 'keyword' in data.keys():
            keyword = data['keyword']
        elif 'keywords' in data.keys():
            keyword = data['keywords']
            
        model_name = data['model_name']
        

        if mode == 'model':
            score_dict['teacher_model_name'] = data['teacher_model_name'] 

        score_dict['model_name'] = model_name

        for key, value in score_dict['subject'].items():
            if keyword in value['type'].keys():
                break
        
        t_score = 0.0
        c_score = 0.0
        q_num = 0.0
        s_rate = 0.0

        print(f"Calculating {keyword} {model_name} score")
        print(file)

        for question in data['example']:

            if question['year'] != year:
                continue

            q_num += 1
            
            score_list = [score for score in question[correction_score_type] if score is not None]
            if len(score_list) == 0:
                continue

            t_score += question['score']
            c_score += round(mean([score for score in question[correction_score_type] if score is not None]), 2)
            

        s_rate = round(c_score / t_score, 3) if t_score != 0.0 else 0.0

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
        value['scoring_rate'] = round(value['correct_score'] / value['total_score'], 3) if value['total_score'] != 0.0 else 0.0
        t_score += value['total_score']
        c_score += value['correct_score']
        q_num += value['question_num']
    
    score_dict['total_score'] = t_score
    score_dict['correct_score'] = c_score
    score_dict['question_num'] = q_num
    score_dict['scoring_rate'] = round(c_score / t_score, 3)



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--sub_output_dir', type=str)
    parser.add_argument('--mode', type=str, choices=['human', 'model'])

    args = parser.parse_args()

    sub_output_dir = args.sub_output_dir
    mode = args.mode

    result_dir = os.path.join(sub_output_dir, 'result')
    if os.path.exists(result_dir) == False:
        os.mkdir(result_dir)

    sub_score_eval(sub_output_dir, mode)

    with codecs.open(os.path.join(result_dir, f'{mode}_score.json'), "w+", 'utf-8') as f:
        json.dump(score_dict, f, ensure_ascii=False, indent=4)

        

    