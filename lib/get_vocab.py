"""
This module to generate vocabulary list
"""
from tqdm import *
import os
import json

def load_word_file(f_input):
    """
    Get all words in files
    :param string: input file
    """
    file_words = {}
    data_list = json.load(open(f_input, mode='r', encoding='utf-8'))
    words = []
    for dic in tqdm(data_list):
        try:
            postag = dic['postag']
            words = [item["word"].strip() for item in postag]
        except:
            continue
        for word in words:
            file_words[word] = file_words.get(word, 0) + 1
    return file_words


def get_vocab(train_file, dev_file , word_idx_file):
    """
    Get vocabulary file from the field 'postag' of files
    :param string: input train data file
    :param string: input dev data file
    """
    word_dic = load_word_file(train_file)
    if len(word_dic) == 0:
        raise ValueError('The length of train word is 0')
    dev_word_dic = load_word_file(dev_file)
    if len(dev_word_dic) == 0:
        raise ValueError('The length of dev word is 0')
    for word in dev_word_dic:
        if word in word_dic:
            word_dic[word] += dev_word_dic[word]
        else:
            word_dic[word] = dev_word_dic[word]
    with open(word_idx_file, mode='w', encoding='utf-8') as fw:
        fw.write('<UNK>' + '\n')
    vocab_set = set()
    value_list = sorted(word_dic.items(), key=lambda d: d[1], reverse=True)
    for word in value_list[:30000]:
        with open(word_idx_file, mode='a', encoding='utf-8') as fw:
            fw.write(word[0] + '\n')
        vocab_set.add(word[0])

    #add predicate in all_50_schemas
    if not os.path.exists('../data/all_50_schemas'):
        raise ValueError("../data/all_50_schemas not found.")
    with open('../data/all_50_schemas', mode='r', encoding='utf-8') as fr:
        for line in fr:
            dic = json.loads(line.strip(), encoding='utf-8')
            p = dic['predicate']
            if p not in vocab_set:
                vocab_set.add(p)
                with open(word_idx_file, mode='a', encoding='utf-8') as fw:
                    fw.write(p + '\n')

    
if __name__ == '__main__':
    train_file = '../data/train_data_hanlp.json'
    dev_file = '../data/dev_data_hanlp.json'
    word_idx_file = '../dict/word_idx'
    get_vocab(train_file, dev_file, word_idx_file)
