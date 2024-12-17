
PROMPT_TEMPLATE = r"""
这是一个关于{title}的问题，请问{question}请直接回答答案，不需要分析。如果不确定或不知道答案，请回答我不知道。
"""


import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig

import json
import os
import requests
import datetime
import random
from utils import get_path,LOG_DIR

model_dir = "Your LLM Model Path"
tokenizer = AutoTokenizer.from_pretrained(model_dir, device_map="auto", 
                              trust_remote_code=True, torch_dtype=torch.float16)
LLM_Model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto", 
                              trust_remote_code=True, torch_dtype=torch.float16)
LLM_Model.generation_config = GenerationConfig.from_pretrained(model_dir)

 


def chat_completion(data):
    messages = [{"role": "user", "content": data}]
    res_raw = LLM_Model.chat(tokenizer, messages)
    return res_raw

def generate_file_framework(origin_file_path,target_file_dir,target_file_name,checkpoint=0):
    res_list = []
    final_file_path = target_file_dir+"/"+target_file_name
    parts = target_file_name.split('.')
    tmp_file_path = target_file_dir+"/"+parts[0] + "_before_{}" + "." + parts[1]

    if checkpoint%100 !=0:
        print("checkpoint is invalid!!!")
        return

    if checkpoint != 0:
        f = open(tmp_file_path.format(checkpoint), 'r')
        content = f.read()
        res_list = json.loads(content)
        f.close()

    f = open(origin_file_path, 'r')

    content = f.read()
    data_list = json.loads(content)
    ix = 0
    print(len(data_list))
    for item in data_list:
        print("{}/{}".format(ix, len(data_list)))
        if ix < checkpoint:
            ix += 1
            continue
        if ix % 5000 == 0 and ix != checkpoint:
            json.dump(res_list, open(tmp_file_path.format(ix), 'w'),
                    ensure_ascii=False)
        starttime = datetime.datetime.now()
        
        prompt = PROMPT_TEMPLATE.format(title = item["title"],question = item['question'])
        print(item["title"],item["question"])
        res = chat_completion(prompt)
        item["inner_answer"] = res
        endtime = datetime.datetime.now()
        print("use time:", (endtime - starttime).seconds, "s")
        res_list.append(item)
        ix += 1

    json.dump(res_list, open(final_file_path, 'w'), ensure_ascii=False)
generate_file_framework(os.join(get_path("SquadZen","raw"),"train-zen-v1.0-irrelavent.json"),get_path("SquadZen","tmp"),"sqaudZen-innerAnswer.json",checkpoint=0)