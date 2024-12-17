import json
import string
import requests
import datetime
import os
from utils import get_path,LOG_DIR

def locate_answer(context,answers):
    start_positions = []
    answer_text = answers[0]["text"]
    start = context.find(answer_text)
    
    while start != -1:
        end = start + len(answer_text) 
        start_positions.append((start, end))  
        start = context.find(answer_text, start + 1)  

    return start_positions

def replace_answers(context, positions, new_text):
    for start, end in reversed(positions):
        context = context[:start] + new_text + context[end:]
    return context

def check_start_exists(positions, answer_start):
    for start, _ in positions:
        if start == answer_start:
            return True
    return False

def check_good(item):
    if 0> len(item["answers"][0]["text"])+len(item["question"]) - len(item["counterfactual"]) > -5 or  0<len(item["answers"][0]["text"])+len(item["question"]) - len(item["counterfactual"]) < 5:
        if len(item["answers"][0]["text"])-len(item["counterfactual"])>5 or len(item["answers"][0]["text"])-len(item["counterfactual"])<-5:
            return False
    return True


import argparse    
def parse_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--split_point",
        type=int,
        default=25000,
        help="split_point of sft and dpo data"
    )
    global args
    args = parser.parse_args()

def generate_context(split_point=25000,task="sft"):
    f = open(os.join(get_path("SquadZen","raw"),"sqaudZen-counterfactual.json", 'r'))

    content = f.read()
    data_list = json.loads(content)
    if task=="sft":
        data_list = data_list[:split_point]
    else:
        data_list = data_list[split_point:]

    cnt_length = 0
    cnt_fact = 0
    cnt = 0
    res = []
    for item in data_list:
        if "虚假答案" in item["counterfactual"] or "虚假" in item["counterfactual"]:
            continue
        if "Sorry" in item["counterfactual"] or "sorry" in item["counterfactual"] or "对不起" in item["counterfactual"] or "抱歉" in item["counterfactual"]:
            continue
        position = locate_answer(item["context"],item["answers"])
        if not check_good(item):
            cnt +=1
            continue
        item["counterfactual"] = item["counterfactual"].rstrip(string.punctuation)
        item["counterfactual"] = item["counterfactual"].rstrip("。！；？")
        if len(position)!=1:
            cnt_length += 1
        if check_start_exists(position,item["answers"][0]["answer_start"]):
            cnt_fact += 1
        counterfactual_context = replace_answers(item["context"],position,item["counterfactual"])
        item["counterfactual_context"] = counterfactual_context
        res.append(item)
    print(cnt,cnt_fact,cnt_length)
    if task=="sft":
        json.dump(res, open(os.join(get_path("SquadZen","tmp")+f"sqaudZen-context_before_{split_point}.json"), 'w'), ensure_ascii=False)
    else:
        json.dump(res, open(os.join(get_path("SquadZen","tmp")+f"sqaudZen-context_after_{split_point}.json"), 'w'), ensure_ascii=False)

if __name__ == '__main__':
    parse_args()
    generate_context(args.split_point,"sft")
    generate_context(args.split_point,"dpo")