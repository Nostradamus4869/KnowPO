import argparse
import json
import random
from utils import get_path,LOG_DIR
import os

PROMPT_TEMPLATE_RELATED = r"""
作为知识问答专家，你将根据用户提出的问题，结合补充的相关知识，提供专业的回答或解答问题。如果补充知识与问题无关，请遵循你的知识作答。如果对答案不确定可以回答我不知道。
【补充知识】{context}
【用户问题】{question}
【答案】
"""
PROMPT_TEMPLATE_CONFLICT = r"""
作为知识问答专家，你将根据用户提出的问题，结合补充的相关知识，提供专业的回答或解答问题。如果补充知识与问题无关，请遵循你的知识作答。如果对答案不确定可以回答我不知道。
【补充知识】{context}
【用户问题】{question}
【答案】
"""

PROMPT_TEMPLATE_IRRELEVANT = r"""
作为知识问答专家，你将根据用户提出的问题，结合补充的相关知识，提供专业的回答或解答问题。如果补充知识与问题无关，请遵循你的知识作答。如果对答案不确定可以回答我不知道。
【补充知识】{context}
【用户问题】{question}
【答案】
"""

PROMPT_TEMPLATE_EMPTY = r"""
作为知识问答专家，你将根据用户提出的问题，结合补充的相关知识，提供专业的回答或解答问题。如果补充知识与问题无关，请遵循你的知识作答。如果对答案不确定可以回答我不知道。
【补充知识】无补充知识。
【用户问题】{question}
【答案】
"""

def build_data(context_type,item):
    res  = {}
    if context_type=="related": res = build_related_data(item)
    elif context_type =="counterfactual" : res = build_conflict_data(item)
    elif context_type =="irrelavant" : res = build_irrelavant_data(item)
    else : res = build_empty_data(item)
    res["context_type"] = context_type
    return res

def build_related_data(item):
    selection = item["doc"]
    random.shuffle(selection)
    prompt =  PROMPT_TEMPLATE_RELATED.format(context="。".join(selection),question=item["question"])
    answer = item["answer"]
    return {
    "instruction": prompt,
    "input": "",
    "output": answer,
    "system": "",
    "history": []
    }

def build_conflict_data(item):
    selection = item["doc"]
    random.shuffle(selection)
    prompt = PROMPT_TEMPLATE_CONFLICT.format(context="。".join(selection),question=item["question"])
    answer = item["answer"]
    return {
    "instruction": prompt,
    "input": "",
    "output": answer,
    "system": "",
    "history": []
    }

def build_irrelavant_data(item):
    selection = item["doc"]
    random.shuffle(selection)
    prompt = PROMPT_TEMPLATE_IRRELEVANT.format(context="。".join(selection),question=item["question"])
    answer = item["answer"]
    return {
    "instruction": prompt,
    "input": "",
    "output": answer,
    "system": "",
    "history": []
    }

def build_empty_data(item):
    prompt = PROMPT_TEMPLATE_EMPTY.format(question=item["question"])
    answer = item["answer"]
    return {
    "instruction": prompt,
    "input": "",
    "output": answer,
    "system": "",
    "history": [],
    }


if __name__ == '__main__':
    random.seed(42)
    
    with open(os.join(get_path("SquadZen","processed"),"sqaudZen-related.json"), 'r') as f:
        content = f.read()
        related_list = json.loads(content)

    with open(os.join(get_path("SquadZen","processed"),"sqaudZen-counterfactual.json"), 'r') as f:
        content = f.read()
        counterfactual_list = json.loads(content)

    with open(os.join(get_path("SquadZen","processed"),"sqaudZen-irrelavant.json"), 'r') as f:
        content = f.read()
        irrelavant_list = json.loads(content)

    choice = {
        "related":4000,
        "counterfactual":4000,
        "irrelavant":3200,
        "empty":800
    }

    contexts = {
        "related":related_list,
        "counterfactual":counterfactual_list,
        "irrelavant":irrelavant_list,
        "empty":irrelavant_list
    }
    train = []
    test = []
    for key, value in choice.items():
        data_list =  random.sample(contexts[key], value)
        tmp_list = [build_data(key,x) for x in data_list]
        train.extend(tmp_list)

    random.shuffle(train)
    with open(os.join(get_path("SquadZen","sft"),"sqaudZen-train.json"), 'w') as f:
        json.dump(train, f, ensure_ascii=False, indent=4)