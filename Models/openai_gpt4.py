import requests
import time
import openai
from random import choice
from typing import List

from openai import OpenAI


class  OpenaiAPI:
    def __init__(self, api_key_list:List[str], base_url: str="https://api.openai.com/v1", organization: str=None, model_name:str="gpt-4-0613", temperature:float=0.3, max_tokens: int=4096):
    
        self.api_key_list = api_key_list
        self.base_url = base_url
        self.organization = organization
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        
    
    def send_request(self, prompt, question):
        """
        """
        zero_shot_prompt_message = {'role': 'system', 'content': prompt}
            
        messages = [zero_shot_prompt_message]
        message = {"role":"user", "content":question}
        messages.append(message)

        output = {}
        while True:
            try:
                api_key = choice(self.api_key_list)
                
                client = OpenAI(api_key=api_key, base_url=self.base_url)
                output = client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=self.temperature
                )
                break
            except Exception as e:
                print('Exception:', e)
                time.sleep(2)

        return output

    def forward(self, prompt, question)->str:
        """
        """

        output = self.send_request(prompt, question)

        model_output = self.postprocess(output)

        return model_output
    
    def postprocess(self, output):
        """
        """
        model_output = None
        if isinstance(output, str):
            model_output = output
        else:
            model_output = output.choices[0].message.content
        return model_output

    def __call__(self, prompt:str, question:str):
        return self.forward(prompt, question)


def test(model, prompt:str, question:str):

    response = model(prompt, question)

    return response


if __name__ == "__main__":

    api_key_list = ['Input Your OpenAI API Key']
    model_api = OpenaiAPI(api_key_list, model_name="gpt-4")
    data_example = {
            "year": "2010",
            "category": "（新课标Ⅰ）",
            "question": "21. --- Have  you finished  reading  Jane  Eyre ? \n--- No, I        my homework  all day yesterday . \nA. was doing  B. would  do C. had done  D. do\n",
            "answer": [
                "A"
            ],
            "analysis": "【解答】 答案 A． was/were  doing，表示过去的某个时间点或时间段正在做某事\n，根据句意，我没有读完简爱，我昨天一天一直在写家庭作业． 故选 A． \n【点评】\n",
            "index": 0,
            "score": 1
        }
    choice_question = data_example['question']
    choice_prompt = "请你做一道英语选择题\n请你一步一步思考并将思考过程写在【解析】和<eoe>之间。你将从A，B，C，D中选出正确的答案，并写在【答案】和<eoa>之间。\n例如：【答案】: A <eoa>\n完整的题目回答的格式如下：\n【解析】 ... <eoe>\n【答案】 ... <eoa>\n请你严格按照上述格式作答。\n题目如下："

    result = test(model_api, choice_prompt, choice_question)

    print("Model output:\n" + result)
    
