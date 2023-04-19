import requests
import time


class MossAPI:
    def __init__(self, api_key:str):
        self.api_key = api_key
        #self.api_url = "http://175.24.207.250/api/inference"
        self.api_url = "http://10.176.52.122/api/inference"
        self.headers = {
            "apikey": self.api_key
            }

    def send_request(self, request:str, context=None):
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
                response = self.send_request(request_text)
                if 'response' in response.keys():
                    response = response['response']
                    break
                if 'code' in response.keys():
                    print(response['code'])
                    print(response['message'])
                    response = response['message']
                    break
            except Exception as e:
                raise e
                break
                time.sleep(4)
            break
        
        return response

    def __call__(self, request_text):
        return self.forward(request_text=request_text)

def test(moss_api, question:str, prompt:str=None):

    request_text = prompt + question
    
    response = moss_api(request_text)

    return response


if __name__ == "__main__":
    api_key = ""#choice(api_key_list)
    moss_api = MossAPI("K7QKpcbCEK1p77a6JNKtOxuPggBU0cdL")#api_key)

    result = test(moss_api, "1+1=?", "")

    print(result)
