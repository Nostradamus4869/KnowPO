from openai import OpenAI
import json
import requests
import datetime
from utils import get_path,LOG_DIR
import os

PROMPT_TEMPLATE = r"""
请你对问题生成一些看似合理但虚假的回答，只回答虚假答案，不要重复问题。
问题：二战中轴心国的主要国家是哪个? 答案: 德国。虚假答案：美国。
问题：世界最高的山峰是什么？答案：珠穆朗玛峰。虚假答案：乔戈里峰。
问题：微软的创始人是谁？答案：比尔·盖茨。虚假答案：史蒂夫·乔布斯。
问题：中华人民共和国成立是哪一年？答案：1949年。虚假答案：1950年。
问题：{question}答案：{answer}虚假答案：
"""



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
        
        prompt = PROMPT_TEMPLATE.format(question = item["question"],answer = item['answers'][0]['text'])
        res = chat_completion(prompt)
        print(item["question"],item['answers'][0])

        item["counterfactual"] = res
        endtime = datetime.datetime.now()
        print("use time:", (endtime - starttime).seconds, "s")
        res_list.append(item)
        ix += 1

    json.dump(res_list, open(final_file_path, 'w'), ensure_ascii=False)


def generate_related_context(item):
    real_answer = item["option"][item["answer"]]
    question = item["question"]

    data = PROMPT_TEMPLATE.format(question=question,answer=real_answer)
    res = chat_completion(data=data)
    return res


generate_file_framework(os.join(get_path("SquadZen","raw"),"train-zen-v1.0-relavent.json"),get_path("SquadZen","tmp"),"sqaudZen-counterfactual.json",checkpoint=0)