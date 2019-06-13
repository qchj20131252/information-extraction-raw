import json
from tqdm import *

import os

def load_word_file(f_input):
    """
    Get all words in files
    :param string: input file
    """
    file_chars = {}
    data_list = json.load(open(f_input, mode='r', encoding='utf-8'))
    for dic in tqdm(data_list):
        chars = []
        try:
            text = dic['text']
            chars = [char for char in text]
        except:
            continue
        for char in chars:
            file_chars[char] = file_chars.get(char, 0) + 1
    return file_chars


def get_char(train_file, dev_file, char_idx_file):
    """
    Get vocabulary file from the field 'postag' of files
    :param string: input train data file
    :param string: input dev data file
    """
    char_dic = load_word_file(train_file)
    if len(char_dic) == 0:
        raise ValueError('The length of train word is 0')
    dev_char_dic = load_word_file(dev_file)
    if len(dev_char_dic) == 0:
        raise ValueError('The length of dev word is 0')
    for char in dev_char_dic:
        if char in char_dic:
            char_dic[char] += dev_char_dic[char]
        else:
            char_dic[char] = dev_char_dic[char]
    with open(char_idx_file, mode='w', encoding='utf-8') as fw:
        fw.write('<UNK>' + '\n')
    char_set = set()
    value_list = sorted(char_dic.items(), key=lambda d: d[1], reverse=True)
    for char in value_list:
        with open(char_idx_file, mode='a', encoding='utf-8') as fw:
            fw.write(char[0] + '\n')
        char_set.add(char[0])

    # add predicate in all_50_schemas
    if not os.path.exists('../data/all_50_schemas'):
        raise ValueError("../data/all_50_schemas not found.")
    with open('../data/all_50_schemas', mode='r', encoding='utf-8') as fr:
        for line in fr:
            dic = json.loads(line.strip(), encoding='utf-8')
            p = dic['predicate']
            for c in p:
                if c not in char_set:
                    char_set.add(c)
                    with open(char_idx_file, mode='a', encoding='utf-8') as fw:
                        fw.write(c + '\n')


if __name__ == '__main__':
    train_file = '../data/train_data_hanlp.json'
    dev_file = '../data/dev_data_hanlp.json'
    char_idx_file = '../dict/char_idx'
    get_char(train_file, dev_file, char_idx_file)