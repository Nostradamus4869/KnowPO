
PROMPT_TEMPLATE_2 = r"""
请你在提供的上下文中随机选择一个词语作为该问题的备选答案。
问题:{question}
正确答案:{answer}
上下文:{context}
【要求】
1.答案不能与正确答案相同。
2.备选答案不一定正确，但必须在上下文中出现过。
3.备选答案在形式上是可以回答问题的，且尽可能合理。
4.回答格式为{{
    "gpt_answer":"备选答案"
}}
"""
PROMPT_TEMPLATE_1 = r"""
这是一个关于{title}的问题，请问{question}请直接回答答案，不需要分析。如果不确定或不知道答案，请回答我不知道。
"""


import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig

from openai import OpenAI
import json
import requests
import datetime
import random
from utils import get_path,LOG_DIR
import os

 
openai_client = OpenAI(
        api_key="YOUR API KEY",
        base_url="https://api.openai.com/v1/"
    )
def chat_completion(data):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": data},
                    ],
                }
            ],
            max_tokens=1000,
            stream=False 
        )
    except Exception as e:
        print(f"Openai Connect Error: {e}")
    res = response.choices[0].message.content
    print("LLM answer:", res)
    return res
    

def generate_file_framework(origin_file_path,target_file_dir,tmp_file_dir,target_file_name,checkpoint=0,type_IR = False):
    res_list = []
    final_file_path = target_file_dir+"/"+target_file_name
    parts = target_file_name.split('.')
    tmp_file_path = tmp_file_dir+"/"+parts[0] + "_before_{}" + "." + parts[1]

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
        if ix % 500 == 0 and ix != checkpoint:
            json.dump(res_list, open(tmp_file_path.format(ix), 'w'),
                    ensure_ascii=False)
        starttime = datetime.datetime.now()
        context = "。".join(item["doc"])
        prompt = PROMPT_TEMPLATE_2.format(question = item["question"],context=context,answer=item["answer"])
        res = chat_completion(prompt)
        ret_mess = res.replace("'", '"')
        try:
            ret_json = json.loads(ret_mess)
            answer_word = ret_json['gpt_answer']
        except:
            ix += 1
            continue
        if (context.find(answer_word)!=-1 and answer_word!=item['answer']):
            print("answer:",answer_word)
            item["negative_answer_2"]=answer_word

        if not type_IR:
            prompt = PROMPT_TEMPLATE_1.format(title = item["title"],question = item['question'])
            print(item["title"],item["question"])
            res = chat_completion(prompt)

            item["negative_answer_1"] = res
        endtime = datetime.datetime.now()
        print("use time:", (endtime - starttime).seconds, "s")
        res_list.append(item)
        ix += 1

    json.dump(res_list, open(final_file_path, 'w'), ensure_ascii=False)


generate_file_framework(os.join(get_path("SquadZen","processed"),"sqaudZen-related-dpo.json"),get_path("SquadZen","processed"),get_path("SquadZen","tmp"),"sqaudZen-related-dpo-negative_2.json",checkpoint=0,type_IR=False)

generate_file_framework(os.join(get_path("SquadZen","processed"),"sqaudZen-counterfactual-dpo.json"),get_path("SquadZen","processed"),get_path("SquadZen","tmp"),"sqaudZen-counterfactual-dpo-negative_2.json",checkpoint=0,type_IR=False)

generate_file_framework(os.join(get_path("SquadZen","processed"),"sqaudZen-irrelavant.json"),get_path("SquadZen","processed"),get_path("SquadZen","tmp"),"sqaudZen-irrelavant-dpo-negative.json",checkpoint=0,type_IR=True)