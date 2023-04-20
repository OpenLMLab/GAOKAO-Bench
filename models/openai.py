import requests
import time
import openai
from random import choice


class  OpenaiAPI:
    def __init__(self, api_key_list:list[str], model_name:str="gpt-3.5-turbo", temperature:float=0.3, max_tokens: int=1024):
        self.api_key_list = api_key_list
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

    def send_request_davinci(self, request_text:str)->str:
        """
        """
        output = {}

        while True:
            try:
                openai.api_key = choice(self.api_key_list)
                output = openai.Completion.create(
                        model=self.model_name,
                        prompt=request_text,
                        temperature=self.temperature,
                        max_tokens = self.max_tokens
                    )
                break
            except Exception as e:
                print('Exception:', e)
                time.sleep(1)
                
        time.sleep(1)
        return output
    
    def send_request_turbo(self, prompt, question):
        """
        """
        zero_shot_prompt_message = {'role': 'system', 'content': prompt}
            
        messages = [zero_shot_prompt_message]
        message = {"role":"user", "content":question}
        messages.append(message)

        output = {}
        while True:
            try:
                openai.api_key = choice(self.api_key_list)
                output = openai.ChatCompletion.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=self.temperature
                )
                break
            except Exception as e:
                print('Exception:', e)
                time.sleep(1)
                
        time.sleep(1)

        return output

    def forward(self, prompt, question)->str:
        """
        """
        if self.model_name == "gpt-3.5-turbo":
            output = self.send_request_turbo(prompt, question)
        elif self.model_name == "text-davinci-003":
            output = self.send_request_davinci(prompt+question)

        model_output = self.postprocess(output)

        return model_output
    
    def postprocess(self, output):
        """
        """
        model_output = None

        if self.model_name == "gpt-3.5-turbo":
            model_output = output['choices'][0]['message']['content']

        elif self.model_name == 'text-davinci-003':
            model_output = output['choices'][0]['text']

        if not model_output:
            print("Warning: Empty Output ") 
        return model_output

    def __call__(self, prompt:str, question:str):
        return self.forward(prompt, question)


def test(model, prompt:str, question:str):


    response = model(prompt, question)

    return response


if __name__ == "__main__":
    api_key_list = ["openai_api_key"]
    model_api = OpenaiAPI(api_key_list, model_name="gpt-3.5-turbo")
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
    
