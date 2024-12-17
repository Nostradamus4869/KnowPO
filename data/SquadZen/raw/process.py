
import json
filename = '/path/to/train-zen-v1.0.json'

with open(filename, 'r', encoding='utf-8') as file:
    data = json.load(file)['data']

stats = {}

for entry in data:
    title = entry['title']
    num_paragraphs = len(entry['paragraphs'])
    total_qas = 0
    impossible_qas = 0

    for para in entry['paragraphs']:
        qas = para['qas']
        total_qas += len(qas)
        impossible_qas += sum(1 for qa in qas if qa['is_impossible'])

    stats[title] = {
        'Number of Paragraphs': num_paragraphs,
        'Total QAs': total_qas,
        'Impossible QAs': impossible_qas,
        'Possible QAs':total_qas-impossible_qas
    }

for title, info in stats.items():
    print(f"Title：{title}")
    print(f"Number of Paragraphs：{info['Number of Paragraphs']}")
    print(f"Total QAs：{info['Total QAs']}")
    print(f"Impossible QAs：{info['Impossible QAs']}")
    print(f"Possible QAs：{info['Possible QAs']}\n")

print(len(stats.keys()))

output_filename_contexts =  '/path/to/train-zen-v1.0-contexts.json'

contexts_by_title = {}

for entry in data:
    title = entry['title']
    contexts = [para['context'] for para in entry['paragraphs']]
    contexts_by_title[title] = contexts

with open(output_filename_contexts, 'w', encoding='utf-8') as file:
    json.dump(contexts_by_title, file, ensure_ascii=False, indent=4)


output_filename_relavent =  '/path/to/train-zen-v1.0-relavent.json'
output_filename_irrelavent =  '/path/to/train-zen-v1.0-irrelavent.json'

possible_qas = []
impossible_qas = []

for entry in data:
    title = entry['title']
    for para in entry['paragraphs']:
        context = para['context']
        for qa in para['qas']:
            if qa['is_impossible']:
                qas_dict = {
                    'title': title,
                    'context': context,
                    'question': qa['question'],
                    'answers': qa['answers']
                }
                impossible_qas.append(qas_dict)
            else:
                qas_dict = {
                'title': title,
                'context': context,
                'question': qa['question'],
                'answers': qa['answers']
            }
                possible_qas.append(qas_dict)

with open(output_filename_relavent, 'w', encoding='utf-8') as file:
    json.dump(possible_qas, file, ensure_ascii=False, indent=4)
with open(output_filename_irrelavent, 'w', encoding='utf-8') as file:
    json.dump(impossible_qas, file, ensure_ascii=False, indent=4)
