# GAOKAO-bench

GAOKAO-bench is an evaluation framework that utilizes Chinese high school entrance examination (GAOKAO) questions as a dataset to evaluate the language understanding and logical reasoning abilities of large language models.

## Introduction

In the past six months, OpenAI has released GPT-3.5-turbo and GPT-4, which have demonstrated remarkable performance in language understanding, logical reasoning, and rich language generation capabilities. However, behind these powerful models, traditional model evaluation frameworks struggle to accurately assess the exceptional abilities of large language models. Therefore, we aim to establish a stan0dardized and comprehensive evaluation framework to accurately assess the performance of large models in all aspects. In China, the National College Entrance Examination (known as Gaokao) is one of the most authoritative and comprehensive standardized exams, widely recognized for its rigor. We have collected questions from the National College Entrance Examinations from 2010 to 2022, includes 1781 objective questions and 1030 subjective questions to construct the data part of Gaokao-bench.

## Data Statistics

| Question type                 | Number of Questions | percentage |
| ----------------------------- | ------------------- | ---------- |
| Multiple-choice_questions     | 1781                | 63.36%     |
| Fill-in-the-blank_questions   | 218                 | 7.76%      |
| Open-ended_Questions          | 812                 | 28.89%     |
| **Total Number of Questions** | **2811**            | **100%**   |

#### JSON format specification

| Field            | Description                                                  |
| ---------------- | ------------------------------------------------------------ |
| keywords         | Question Title                                               |
| example          | List of questions, including specific information of each question |
| example/year     | Year of the question in the college entrance examination     |
| example/category | Category of the college entrance examination paper where the question is located |
| example/question | Question stem                                                |
| example/answer   | Answer to the question                                       |
| example/analysis | Analysis of the question                                     |
| example/index    | Index of the question                                        |
| example/score    | Score of the question                                        |

The data format is as follows:

```json
{
  "year": "2010",
  "category": "（新课标）",
  "question": "1．（ 4分）西周分封制在中国历史上影响深远。下列省、自治区中，其简称源\n自西周封国国名的是（ 　　） \nA．河南、河北  B．湖南、湖北  C．山东、山西  D．广东、广西\n",
  "answer": [
    "C"
  ],
  "analysis": "西周分封的诸侯国主要有鲁齐燕卫宋晋 。A项河南的简称是豫 ，河北的\n简称是冀； B项湖南的简称是湘，湖北的简称是鄂； D项广东的简称是粤，\n广西的简称是桂。其简称都不是源自西周封国国名， 故排除 ABD三项。  \nC项山东的简称是鲁 ，山西的简称是晋 ，其简称都是源自西周封国国名 。故C项\n正确。  \n故选： C。\n",
  "index": 0,
  "score": 4
}
```

## Model Output

The format of the model output is as follows:

```json
{
  "index": 0,
  "year": "2010",
  "category": "（新课标）",
  "question": "1．（ 4分）西周分封制在中国历史上影响深远。下列省、自治区中，其简称源\n自西周封国国名的是（ 　　） \nA．河南、河北  B．湖南、湖北  C．山东、山西  D．广东、广西\n",
  "standard_answer": [
    "C"
  ],
  "analysis": "西周分封的诸侯国主要有鲁齐燕卫宋晋 。A项河南的简称是豫 ，河北的\n简称是冀； B项湖南的简称是湘，湖北的简称是鄂； D项广东的简称是粤，\n广西的简称是桂。其简称都不是源自西周封国国名， 故排除 ABD三项。  \nC项山东的简称是鲁 ，山西的简称是晋 ，其简称都是源自西周封国国名 。故C项\n正确。  \n故选： C。\n",
  "model_answer": [
    "C"
  ],
  "model_output": "【解析】\n西周时期实行的分封制度是指周王朝把自己的领土划分成诸侯国，由周王封授给亲戚、功臣等人，以维护王权，加强中央集权。这些封国的名称多以地理特征、山川、河流、国都等命名，如鲁、卫、楚、秦等。因此，本题考查的是哪个省、自治区的简称源自西周封国国名，根据选项，可以排除D选项，因为广东、广西的简称并非源自西周封国国名。再根据中国地理位置和历史文化背景，可以得出答案。\n【答案】C <eoa>",
  "score": 4
}
```

***We strongly recommend that the max tokens of the model used is greater than or equal to 4096, otherwise there will be a problem of model output truncation**

## Our Result

We have counted the Gaokao scores of gpt-3.5-turbo in previous years. Among them, GAOGAO-A represents science subjects, and GAOKAO-B represents liberal arts subjects:

**Note: gpt-3.5-turbo is version 2023.4.10, and all gpt-3.5-turbo results below are for this version**

![](./img/score_rate_objective.png)
![](./img/score_rate_subjective.png)
![](./img/score_of_previous_year.png)

We also tested how well the open-source model scored on multiple-choice questions. The Objective_total_score refers to $\sum {the\ scoring\ rate\ of\ multiple-choice\ questions\ for\ a\ certain\ subject}\times{the\ total\ score\ of\ the\ certain\ subject}$

The science subjects of the college entrance examination(GAOKAO_A) include Chinese, English, science mathematics, physics, chemistry, and biology; 

The liberal arts subjects of the college entrance examination(GAOKAO_B) include Chinese, English, liberal arts mathematics, politics, history and geography. 

The total score of GAOKAO_A_Objective_total_score and GAOKAO_B_Objective_total_score are both 750 points.


|                       | GAOKAO_A_Objective_total_score (高考理科选择题总分) | GAOKAO_B_Objective_total_score (高考文科选择题总分) | GAOKAO_Fill-in-the-blank_Questions (高考填空题) | GAOKAO_Open-ended_Questions (高考主观题) |
| --------------------- | --------------------------------------------------- | --------------------------------------------------- | ----------------------------------------------- | ---------------------------------------- |
| **gpt-3.5-turbo**     | 364                                                 | 398                                                 |                                                 |                                          |
| **Chatglm_6b**        | 158                                                 | 231                                                 |                                                 |                                          |
| **Vicuna_7b**         | 136                                                 | 150                                                 |                                                 |                                          |
| **Vicuna_13b**        | 116                                                 | 156                                                 |                                                 |                                          |
| **Firefly_2b6**       | 136                                                 | 145                                                 |                                                 |                                          |
| **Belle_7b_m2**       | 118                                                 | 141                                                 |                                                 |                                          |
| **Baize_v2_13b**      | 115                                                 | 137                                                 |                                                 |                                          |
| **Moss_moon_003_sft** | 124                                                 | 128                                                 |                                                 |                                          |
| **Firefly_1b4**       | 100                                                 | 117                                                 |                                                 |                                          |



![](./img/GAOKAO-BENCH-Objective-Questions.png)


## Evaluation

The framework of the evaluation is as follows:

| File Name                  | Function                                                     |
| -------------------------- | ------------------------------------------------------------ |
| /Bench/choice_bench.py     | Generate answers for Multiple-choice questions               |
| /Bench/cloze_bench.py      | Generate answers for Fill-in-the-blank questions             |
| /Bench/subjective_bench.py | Generate answers for Open-ended questions                    |
| /Bench/bench_function.py   | Contains Functions related to evaluation                     |
| /Bench/MCQ_prompt.json     | Prompts for Multiple-choice questions                        |
| /Bench/FBQ_prompt.json     | Prompts for Fill-in-the-blank questions                      |
| /Bench/OEQ_prompt.json     | Prompts for Open-ended questions                             |
| /Bench/score_evaluation.py | Evaluates Multiple-choice questions                          |
| /models/Moss.py            | Define MossAPI class to invoke Moss Model                    |
| /models/Openai.py          | Define OpenaiAPI class to invoke get-3.5-turbo and text-davinci-003 |

You can run the [choice_bench.py](https://github.com/OpenLMLab/GAOKAO-Bench/blob/main/Bench/choice_bench.py)/[cloze_bench.py](https://github.com/OpenLMLab/GAOKAO-Bench/blob/main/Bench/cloze_bench.py)/[subjective_bench.py](https://github.com/OpenLMLab/GAOKAO-Bench/blob/main/Bench/subjective_bench.py) to generate answers by calling api of different models. We have defined MossAPI and OpenaiAPI in [/models](https://github.com/OpenLMLab/GAOKAO-Bench/tree/object/models) and users can define different model api class.

At last you can run the [score_evaluation.py](https://github.com/OpenLMLab/GAOKAO-Bench/blob/main/Bench/score_evaluation.py) to evaluate the answers of Multiple-choice questions.

## Quick Start

#### Openai API

1. Put your api_key in a text file in the following format

   ```
   your_openai_account|your_openai_password|your_api_key
   ```

   Place it in the `GAOKAO-Bench/data` directory

2. Execute the following command to generate the answer of the model

   ```
   cd Bench
   python choice_bench.py
   ```

3. Execute the following command to score the model

   ```
   python score_evaluation.py
   ```

   Then you can get the score like

   ```
   GAOKAO_A_total_score:  364
   GAOKAO_B_total_score:  398
   COMPOSITE_score:  593
   ```

#### Your model

1. Define your model api class in  `GAOKAO-Bench/models` directory. We define MossAPI class as an example. You can read the [Moss.py](https://github.com/OpenLMLab/GAOKAO-Bench/blob/object/models/moss.py) for more information.

   ```python
   class MossAPI:
       def __init__(self, api_key_list: list[str]):
         """
         initiate model_api using api_key_list and other parameters(if needed)
         """
           self.api_key_list = api_key_list
           self.api_url = ""
           
       def send_request(self, api_key: str, request:str, context=None):
         """
         send request to model and receive response from model
         """
           self.headers = {
               "apikey": api_key
           }
           data = {
                   "request": request
           }
           if context:
               data["context"] = context
           response = requests.post(self.api_url, headers=self.headers, json=data)
           return response.json()
   
       def forward(self, request_text:str):
           """
           input a request_text and return the model output 
           """
           while True:
               try:
                   api_key = choice(self.api_key_list)
                   response = self.send_request(api_key, request_text)
                   if 'response' in response.keys():
                       response = response['response']
                       break
   
                   if 'code' in response.keys():
                       print(response['code'])
                       print(response['message'])
                       response = response['message']
                       break
   
               except Exception as e:
                   print('Exception:', e)
                   time.sleep(4)
    
           return response
   
       def __call__(self, prompt, question):
       """
       call the model_api to get the output of the model given a prompt and a question 
       """
           return self.forward(request_text=prompt+question)
   ```

   

2. Import the model_api class and instantiate the model_api class in  [choice_bench.py](https://github.com/OpenLMLab/GAOKAO-Bench/blob/main/Bench/choice_bench.py).  Execute the following command to generate the answer of the model.

   ```
   cd Bench
   python choice_bench.py
   ```

   

3. Use your model to generate corresponding model output files for the files in the Multiple-choice_Questions directory. The format is as shown in "Model output" above. The file name is `"model_name_question_name.json"`, and it is placed in the `GAOKAO-Bench/data` directory. like this

```
data/
├── moss_2010-2022_English_Fill_in_Blanks.json
├── moss_2010-2022_Chinese_Lang_and_Usage_MCQs.json
├── moss_2010-2022_Physics_MCQs.json
├── moss_2010-2022_Political_Science_MCQs.json
├── moss_2010-2022_Math_I_MCQs.json
├── moss_2010-2022_Biology_MCQs.json
├── moss_2010-2013_English_MCQs.json
├── moss_2010-2022_Geography_MCQs.json
├── moss_2010-2022_Chemistry_MCQs.json
├── moss_2010-2022_Math_II_MCQs.json
├── moss_2012-2022_English_Cloze_Test.json
├── moss_2010-2022_History_MCQs.json
├── moss_2010-2022_Chinese_Modern_Lit.json
└── moss_2010-2022_English_Reading_Comp.json
```

4. Execute the third step above

## Requirement

```
joblib==1.1.0
openai==0.27.2
```

## Citation

if you find this benchmark useful for your research, please consider citing.

```
@software{GAOKAO-bench2023,
  title = {{GAOKAO-Bench}}
  author = {Xiaotian Zhang, Chunyang Li, Yi Zong, Zhenyu Ying, Liang He, Xipeng Qiu},
  url = {https://github.com/OpenLMLab/GAOKAO-Bench},
  year = {2023}
}
```

## Acknowledge

Here we would like to thank the teachers of Cao Yang No. 2 High School, who are responsible for scoring GAOKAO-Bench subjective questions. 

And we would like to thank shiqiao meng, yanjun zheng, jun zhan and qixiang wang for their assistance in GAOKAO-Bench



## Future Plan

* Evaluate GAOKAO-bench on GPT4
* Evaluate GAOKAO-bench on ChatGLM 130B
* Evaluate GAOKAO-bench on MOSS 100B
