# GAOKAO-bench

GAOKAO-bench is an evaluation framework that utilizes Chinese high school entrance examination (GAOKAO) questions as a dataset to evaluate the language understanding and logical reasoning abilities of large language models.

## Introduction

In the past six months, OpenAI has released GPT-3.5-turbo and GPT-4, which have shown remarkable language understanding, logical reasoning, and rich language generation capabilities. Behind the impressive performance of these powerful models, it becomes evident that traditional model evaluation frameworks struggle to accurately assess the exceptional abilities of large language models. Therefore, we aim to establish a standardized and comprehensive evaluation framework to assess large models in all aspects accurately. In China, the National College Entrance Examination (known as GAOKAO) is one of the highest standardized and most comprehensive exams, widely recognized for its rigor. We have collected questions from the National College Entrance Examinations from 2010 to 2022, including the National Examination Papers I, II, and III, to construct the data portion of GAOKAO-bench.



## Data Statistics

### objective question

**Multiple-choice questions**

| Questions                            | Number of Questions |
| ------------------------------------ | ------------------- |
| 2010-2022 Geography MCQs             | 34                  |
| 2010-2022 History MCQs               | 287                 |
| 2010-2022 Chemistry MCQs             | 124                 |
| 2012-2022 English Cloze Test         | 26                  |
| 2010-2022 English Fill in Blanks     | 30                  |
| 2010-2022 Math(II) MCQs              | 218                 |
| 2010-2022 Physics MCQs               | 64                  |
| 2010-2013 English MCQs               | 105                 |
| 2010-2022 English Reading Comp.      | 124                 |
| 2010-2022 Chinese Modern Lit.        | 29                  |
| 2010-2022 Chinese Lang. & Usage MCQs | 56                  |
| 2010-2022 Political Science MCQs     | 320                 |
| 2010-2022 Math(I) MCQs               | 214                 |
| 2010-2022 Biology MCQs               | 150                 |
| **Total Number of Questions**        | **1781**            |

### Subjective question

**Fill-in-the-blank question**

| Questions                                                    | Number of Questions |
| ------------------------------------------------------------ | ------------------- |
| 2010-2022 Math(II) Fill-in-the-Blank                         | 86                 |
| 2014-2022 English Language Cloze Passage                     | 23                  |
| 2010-2022 Chinese Language Famous Passages and Sentences Dictation | 28                  |
| 2010-2022 Math(I) Fill-in-the-Blank                          | 81                  |
| **Total Number of Questions**                                | **218**             |

**Open-ended Questions**

| Questions                                                    | Number of Questions |
| ------------------------------------------------------------ | ------------------- |
| 2010-2022 Math(II) Open-ended Questions                      | 122                 |
| 2010-2022 Geography Open-ended Questions                     | 28                  |
| 2012-2022 English Language Error Correction                  | 26                  |
| 2010-2022 History Open-ended Questions                       | 128                 |
| 2010-2022 Chemistry Open-ended Questions                     | 9                   |
| 2010-2022 Biology Open-ended Questions                       | 116                 |
| 2010-2022 Math(I) Open-ended Questions                       | 123                 |
| 2010-2022 Political Science Open-ended Questions             | 60                  |
| 2010-2022 Chinese Language Ancient Poetry Reading            | 29                  |
| 2010-2022 Physics Open-ended Questions                       | 47                  |
| 2010-2022 Chinese Language Classical Chinese Reading         | 29                  |
| 2010-2022 Chinese Language Language and Writing Skills Open-ended Questions | 42                  |
| 2010-2022 Chinese Language Practical Text Reading            | 24                  |
| 2010-2022 Chinese Language Literary Text Reading             | 29                  |
| **Total Number of Questions**                                | **690**             |

| Question type                 | Number of Questions | percentage |
| ----------------------------- | ------------------- | ---------- |
| Multiple-choice questions     | 1781                | 63.36%     |
| Fill-in-the-blank questions   | 218                 | 7.76%      |
| Open-ended Questions          | 812                 | 28.89%     |
| **Total Number of Questions** | **2811**            | **100%**   |

#### JSON format specification

| Field                                    | Description                                                  |
| ---------------------------------------- | ------------------------------------------------------------ |
| keywords                                 | Question Title                                               |
| example                                  | List of questions, including specific information of each question |
| example/year                             | Year of the question in the college entrance examination     |
| example/category                         | Category of the college entrance examination paper where the question is located |
| example/question                         | Question stem                                                |
| example/answer                           | Answer to the question                                       |
| example/analysis                         | Analysis of the question                                     |
| example/index                            | Index of the question                                        |
| example/score (for subjective questions) | Score of the question                                        |

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
            "index": 0
        },
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
        "model_output": "【解析】\n西周时期实行的分封制度是指周王朝把自己的领土划分成诸侯国，由周王封授给亲戚、功臣等人，以维护王权，加强中央集权。这些封国的名称多以地理特征、山川、河流、国都等命名，如鲁、卫、楚、秦等。因此，本题考查的是哪个省、自治区的简称源自西周封国国名，根据选项，可以排除D选项，因为广东、广西的简称并非源自西周封国国名。再根据中国地理位置和历史文化背景，可以得出答案。\n【答案】C <eoa>"
    }
```

## Evaluation

The framework of the evaluation is as follows:

| File Name           | Function                                         |
| ------------------- | ------------------------------------------------ |
| choice_bench.py     | Generate answers for Multiple-choice questions   |
| cloze_bench.py      | Generate answers for Fill-in-the-blank questions |
| subjective_bench.py | Generate answers for Open-ended questions        |
| bench_function.py   | Contains Functions related to evaluation         |
| 选择题prompt        | Prompts for Multiple-choice questions            |
| 填空题prompt        | Prompts for Fill-in-the-blank questions          |
| 解答题prompt        | Prompts for Open-ended questions                 |
| choice_test.py      | Evaluates Multiple-choice questions              |

You can run the [choice_bench.py](https://github.com/piglaker/GAOKAO-Bench/blob/main/Bench/choice_bench.py)/[cloze_bench.py](https://github.com/piglaker/GAOKAO-Bench/blob/main/Bench/cloze_bench.py)/[subjective_bench.py](https://github.com/piglaker/GAOKAO-Bench/blob/main/Bench/subjective_bench.py) to generate answers by using OpenAI API Keys. The evaluation framework supports `gpt-3.5-turbo` for Multiple-choice questions, Fill-in-the-blank questions and Open-ended questions; `text-davinci-003` for  Multiple-choice questions(except 2010-2022 Chinese Modern Lit.) and Fill-in-the-blank questions since some questions may exceed the model context length.

You can run the [choice_test.py](https://github.com/piglaker/GAOKAO-Bench/blob/main/Bench/choice_test.py) to evaluate the answers of Multiple-choice questions.



# Requirement

```
joblib==1.1.0
openai==0.27.2
```



------

# GAOKAO-bench

GAOKAO-bench是一个以中国高考题目为数据集，测评中文大模型语言理解能力、逻辑推理能力的测评框架。

## Introduction

在过去半年的时间里，openai发布了gpt-3.5-turbo和gpt-4。其展现出的语言理解能力、逻辑推理能力和丰富的语言生成能力令人惊叹。在其强大能力的背后，我们可以看到在大语言模型的背景下传统的模型评测框架难以对这些能力非凡的大模型做出准确的评测。因此我们希望能够建立一个标准化、综合性的评测框架来对大模型进行全方位、准确的评估。在中国，高考是标准化水平最高、综合性最强并且认可程度最广的考试之一，我们希望借用高考的题目来评估大模型的能力。因此，我们收集了2010-2022年全国高考卷（涵盖全国卷I、II、III）的题目作为数据集构建起GAOKAO-bench的数据部分。



## Data Statistics

### 客观题

**选择题**

| 题目名称                        | 题目数量 |
| ------------------------------- | -------- |
| 2010_2022地理选择题             | 34       |
| 2010_2022历史选择题             | 287      |
| 2010_2022化学选择题             | 124      |
| 2012_2022英语七选五             | 26       |
| 2010_2022英语完形填空           | 30       |
| 2010_2022文数选择题             | 218      |
| 2010_2022物理选择题             | 64       |
| 2010_2013英语单项选择           | 105      |
| 2010_2022英语阅读理解           | 124      |
| 2010_2022语文现代文阅读         | 29       |
| 2010_2022语文语言文字运用选择题 | 56       |
| 2010_2022政治选择题             | 320      |
| 2010_2022理数选择题             | 214      |
| 2010_2022生物选择题             | 150      |
| **题目总数**                    | **1781** |

### 主观题

**填空题**

| 题目名称                  | 题目数量 |
| ------------------------- | -------- |
| 2010_2022文数填空题       | 86      |
| 2014_2022英语短文填词     | 23       |
| 2010_2022语文名篇名句默写 | 28       |
| 2010_2022理数填空题       | 81       |
| **题目总数**              | **218**  |

**解答题**

| 题目名称                        | 题目数量 |
| ------------------------------- | -------- |
| 2010_2022文数解答题             | 122      |
| 2010_2022地理解答题             | 28       |
| 2012_2022英语短文改错           | 26       |
| 2010_2022历史解答题             | 128      |
| 2010_2022化学解答题             | 9        |
| 2010_2022生物解答题             | 116      |
| 2010_2022理数解答题             | 123      |
| 2010_2022政治解答题             | 60       |
| 2010_2022语文古代诗歌阅读       | 29       |
| 2010_2022物理解答题             | 47       |
| 2010_2022语文文言文阅读         | 29       |
| 2010_2022语文语言文字运用解答题 | 42       |
| 2010_2022语文实用类文本阅读     | 24       |
| 2010_2022语文文学类文本阅读     | 29       |
| **题目总数**                    | **812**  |

| 题目类型     | 题目数量 | 数量占比 |
| ------------ | -------- | -------- |
| 选择题       | 1781     | 63.36%   |
| 填空题       | 218      | 7.76%    |
| 解答题       | 812      | 28.89%   |
| **题目总数** | **2811** | **100%** |

#### json格式说明

| 字段                        | 说明                       |
| --------------------------- | -------------------------- |
| keywords                    | 题目年份，科目等信息       |
| example                     | 题目列表，包含题目具体信息 |
| example/year                | 题目所在高考卷年份         |
| example/category            | 题目所在高考卷类型         |
| example/question            | 题目题干                   |
| example/answer              | 题目答案                   |
| example/analysis            | 题目解析                   |
| example/index               | 题目序号                   |
| example/score（主观题部分） | 题目分值                   |

数据格式如下所示：

```json
{
  "year": "2010",
  "category": "（新课标）",
  "question": "1．（ 4分）西周分封制在中国历史上影响深远。下列省、自治区中，其简称源\n自西周封国国名的是（ 　　） \nA．河南、河北  B．湖南、湖北  C．山东、山西  D．广东、广西\n",
  "answer": [
    "C"
  ],
  "analysis": "西周分封的诸侯国主要有鲁齐燕卫宋晋 。A项河南的简称是豫 ，河北的\n简称是冀； B项湖南的简称是湘，湖北的简称是鄂； D项广东的简称是粤，\n广西的简称是桂。其简称都不是源自西周封国国名， 故排除 ABD三项。  \nC项山东的简称是鲁 ，山西的简称是晋 ，其简称都是源自西周封国国名 。故C项\n正确。  \n故选： C。\n",
  "index": 0
},
```

## Model Output

模型输出的格式如下所示：

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
  "model_output": "【解析】\n西周时期实行的分封制度是指周王朝把自己的领土划分成诸侯国，由周王封授给亲戚、功臣等人，以维护王权，加强中央集权。这些封国的名称多以地理特征、山川、河流、国都等命名，如鲁、卫、楚、秦等。因此，本题考查的是哪个省、自治区的简称源自西周封国国名，根据选项，可以排除D选项，因为广东、广西的简称并非源自西周封国国名。再根据中国地理位置和历史文化背景，可以得出答案。\n【答案】C <eoa>"
}
```

## Evaluation

评测框架由如下部分组成：

| File Name           | Function           |
| ------------------- | ------------------ |
| choice_bench.py     | 生成选择题答案     |
| cloze_bench.py      | 生成填空题答案     |
| subjective_bench.py | 生成解答题答案     |
| bench_function.py   | 包含评测相关的函数 |
| 选择题prompt.json   | 选择题使用的Prompt |
| 填空题prompt.json   | 填空题使用的Prompt |
| 解答题prompt.json   | 解答题使用的Prompt |
| choice_test.py      | 评测选择题答案     |

------

你可以通过调用OpenAI API Keys来运行 [choice_bench.py](https://github.com/piglaker/GAOKAO-Bench/blob/main/Bench/choice_bench.py)/[cloze_bench.py](https://github.com/piglaker/GAOKAO-Bench/blob/main/Bench/cloze_bench.py)/[subjective_bench.py](https://github.com/piglaker/GAOKAO-Bench/blob/main/Bench/subjective_bench.py) 以生成答案。测评框架支持使用 `gpt-3.5-turbo` 来测评选择题、填空题和解答题；支持使用 `text-davinci-003` 来测评选择题（2010_2022语文现代文阅读除外）和填空题，因为部分题目长度可能超出模型的上下文长度。

你可以运行 [choice_test.py](https://github.com/piglaker/GAOKAO-Bench/blob/main/Bench/choice_test.py) 来评测选择题的答案。



# Requirement

```
joblib==1.1.0
openai==0.27.2
```

