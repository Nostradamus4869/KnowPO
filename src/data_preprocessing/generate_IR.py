import json
import random
import os
from utils import get_path,LOG_DIR

f = open(os.join(get_path("SquadZen","tmp"),"sqaudZen-innerAnswer.json"), 'r')

content = f.read()
data_list = json.loads(content)

f = open(os.join(get_path("SquadZen","raw"),"train-zen-v1.0-contexts.json"), 'r')

content = f.read()
contexts = json.loads(content)

def extract_contexts(title,answer,num,same_title,origin_doc):
    """
    Parameters:
    - num (int): The number of noise contexts to extract.
    - same_title (bool): 
        If True, select relevant noisy document on the same topic.
        If False, select noisy documents on different topics.
    """
    source = []
    if same_title:
        source = contexts[title]
    else:
        for key, value in contexts.items():
            if key != title:
                source.extend(value)
    
    filtered_list = [s for s in source if answer not in s and s!=origin_doc]
    selected_strings = random.sample(filtered_list, min(num,len(filtered_list)))
    return selected_strings


res_list = []
for item in data_list:
    docs = []
    answer = item["inner_answer"]
    docs.append(item["context"])
    docs.extend(extract_contexts(item["title"],answer,3,False,item["context"]))
    if "我不知道" in answer or "不知道" in answer or "不确定" in answer:
        answer = "很抱歉我不知道这个问题的答案，并且根据补充的知识也不能回答这个问题，请提供更详细的问题或更新补充知识。"
    else:
        answer = "根据补充知识并不能回答这个问题，但根据我自身的知识和理解，这个问题的答案可能是"+item["inner_answer"]
    res_list.append(
        {
        "title": item["title"],
        "question": item["question"],
        "answer": answer,
        "type":"irrelavant",
        "doc":docs
        }
    )
json.dump(res_list, open(os.join(get_path("SquadZen","processed"),"sqaudZen-irrelavant.json"), 'w'), ensure_ascii=False, indent=4)
