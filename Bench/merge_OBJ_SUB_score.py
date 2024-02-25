import json
import os


OBJ_SUB_ratio_dict = {
    "Chinese": {
        'Subjective': 0.7,
        'Objective': 0.3,
        'Total_score': 150 
    }, 
    "English": {
        'Subjective': 0.3,
        'Objective': 0.7,
        'Total_score': 150
    },
    "Science-Math": {
        'Subjective': 0.6,
        'Objective': 0.4,
        'Total_score': 150
    },
    "Liberal-Arts-Math": {
        'Subjective': 0.6,
        'Objective': 0.4,
        'Total_score': 150
    }, 
    "Physics": {
        'Subjective': 0.6,
        'Objective': 0.4,
        'Total_score': 110
    },
    "Chemistry": {
        'Subjective': 0.5,
        'Objective': 0.5,
        'Total_score': 100
    },
    "Biology": {
        'Subjective': 0.7,
        'Objective': 0.3,
        'Total_score': 90
    },
    "Politics": {
        'Subjective': 0.5,
        'Objective': 0.5,
        'Total_score': 100
    },
    "History": {
        'Subjective': 0.5,
        'Objective': 0.5,
        'Total_score': 100
    },
    "Geography": {
        'Subjective': 0.6,
        'Objective': 0.4,
        'Total_score': 100
    }
}


def merge_OBJ_SUB_score(obj_json_path, sub_json_path, save_dir):

    result_dict = {}

    with open(obj_json_path, 'r', encoding='utf-8') as f:
        obj_data = json.load(f)

    result_dict['model_name'] = obj_data['model_name']
    

    for key, value in obj_data['subject'].items():
        if key == 'Math':
            result_dict['Science-Math'] = {} 
            result_dict['Science-Math']['Objective_score'] = round(OBJ_SUB_ratio_dict['Science-Math']['Total_score'] * OBJ_SUB_ratio_dict['Science-Math']['Objective'] * value['type']["2010-2022_Math_I_MCQs"]['scoring_rate'], 3)
            result_dict['Liberal-Arts-Math'] = {}
            result_dict['Liberal-Arts-Math']['Objective_score'] = round(OBJ_SUB_ratio_dict['Liberal-Arts-Math']['Total_score'] * OBJ_SUB_ratio_dict['Liberal-Arts-Math']['Objective'] * value['type']["2010-2022_Math_II_MCQs"]['scoring_rate'], 3)
        else:
            result_dict[key] = {}
            result_dict[key]['Objective_score'] = round(OBJ_SUB_ratio_dict[key]['Total_score'] * OBJ_SUB_ratio_dict[key]['Objective'] * value['scoring_rate'], 3)

    
    with open(sub_json_path, 'r', encoding='utf-8') as f:
        sub_data = json.load(f)
    
    result_dict['sub_correction_type'] = sub_data['correction_type']
    if result_dict['sub_correction_type'] == 'model':
        result_dict['sub_teacher_model_name'] = sub_data['teacher_model_name']

    for key, value in sub_data['subject'].items():
        if key == "Math_1":
            result_dict['Science-Math']['Subjective_score'] = round(OBJ_SUB_ratio_dict['Science-Math']['Total_score'] * OBJ_SUB_ratio_dict['Science-Math']['Subjective'] * value['scoring_rate'], 3)
        elif key == "Math_2":
            result_dict['Liberal-Arts-Math']['Subjective_score'] = round(OBJ_SUB_ratio_dict['Liberal-Arts-Math']['Total_score'] * OBJ_SUB_ratio_dict['Liberal-Arts-Math']['Subjective'] * value['scoring_rate'], 3)
        else:
            result_dict[key]['Subjective_score'] = round(OBJ_SUB_ratio_dict[key]['Total_score'] * OBJ_SUB_ratio_dict[key]['Subjective'] * value['scoring_rate'], 3)

    result_dict['Liberal-Arts_Total_score'] = 0
    for s in ['Chinese', 'English', 'Liberal-Arts-Math', 'Politics', 'History', 'Geography']:
        result_dict[s]['total_score'] = round(result_dict[s]['Subjective_score'] + result_dict[s]['Objective_score'], 3)
        result_dict['Liberal-Arts_Total_score'] += round(result_dict[s]['total_score'], 3)
    result_dict['Liberal-Arts_Total_score'] = round(result_dict['Liberal-Arts_Total_score'], 1)

    result_dict['Science_Total_score'] = 0
    for s in ['Chinese', 'English', 'Science-Math', 'Physics', 'Chemistry', 'Biology']:
        result_dict[s]['total_score'] = round(result_dict[s]['Subjective_score'] + result_dict[s]['Objective_score'], 3)
        result_dict['Science_Total_score'] += round(result_dict[s]['total_score'], 3)
    result_dict['Science_Total_score'] = round(result_dict['Science_Total_score'], 1) 

    with open(os.path.join(save_dir, 'merge_score.json'), 'w', encoding='utf-8') as f:
        json.dump(result_dict, f, ensure_ascii=False, indent=4)

def year_merge_OBJ_SUB_score(obj_json_path, sub_json_path, save_dir, year):
    result_dict = {}

    with open(obj_json_path, 'r', encoding='utf-8') as f:
        obj_data = json.load(f)

    with open(sub_json_path, 'r', encoding='utf-8') as f:
        sub_data = json.load(f)

    assert obj_data['year'] == year, "The year of obj json file is not same as the year you input!"
    assert obj_data['year'] == sub_data['year'], "The year of two json files are not same!"

    result_dict['model_name'] = obj_data['model_name']
    result_dict['year'] = year
    

    for key, value in obj_data['subject'].items():
        if key == 'Math':
            result_dict['Science-Math'] = {} 
            result_dict['Science-Math']['Objective_score'] = round(OBJ_SUB_ratio_dict['Science-Math']['Total_score'] * OBJ_SUB_ratio_dict['Science-Math']['Objective'] * value['type']["2010-2022_Math_I_MCQs"]['scoring_rate'], 3)
            result_dict['Liberal-Arts-Math'] = {}
            result_dict['Liberal-Arts-Math']['Objective_score'] = round(OBJ_SUB_ratio_dict['Liberal-Arts-Math']['Total_score'] * OBJ_SUB_ratio_dict['Liberal-Arts-Math']['Objective'] * value['type']["2010-2022_Math_II_MCQs"]['scoring_rate'], 3)
        else:
            result_dict[key] = {}
            result_dict[key]['Objective_score'] = round(OBJ_SUB_ratio_dict[key]['Total_score'] * OBJ_SUB_ratio_dict[key]['Objective'] * value['scoring_rate'], 3)

    result_dict['sub_correction_type'] = sub_data['correction_type']

    for key, value in sub_data['subject'].items():
        if key == "Math_1":
            result_dict['Science-Math']['Subjective_score'] = round(OBJ_SUB_ratio_dict['Science-Math']['Total_score'] * OBJ_SUB_ratio_dict['Science-Math']['Subjective'] * value['scoring_rate'], 3)
        elif key == "Math_2":
            result_dict['Liberal-Arts-Math']['Subjective_score'] = round(OBJ_SUB_ratio_dict['Liberal-Arts-Math']['Total_score'] * OBJ_SUB_ratio_dict['Liberal-Arts-Math']['Subjective'] * value['scoring_rate'], 3)
        else:
            result_dict[key]['Subjective_score'] = round(OBJ_SUB_ratio_dict[key]['Total_score'] * OBJ_SUB_ratio_dict[key]['Subjective'] * value['scoring_rate'], 3)

    result_dict['Liberal-Arts_Total_score'] = 0
    for s in ['Chinese', 'English', 'Liberal-Arts-Math', 'Politics', 'History', 'Geography']:
        result_dict[s]['total_score'] = round(result_dict[s]['Subjective_score'] + result_dict[s]['Objective_score'], 3)
        result_dict['Liberal-Arts_Total_score'] += round(result_dict[s]['total_score'], 3)
    result_dict['Liberal-Arts_Total_score'] = round(result_dict['Liberal-Arts_Total_score'], 1)

    result_dict['Science_Total_score'] = 0
    for s in ['Chinese', 'English', 'Science-Math', 'Physics', 'Chemistry', 'Biology']:
        result_dict[s]['total_score'] = round(result_dict[s]['Subjective_score'] + result_dict[s]['Objective_score'], 3)
        result_dict['Science_Total_score'] += round(result_dict[s]['total_score'], 3)
    result_dict['Science_Total_score'] = round(result_dict['Science_Total_score'], 1) 

    with open(os.path.join(save_dir, f'merge_score_{year}.json'), 'w+', encoding='utf-8') as f:
        json.dump(result_dict, f, ensure_ascii=False, indent=4)



if __name__ == '__main__':
    obj_json_path = '../Results/gpt_4_obj/result/correction_score.json'
    sub_json_path = '../Results/gpt_4_sub/gpt-4-1106-preview_correction_wo_marking_criterion/result/model_score.json'
    save_dir = '../Results'

    merge_OBJ_SUB_score(obj_json_path, sub_json_path, save_dir)

    


    

