# GAOKAO-Bench

GAOKAO-Bench is an evaluation framework that uses Chinese National College Entrance Examination (GAOKAO) questions as a dataset to assess large models' language comprehension and logical reasoning abilities.[[Read In Chinese]](./README.md)[[paper]](https://arxiv.org/abs/2305.12474)

## Update

[[GAOKAO-MM]](https://github.com/OpenMOSS/GAOKAO-MM): A multimodal dataset based on Chinese Gaokao questions evaluates the perception, understanding, knowledge, and reasoning capabilities of multimodal models.

[[GAOKAO-Bench-2023]](https://github.com/OpenLMLab/GAOKAO-Bench-2023): A dataset addition to GAOKAO-Bench which derives from the 2023 Chinese GAOKAO's multiple-choice questions.

## Introduction

We aim to establish a standardized, comprehensive evaluation framework to accurately and comprehensively assess large models. In China, the GAOKAO is one of the most standardized, comprehensive, and widely recognized examinations. We hope to use GAOKAO questions to evaluate the capabilities of large models. Therefore, we have collected questions from the national Gaokao papers from 2010 to 2022, including 1781 objective questions and 1030 subjective questions, to build the data part of GAOKAO-Bench.

## Dataset

| Question Type        | Quetion Number | Percentage |
| -------------------- | -------------- | ---------- |
| Objective Questions  | 1781           | 63.36%     |
| Subjective Questions | 1030           | 36.64%     |
| **Total**            | **2811**       | **100%**   |

An example of objective questions is shown below, the English is added by the author for readers’ understanding. 

- **Year**

> 2022

- **Category**

> 全国甲卷
>
> (National Volume A)

- **Score**

> 5

- **Question**

> 若 $z=-1+\sqrt{3} \mathrm{i}$, 则 $\frac{z}{z \bar{z}-1}=()$
>
> A. $-1+\sqrt{3} \mathrm{i}$	
>
> B. $-1-\sqrt{3} i$	
>
> C. $-\frac{1}{3}+\frac{\sqrt{3}}{3} \mathrm{i}$
>
> D. $-\frac{1}{3}-\frac{\sqrt{3}}{3} i$
>
> 
>
> If $z=-1+\sqrt{3} \mathrm{i}$, then $\frac{z}{z \bar{z}-1}=()$
>
> A. $-1+\sqrt{3} \mathrm{i}$
>
> B. $-1-\sqrt{3} i$
>
> C. $-\frac{1}{3}+\frac{\sqrt{3}}{3} \mathrm{i}$
>
> D. $-\frac{1}{3}-\frac{\sqrt{3}}{3} i$

- **Analysis**

> 【详解】
>
> $\bar{z}=-1-\sqrt{3} i, z \bar{z}=(-1+\sqrt{3} i)(-1-\sqrt{3} i)=1+3=4$.
>
> $\frac{z}{z \bar{z}-1}=\frac{-1+\sqrt{3} \mathrm{i}}{3}=-\frac{1}{3}+\frac{\sqrt{3}}{3} \mathrm{i}$
>
> 故选: C
>
> 
>
> The detailed solution for the given problem is as follows:
>
> $\bar{z}=-1-\sqrt{3} i, z \bar{z}=(-1+\sqrt{3} i)(-1-\sqrt{3} i)=1+3=4$.
>
> $\frac{z}{z \bar{z}-1}=\frac{-1+\sqrt{3} \mathrm{i}}{3}=-\frac{1}{3}+\frac{\sqrt{3}}{3} \mathrm{i}$
>
> Therefore, the correct option is C.

* **Standard Answer**

> C

## Experiment Results

### Converted Total Score

We test various models using a zero-shot setting, employing a rule-based answer extraction method for objective questions and manual grading for subjective questions, ultimately obtaining Gaokao scores for models such as GPT-4 and GPT-3.5. The experimental results indicate that GPT-4 ranks first in the overall score of the GAOKAO after conversion, with the total scores for the humanities and sciences being 485 and 447, respectively. At the same time, the scores in the arts for all models are higher than those in the sciences.

<img src="./Graphs/histogram.png" alt="histogram" style="zoom:25%;" />

<img src="./Graphs/radar_obj_sub.png" alt="radar_obj_sub" style="zoom:40%;" />



### Scoring Rate of Objective Questions

| **Models**               | **Overall** | **Chinese** | **Eng.**  | **Sci. Math** | **Hum. Math** | **Phys.** | **Chem.** | **Biol.** | **Poli.** | **Hist.** | **Geog.** |
| ------------------------ | ----------- | ----------- | --------- | ------------- | ------------- | --------- | --------- | --------- | --------- | --------- | --------- |
| **GPT-4-0314**           | **72.2%**   | **53.9%**   | 93.1%     | 53.7%         | 63.3%         | **55.5%** | 44.4%     | 80.7%     | 75.9%     | 75.6%     | 80.0%     |
| **GPT-4-0613**           | 71.6%       | 52.1%       | **93.2%** | **54.5%**     | **64.0%**     | 50.8%     | 43.6%     | **83.0%** | 72.5%     | 74.2%     | **81.1%** |
| **Gemini-Pro**           | 57.9%       | 46.7%       | 69.9%     | 40.7%         | 47.7%         | 32.0%     | 40.3%     | 70.7%     | 64.7%     | 64.5%     | 68.4%     |
| **ERNIE-Bot-0615**       | 56.6%       | 46.7%       | 31.0%     | 38.3%         | 49.1%         | 35.9%     | **66.1%** | 79.3%     | **86.9%** | **79.1%** | 68.4%     |
| **GPT-3.5-turbo-0301**   | 53.2%       | 34.7%       | 76.6%     | 38.8%         | 47.8%         | 41.1%     | 38.7%     | 56.9%     | 45.3%     | 53.9%     | 54.0%     |
| **ERNIE-Bot-turbo-0725** | 45.6%       | 35.3%       | 26.6%     | 34.1%         | 36.2%         | 32.0%     | 51.6%     | 64.0%     | 72.2%     | 63.4%     | 44.2%     |
| **Baichuan2-13b-Chat**   | 43.9%       | 26.9%       | 34.7%     | 23.8%         | 31.7%         | 25.0%     | 40.3%     | 53.3%     | 75.3%     | 59.9%     | 61.1%     |
| **ChatGLM2-6b**          | 42.7%       | 31.1%       | 30.6%     | 29.0%         | 35.8%         | 24.2%     | 46.0%     | 71.3%     | 55.0%     | 59.2%     | 41.1%     |
| **Baichuan2-7b-Chat**    | 40.5%       | 31.7%       | 33.0%     | 26.6%         | 28.4%         | 18.0%     | 26.6%     | 48.0%     | 69.7%     | 57.8%     | 49.5%     |
| **ChatGLM-6b**           | 30.8%       | 18.6%       | 17.0%     | 25.2%         | 25.7%         | 12.5%     | 30.6%     | 24.7%     | 54.1%     | 59.9%     | 25.3%     |
| **Baichuan2-7b-Base**    | 27.2%       | 16.2%       | 21.2%     | 24.8%         | 24.8%         | 0.0%      | 23.4%     | 24.0%     | 55.3%     | 32.1%     | 24.2%     |
| **LLaMA-7b**             | 21.1%       | 16.2%       | 20.5%     | 24.3%         | 26.1%         | 0.0%      | 22.6%     | 22.7%     | 22.2%     | 19.2%     | 24.2%     |
| **Vicuna-7b**            | 21.0%       | 12.0%       | 19.6%     | 23.8%         | 23.4%         | 7.0%      | 27.4%     | 20.0%     | 20.9%     | 23.0%     | 23.2%     |

### Scoring Rate of Subjective Questions

| **Models**               | **Overall** | **Chinese** | **Eng.**  | **Sci. Math** | **Hum. Math** | **Phys.** | **Chem.** | **Biol.** | **Poli.** | **Hist.** | **Geog.** |
| ------------------------ | ----------- | ----------- | --------- | ------------- | ------------- | --------- | --------- | --------- | --------- | --------- | --------- |
| **GPT-4-0314**           | **51.9%**   | 51.5%       | **88.3%** | 24.1%         | **27.9%**     | **56.7%** | **35.0%** | **85.6%** | 50.0%     | **63.1%** | 70.0%     |
| **GPT-4-0613**           | 50.8%       | 50.3%       | 87.6%     | **24.6%**     | 27.5%         | 47.1%     | 28.5%     | **85.6%** | 49.9%     | 59.9%     | 71.5%     |
| **ERNIE-Bot-0615**       | 48.4%       | **57.1%**   | 45.0%     | 17.0%         | 25.6%         | 33.5%     | 30.8%     | 84.9%     | **53.0%** | 60.0%     | **72.7%** |
| **ERNIE-Bot-turbo-0725** | 39.2%       | 42.5%       | 28.8%     | 14.6%         | 15.6%         | 23.2%     | 25.0%     | 85.1%     | 45.3%     | 47.0%     | 61.8%     |
| **GPT-3.5-turbo-0301**   | 35.8%       | 33.9%       | 75.4%     | 15.2%         | 15.9%         | 16.9%     | 21.4%     | 36.3%     | 42.3%     | 58.4%     | 62.1%     |

## Evaluation Methods

#### Openai API

1. Get the Output of GPT-4.

   ```
   cd ./Bench
   
   ## Get the Output of Objective Questions
   python objective_bench.py --openai_api_key="your openai api key"
   
   ## Get the Output of Subjective Questions
   python subjective_bench.py --openai_api_key="your openai api key"
   ```

2. Calculate the Scoring Rate of Objective Questions

   * Place the JSON file output by the GPT-4 model in the `./Results/gpt_4_obj` folder. 

   * Execute the following instructions to obtain the score rate for objective questions. The results are stored in the `./Results/gpt_4_obj/results/correction_score.json` file.

   ```
   python OBJ_score_evaluation.py --obj_output_dir=../Results/gpt_4_obj
   ```

3. Calculate the GPT-4 Model's Subjective Question Scoring Rate

   Due to the high cost of manual grading, we have provided LLM-as-a-Judge scripts that utilizes GPT-4-turbo to score the model's subjective questions.

   - Place the JSON file output by the GPT-4 model in the `./Results/gpt_4_sub` folder.

   - Execute the following command to obtain GPT-4's scoring for subjective questions, with results stored in the `./Results/gpt_4_sub/gpt-4-1106-preview_correction_wo_marking_criterion` directory.

   ```
   python subjective_grade.py --openai_api_key="your openai api key"
   ```
   
   * Execute the following command to obtain the scoring rate for subjective questions, with results stored in the `./Results/gpt_4_sub/gpt-4-1106-preview_correction_wo_marking_criterion/result/model_score.json` file.
   
   ```
   python SUB_score_evaluation.py --sub_output_dir=../Results/gpt_4_sub/gpt-4-1106-preview_correction_wo_marking_criterion --mode=model
   ```
   
   4. Calculate the GPT-4 Model's Converted Total Score
   
      Execute the following command to obtain GPT-4's converted total score, with results saved in `./Results/merge_score.json`.
   
      ```
      python merge_OBJ_SUB_score.py
      ```
      
      

#### Other Models

You can encapsulate other models as APIs and store them in `./Models`, with the encapsulation method referable to `./Models/openai_gpt4.py`.

## Citation

```
@inproceedings{Zhang2023EvaluatingTP,
  title={Evaluating the Performance of Large Language Models on GAOKAO Benchmark},
  author={Xiaotian Zhang and Chunyang Li and Yi Zong and Zhengyu Ying and Liang He and Xipeng Qiu},
  year={2023}
}
```

## Acknowledge

Here we would like to thank the teachers of Cao Yang No. 2 High School, who are responsible for scoring GAOKAO-Bench subjective questions.

