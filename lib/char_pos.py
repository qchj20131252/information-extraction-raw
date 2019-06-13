from tqdm import *
import json

train_data_path = '../data/train_data.json'
train_data_hanlp_path = '../data/train_data_hanlp.json'
train_data_char_path = '../data/train_data_char.json'
dev_data_path = '../data/dev_data.json'
dev_data_hanlp_path = '../data/dev_data_hanlp.json'


def postag_by_char(filepath):
    train_data_list = json.load(open(filepath, mode='r', encoding='utf-8'))

    for dic in tqdm(train_data_list):
        char_pos = []
        for pos in dic['postag']:
            word = pos['word']
            postag = pos['pos']
            if len(word) == 1:
                char_pos.append({'char': word, 'pos': 'B-' + postag})
            elif len(word) == 2:
                char_pos.append({'char': word[0], 'pos': 'B-' + postag})
                char_pos.append({'char': word[-1], 'pos': 'E-' + postag})
            elif len(word) > 2:
                char_pos.append({'char': word[0], 'pos': 'B-' + postag})
                for c in word[1:-1]:
                    char_pos.append({'char': c, 'pos': 'I-' + postag})
                char_pos.append({'char': word[-1], 'pos': 'E-' + postag})
        dic['postag_by_char'] = char_pos

    json.dump(train_data_list, open(filepath, mode='w', encoding='utf-8'), ensure_ascii=False, indent=4)

if __name__ == '__main__':
    postag_by_char(train_data_hanlp_path)
    postag_by_char(dev_data_hanlp_path)

