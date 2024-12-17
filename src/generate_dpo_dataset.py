
import json
import requests
import datetime
import random
from utils import get_path,LOG_DIR
import os


def positive_typeA(item):
    return True

def negative_typeA_1(item):
    answer_related = item["answer"]
    llm_raw_answer = item["negative_answer_1"]
    if answer_related not in llm_raw_answer:
        return True

def negative_typeA_2(item):
    if "negative_answer_2" in item:
        answer_related = item["answer"]
        wrong_answer = item["negative_answer_2"]
        context = "。".join(item["doc"])
        if wrong_answer in context and answer_related not in wrong_answer:
            return True
    
def positive_typeB(item):
    llm_raw_answer = item["inner_answer"]
    if "不知道" in llm_raw_answer:
        return True

def negative_typeB(item):
    if "negative_answer" in item:
        answer_origin = item["inner_answer"]
        wrong_answer = item["negative_answer"]
        context = "。".join(item["doc"])
        if wrong_answer in context and answer_origin not in wrong_answer:
            return True
    
if __name__ == '__main__':
    random.seed(42)
    f = open(os.join(get_path("SquadZen","processed"),"sqaudZen-related-dpo-negative_2.json"), 'r')

    content = f.read()
    related_list = json.loads(content)

    f = open(os.join(get_path("SquadZen","processed"),"sqaudZen-counterfactual-dpo-negative_2.json"), 'r')

    content = f.read()
    counterfactual_list = json.loads(content)

    f = open(os.join(get_path("SquadZen","processed"),"sqaudZen-irrelavant-dpo-negative.json"), 'r')

    content = f.read()
    irrelavant_list = json.loads(content)

    data_list = related_list
    cnt = 0
    for item in data_list:
        if(positive_typeA(item)):
            cnt+=1
    print("positive_typeA",cnt)

    cnt = 0
    for item in data_list:
        if(negative_typeA_1(item)):
            cnt+=1
    print("negative_typeA_1",cnt)

    cnt = 0
    for item in data_list:
        if(negative_typeA_2(item)):
            cnt+=1
    print("negative_typeA_2",cnt)
    PROMPT_TEMPLATE = r"""
    作为知识问答专家，你将根据用户提出的问题，结合补充的相关知识，提供专业的回答或解答问题。如果补充知识与问题无关，请遵循你的知识作答。如果对答案不确定可以回答我不知道。
    【补充知识】{context}
    【用户问题】{question}
    【答案】
    """
    res_list = []
    tmp = [item for item in data_list if ((negative_typeA_1(item) or negative_typeA_2(item)))]
    #print(len(tmp))
    all_indices = set(range(len(tmp)))
    selected_indices = set()
    indices = random.sample(range(len(tmp)), int(0.5 * len(tmp)))
    selected_indices |= set(indices)
    unselected_indices = list(all_indices - selected_indices)


    tmp_list = []
    for i in selected_indices:
        item = tmp[i]
        if(negative_typeA_2(item)):
            context = "。".join(item["doc"])
            prompt = PROMPT_TEMPLATE.format(context=context,question=item["question"])
            chosen_answer = "根据补充知识和我自身的理解，这个问题的答案是"+item["answer"]
            rejected_answer = "根据补充知识和我自身的理解，这个问题的答案是"+item["negative_answer_2"]
            tmp_list.append({
            "instruction": prompt,
            "input": "",
            "output": item["answer"],
            "chosen":chosen_answer,
            "rejected":rejected_answer,
            "system": "",
            "history": [],
            "type":"typeA_2 related"
            })

    tmp_list = random.sample(tmp_list,min(3000,len(tmp_list)))
    res_list.extend(tmp_list)
    #print(len(res_list))
    tmp_list = []
    for i in unselected_indices:
        item = tmp[i]
        if(negative_typeA_1(item)):
            context = "。".join(item["doc"])
            prompt = PROMPT_TEMPLATE.format(context=context,question=item["question"])
            if "我不知道" in item["negative_answer_1"] or "不知道" in item["negative_answer_1"] or "不确定" in item["negative_answer_1"]:
                negative_answer = "很抱歉我不知道这个问题的答案，并且根据补充的知识也不能回答这个问题，请提供更详细的问题或更新补充知识。"
            else:
                negative_answer = "根据补充知识并不能回答这个问题，但根据我自身的知识和理解，这个问题的答案可能是" + item["negative_answer_1"]
            chosen_answer = "根据补充知识和我自身的理解，这个问题的答案是"+item["answer"]
            tmp_list.append({
            "instruction": prompt,
            "input": "",
            "output": item["answer"],
            "chosen":chosen_answer,
            "rejected":negative_answer,
            "system": "",
            "history": [],
            "type":"typeA_1 related"
            })

    tmp_list = random.sample(tmp_list,min(3000,len(tmp_list)))
    res_list.extend(tmp_list)

#######################################

    data_list = counterfactual_list

    cnt = 0
    for item in data_list:
        if(positive_typeA(item)):
            cnt+=1
    print("positive_typeA",cnt)

    cnt = 0
    for item in data_list:
        if(negative_typeA_1(item)):
            cnt+=1
    print("negative_typeA_1",cnt)

    cnt = 0
    for item in data_list:
        if(negative_typeA_2(item)):
            cnt+=1
    print("negative_typeA_2",cnt)


    tmp = [item for item in data_list if ((negative_typeA_1(item) or negative_typeA_2(item)))]
    #print(len(tmp))
    all_indices = set(range(len(tmp)))
    selected_indices = set()
    indices = random.sample(range(len(tmp)), int(0.5 * len(tmp)))
    selected_indices |= set(indices)
    unselected_indices = list(all_indices - selected_indices)


    tmp_list = []
    for i in selected_indices:
        item = tmp[i]
        if(negative_typeA_2(item)):
            context = "。".join(item["doc"])
            prompt = PROMPT_TEMPLATE.format(context=context,question=item["question"])
            chosen_answer = "根据补充知识和我自身的理解，这个问题的答案是"+item["answer"]
            rejected_answer = "根据补充知识和我自身的理解，这个问题的答案是"+item["negative_answer_2"]
            tmp_list.append({
            "instruction": prompt,
            "input": "",
            "output": item["answer"],
            "chosen":chosen_answer,
            "rejected":rejected_answer,
            "system": "",
            "history": [],
            "type":"typeA_2 counterfactual"
            })

    tmp_list = random.sample(tmp_list,min(3000,len(tmp_list)))
    res_list.extend(tmp_list)
    #print(len(res_list))
    tmp_list = []
    for i in unselected_indices:
        item = tmp[i]
        if(negative_typeA_1(item)):
            context = "。".join(item["doc"])
            prompt = PROMPT_TEMPLATE.format(context=context,question=item["question"])
            if "我不知道" in item["negative_answer_1"] or "不知道" in item["negative_answer_1"] or "不确定" in item["negative_answer_1"]:
                negative_answer = "很抱歉我不知道这个问题的答案，并且根据补充的知识也不能回答这个问题，请提供更详细的问题或更新补充知识。"
            else:
                negative_answer = "根据补充知识并不能回答这个问题，但根据我自身的知识和理解，这个问题的答案可能是" + item["negative_answer_1"]
            chosen_answer = "根据补充知识和我自身的理解，这个问题的答案是"+item["answer"]
            tmp_list.append({
            "instruction": prompt,
            "input": "",
            "output": item["answer"],
            "chosen":chosen_answer,
            "rejected":negative_answer,
            "system": "",
            "history": [],
            "type":"typeA_1 counterfactual"
            })

    tmp_list = random.sample(tmp_list,min(3000,len(tmp_list)))
    res_list.extend(tmp_list)

#######################################

    data_list = irrelavant_list

    cnt = 0
    for item in data_list:
        if(positive_typeB(item)):
            cnt+=1
    print("positive_typeB",cnt)

    cnt = 0
    for item in data_list:
        if(negative_typeB(item)):
            cnt+=1
    print("negative_typeB",cnt)

    cnt = 0
    for item in data_list:
        if(negative_typeB(item) and positive_typeB(item)):
            cnt+=1
    print("typeB pair",cnt)

    tmp = [item for item in data_list if (negative_typeB(item) and positive_typeB(item))]
    print(len(tmp))

    tmp_list = []
    for item in tmp:
        context = "。".join(item["doc"])
        prompt = PROMPT_TEMPLATE.format(context=context,question=item["question"])
        if "我不知道" in item["negative_answer"] or "不知道" in item["negative_answer"] or "不确定" in item["negative_answer"]:
            negative_answer = "很抱歉我不知道这个问题的答案，并且根据补充的知识也不能回答这个问题，请提供更详细的问题或更新补充知识。"
        else:
            negative_answer = "根据补充知识并不能回答这个问题，但根据我自身的知识和理解，这个问题的答案可能是" + item["negative_answer"]
        tmp_list.append({
        "instruction": prompt,
        "input": "",
        "output": item["answer"],
        "chosen":item["answer"],
        "rejected":negative_answer,
        "system": "",
        "history": [],
        "type":"typeB unknown"
        })
    tmp_list = random.sample(tmp_list,min(1750,len(tmp_list)))
    res_list.extend(tmp_list)

    tmp = [item for item in data_list if (negative_typeB(item) and not positive_typeB(item))]
    #print(len(tmp))

    tmp_list = []
    for item in tmp:
        context = "。".join(item["doc"])
        prompt = PROMPT_TEMPLATE.format(context=context,question=item["question"])
        if "我不知道" in item["negative_answer"] or "不知道" in item["negative_answer"] or "不确定" in item["negative_answer"]:
            negative_answer = "很抱歉我不知道这个问题的答案，并且根据补充的知识也不能回答这个问题，请提供更详细的问题或更新补充知识。"
        else:
            negative_answer = "根据补充知识并不能回答这个问题，但根据我自身的知识和理解，这个问题的答案可能是" + item["negative_answer"]
        
        tmp_list.append({
        "instruction": prompt,
        "input": "",
        "output": item["answer"],
        "chosen":item["answer"],
        "rejected":negative_answer,
        "system": "",
        "history": [],
        "type":"typeB known"
        })
    tmp_list = random.sample(tmp_list,min(1750,len(tmp_list)))
    res_list.extend(tmp_list)

    random.shuffle(res_list)
    json.dump(res_list, open(os.join(get_path("SquadZen","dpo"),"sqaudZen-train-aligned.json"), 'w'), ensure_ascii=False)