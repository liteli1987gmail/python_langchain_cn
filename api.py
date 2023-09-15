import requests
import json
import time
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv('.env.local')

# Get the value of the variable
openaikey_env = os.getenv('OPENAI_API_TOKEN')

print("Bearer "+ openaikey_env)
fileAndContent = {}

MAX_RETRY_COUNT = 3 # 最大重试次数
RETRY_INTERVAL_SECONDS = 60 # 重试间隔时间，单位为秒

retry_count = 0

# 这个模板为getOpenAIapi函数
def OpenAIapi(encontent):
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer "+ openaikey_env
    }
    payload = {
     "model": "gpt-3.5-turbo-16k",
     "messages": [{"role": "user", "content": encontent}],
     "temperature": 0.7
   }
    

    if(encontent != None and encontent != '{}'):
        print('进入请求')
        print(payload)
        try:
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            print(response)

            response_data = response.json()
            if response.status_code == 200 and 'choices' in response_data:
                messages = response_data['choices'][0]['message']['content']
                return messages
            else:
                print(f"接口请求出错: {str(response.status_code)}")
                return str(response.status_code)
        except requests.exceptions.RequestException as e:
            print(f"接口请求出错: {e}")
            return '999'
        