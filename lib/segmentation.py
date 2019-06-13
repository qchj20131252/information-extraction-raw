# -*- coding: UTF-8 -*-

from pyhanlp import *
import json
from tqdm import *



return_list = []


cixing_list = ['r', 'v', 'u', 'n', 'w', 'nz', 'nr', 'p', 'f', 'b', 'nx', 'm', 'q', 'd', 'ns', 'i', 'a', 'ad', 't', 'Ng', 'ntc', 'z', 's', 'nt', 'vn', 'c', 'nnt', 'Vg', 'j', 'y', 'l', 'nrf', 'k', 'an', 'ntu', 'nsf', 'nto', 'Tg', 'Ag', 'nbc', 'nth', 'nit', 'ntcf', 'gb', 'nrj', 'nis', 'gp', 'ntcb', 'vd', 'nnd', 'gi', 'gm', 'Dg', 'gg', 'nba', 'vi', 'h', 'nf', 'nts', 'ntch', 'nhd', 'gc', 'nmc', 'nhm', 'Bg', 'e', 'o', 'Rg']
def word_segmentation(input_file, output_file):
    CRFnewSegment = HanLP.newSegment("crf")
    with open(input_file, mode='r', encoding='utf-8') as fr:
        for line in tqdm(fr.readlines()):
            return_dic = {}
            dic = json.loads(line.strip(), encoding='utf-8')
            text = dic['text']
            spo_list = dic['spo_list']
            return_dic['text'] = text
            return_dic['spo_list'] = spo_list
            term_list = CRFnewSegment.seg(text)
            pos_list = []
            for term in term_list:
                word = ''
                for q in str(term).split('/')[0: -1]:
                    word += q
                cixing = str(term).split('/')[-1]
                pos_list.append({'word': word, 'pos': cixing})
                if cixing not in cixing_list:
                    cixing_list.append(cixing)
            return_dic['postag'] = pos_list
            return_list.append(return_dic)
        json.dump(return_list, open(output_file, mode='a', encoding='utf-8'), ensure_ascii=False, indent=4)

def postag_dict(postag_dict_file):
    s = ['a', 'ad', 'Ag', 'al', 'an', 'b', 'begin', 'Bg', 'bl', 'c', 'cc', 'd', 'Dg', 'dl', 'e', 'end', 'f', 'g', 'gb', 'gbc', 'gc', 'gg', 'gi', 'gm', 'gp', 'h', 'i', 'j', 'k', 'l', 'm', 'mg', 'Mg', 'mq', 'n', 'nb', 'nba', 'nbc', 'nbp', 'nf', 'Ng', 'nh', 'nhd', 'nhm', 'ni', 'nic', 'nis', 'nit', 'nl', 'nm', 'nmc', 'nn', 'nnd', 'nnt', 'nr', 'nr1', 'nr2', 'nrf', 'nrj', 'ns', 'nsf', 'nt', 'ntc', 'ntcb', 'ntcf', 'ntch', 'nth', 'nto', 'nts', 'ntu', 'nx', 'nz', 'o', 'p', 'pba', 'pbei', 'q', 'qg', 'qt', 'qv', 'r', 'rg', 'Rg', 'rr', 'ry', 'rys', 'ryt', 'ryv', 'rz', 'rzs', 'rzt', 'rzv', 's', 't', 'Tg', 'u', 'ud', 'ude1', 'ude2', 'ude3', 'udeng', 'udh', 'ug', 'uguo', 'uj', 'ul', 'ule', 'ulian', 'uls', 'usuo', 'uv', 'uyy', 'uz', 'uzhe', 'uzhi', 'v', 'vd', 'vf', 'Vg', 'vi', 'vl', 'vn', 'vshi', 'vx', 'vyou', 'w', 'wb', 'wd', 'wf', 'wh', 'wj', 'wky', 'wkz', 'wm', 'wn', 'wp', 'ws', 'wt', 'ww', 'wyy', 'wyz', 'x', 'xu', 'xx', 'y', 'yg', 'z', 'zg']
    for pos in s:
        with open(postag_dict_file, mode='a', encoding='utf-8') as fw:
            fw.write('B-' + pos + '\n' + 'I-' + pos + '\n' + 'E-' + pos + '\n')

if __name__ == '__main__':
    train_data_path = '../data/train_data.json'
    train_data_hanlp_path = '../data/train_data_hanlp.json'
    dev_data_path = '../data/dev_data.json'
    dev_data_hanlp_path = '../data/dev_data_hanlp.json'
    postag_dict_file = '../dict/postag_dict'

    word_segmentation(train_data_path, train_data_hanlp_path)
    word_segmentation(dev_data_path, dev_data_hanlp_path)
    # postag_dict(postag_dict_file)
