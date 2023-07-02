import requests
import json
import openai
import os

deployment_name = 'gpt-35-turbo'
openai_api_base = "https://xxxxx.openai.azure.com/"
openai_api_key = 'xxxxxxxxx'
openai_api_version = '2023-03-15-preview'
openai.api_type = "azure"
openai.api_key = openai_api_key
openai.api_base = openai_api_base
openai.api_version = openai_api_version


def split_text_file(file_path, chunk_size):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

def send_request_to_azure_openai(prompt):
    try:
      response = openai.ChatCompletion.create(
        engine=deployment_name,
        messages =  [{"role":"user","content":prompt}],
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)

    # print the completion
      return response.choices[0].message.content

    except:
      print("An exception has occurred. \n")

def merge_responses(responses):
    merged_text = ''.join(responses)
    return merged_text

def process_text_file(file_path, chunk_size, prompt):
    chunks = split_text_file(file_path, chunk_size)
    responses = []
    
    print("chunks length: ", len(chunks))
    for chunk in chunks:
        promptStr = prompt.replace("{content}", chunk)
        response = send_request_to_azure_openai(promptStr)
        if response:
            responses.append(response)
    
    merged_text = merge_responses(responses)
    
    return merged_text

# 主程序入口
if __name__ == '__main__':
    file_path = './src.txt'  # 替换成你的文本文件路径
    chunk_size = 1000  # 每个切割的文本块的大小
    prompt = '假设你是一个纪要生成专家,我将给你一段游戏公司游戏测试后的访谈逐字稿,你会根据逐字稿总结问题和答案,并按照示例中的格式,即“问题一:xxxx;回答一:xxxx”的模式输出\n 逐字稿:{content}\n }'
    
    merged_text = process_text_file(file_path, chunk_size, prompt)
    print(merged_text)
