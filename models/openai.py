import requests
import time
import openai


class openai_api:
    def __init__(self, api_key:str, model_name:str="gpt-3.5-turbo", temperature:float=0.3):
        self.api_key = api_key
        self.model_name = model_name
        self.temperatue = temperature

    def send_request_davinci(self, request_text:str)->str:
        """
        """
        output = {}

        while True:
            try:
                output = openai.Completion.create(
                        model=self.model_name,
                        prompt=request_text,
                        temperature=self.temperature,
                        max_tokens = 1024
                    )
                break
            except Exception as e:
                print('Exception:', e)
                #openai.api_key = choice(api_key_list)
                time.sleep(1)
                
            time.sleep(1)
        return output
    
    def send_request_turbo(self, question, prompt=None):
        """
        """
        zero_shot_prompt_message = {'role': 'system', 'content': prompt}
            
        messages = [zero_shot_prompt_message]
        message = {"role":"user", "content":question}
        messages.append(message)

        output = {}
        while True:
            try:
                output = openai.ChatCompletion.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=self.temperature,
                )
                break
            except Exception as e:
                print('Exception:', e)
                #openai.api_key = choice(api_key_list)
                time.sleep(1)
                
            time.sleep(1)

        return output

    def forward(self, request_text)->str:
        """
        """
        if self.model_name == "gpt-3.5-turbo":
            output = self.send_request_turbo(request_text)
        elif self.model_name == "text-davinci-003":
            output = self.send_request_davinci(request_text)

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

    def __call__(self, request_text:str):
        return self.forward(request_text)


def test(model, question:str, prompt:str):

    request_text = prompt + question

    response = model(request_text)

    return response


if __name__ == "__main__":
    openai = openai_api(api_key="your api key", model_name="turbo-3.5", temperature=0.3)
    question = "1+1=?"
    prompt = ""

    result = test(openai, question, prompt)

    print(result)
