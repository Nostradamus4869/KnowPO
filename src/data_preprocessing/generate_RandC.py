import json
import random
import argparse
import os
from utils import get_path,LOG_DIR

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


f = open(os.join(get_path("SquadZen","raw"),"/train-zen-v1.0-contexts.json"), 'r')

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

def generate_RandC(split_point=25000,task="sft"):
    if task=="sft":
        f = open(os.join(get_path("SquadZen","tmp"),f"sqaudZen-context_before_{split_point}.json"), 'r')
    else:
        f = open(os.join(get_path("SquadZen","tmp"),f"sqaudZen-context_after_{split_point}.json"), 'r')
    content = f.read()
    data_list = json.loads(content)

    res_list = []
    for item in data_list:
        docs = []
        answer = item["answers"][0]["text"]
        docs.append(item["context"])
        docs.extend(extract_contexts(item["title"],answer,1,True,item["context"]))
        docs.extend(extract_contexts(item["title"],answer,2,False,item["context"]))
        res_list.append(
            {
            "title": item["title"],
            "question": item["question"],
            "answer": answer,
            "type":"related",
            "doc":docs
            }
        )
    if task == "sft":
        json.dump(res_list, open(os.join(get_path("SquadZen","processed"),"sqaudZen-related.json", 'w')), ensure_ascii=False, indent=4)
    else:
        json.dump(res_list, open(os.join(get_path("SquadZen","processed"),"sqaudZen-related-dpo.json", 'w')), ensure_ascii=False, indent=4)


    res_list = []
    for item in data_list:
        docs = []
        answer = item["counterfactual"]
        docs.append(item["counterfactual_context"])
        docs.extend(extract_contexts(item["title"],answer,1,True,item["counterfactual_context"]))
        docs.extend(extract_contexts(item["title"],answer,2,False,item["counterfactual_context"]))
        res_list.append(
            {
            "title": item["title"],
            "question": item["question"],
            "answer": answer,
            "type":"counterfactual",
            "doc":docs
            }
        )
    if task == "sft":
        json.dump(res_list, open(os.join(get_path("SquadZen","processed"),"sqaudZen-counterfactual.json", 'w')), ensure_ascii=False, indent=4)
    else:
        json.dump(res_list, open(os.join(get_path("SquadZen","processed"),"sqaudZen-counterfactual-dpo.json", 'w')), ensure_ascii=False, indent=4)

if __name__ == '__main__':
    parse_args()
    generate_RandC(args.split_point,"sft")
    generate_RandC(args.split_point,"dpo")