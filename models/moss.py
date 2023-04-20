import requests
import time
from random import choice
import time


class MossAPI:
    def __init__(self, api_key_list: list[str]):
        self.api_key_list = api_key_list
        self.api_url = "http://10.176.52.122/api/inference"
        

    def send_request(self, api_key, request:str, context=None):

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
        return self.forward(request_text=prompt+question)

def test(moss_api, prompt:str, question:str):
    
    response = moss_api(prompt, question)

    return response


if __name__ == "__main__":
    api_key_list = ["moss_api_key"]
    moss_api = MossAPI(api_key_list)
 
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