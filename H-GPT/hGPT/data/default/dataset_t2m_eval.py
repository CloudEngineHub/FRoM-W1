import random
import numpy as np
from torch.utils.data import Dataset
import codecs as cs
import os
import random
from os.path import join as pjoin

import numpy as np
import spacy
import torch
from rich.progress import track
from torch.utils import data
from torch.utils.data._utils.collate import default_collate
from tqdm import tqdm
import threading
from concurrent.futures import ThreadPoolExecutor
import queue

from .dataset_t2m_base import Text2MotionDatasetBaseDist

class Text2MotionDatasetEval(Text2MotionDatasetBaseDist):
    def __init__(
        self,
        motion_feat_path,
        text_path,
        cot_path,
        split_path,
        split,
        mean,
        std,
        min_motion_length,
        max_motion_length,
        unit_length,
        fps,
        max_text_len,
        w_vectorizer,
        debug=False,
        mean_eval=None,
        std_eval=None,
        # truncate=False,
        # test_bs=32,
        **kwargs,
    ):
        super().__init__(motion_feat_path, text_path, cot_path, split_path, split, mean, std, min_motion_length,
                         max_motion_length, unit_length, fps, debug, **kwargs)
        self.max_text_len = max_text_len
        self.w_vectorizer = w_vectorizer
        
        # yfgao: WARNING! This is only for MM test
        # if truncate:
        #     raise NotImplementedError
        #     len_dataset = len(self.name_list)
        #     self.name_list = self.name_list[:len_dataset - len_dataset % test_bs]

    def __getitem__(self, idx):
        name = self.name_list[idx]
        # name = '013514'
        
        data = self.data_dict[name]
        motion, m_length, text_list = data["motion"], data["length"], data["text"]
        
        # print (">>> text list: ", text_list)
        
        # Randomly select a caption
        text_data = random.choice(text_list)
        # print(text_data)
        caption = text_data["caption"]
        tokens = text_data["tokens"]
        cot = text_data["cot"]

        all_captions = [
            ' '.join([token.split('/')[0] for token in text_dic['tokens']])
            for text_dic in text_list
        ]
        if len(all_captions) > 3:
            all_captions = all_captions[:3]
        elif len(all_captions) == 2:
            all_captions = all_captions + all_captions[0:1]
        elif len(all_captions) == 1:
            all_captions = all_captions * 3

        # Text
        if len(tokens) < self.max_text_len:
            # pad with "unk"
            # if sent_len == 0:
            #     tokens = ["sos/OTHER"] + ["eos/OTHER"]
            # else:
            tokens = ["sos/OTHER"] + tokens + ["eos/OTHER"]
            sent_len = len(tokens)
            tokens = tokens + ["unk/OTHER"] * (self.max_text_len + 2 - sent_len)
        else:
            # crop
            tokens = tokens[:self.max_text_len]
            tokens = ["sos/OTHER"] + tokens + ["eos/OTHER"]
            sent_len = len(tokens)
        
        pos_one_hots = []
        word_embeddings = []
        for token in tokens:
            # for noise version.
            try:
                _, _ = token.split('/')
            except:
                # print (f"item: {token}")
                pos_one_hots.append(pos_one_hots[-1])
                word_embeddings.append(word_embeddings[-1])
                continue
            
            word_emb, pos_oh = self.w_vectorizer[token]
            pos_one_hots.append(pos_oh[None, :])
            word_embeddings.append(word_emb[None, :])
        pos_one_hots = np.concatenate(pos_one_hots, axis=0)
        word_embeddings = np.concatenate(word_embeddings, axis=0)
        
        # Crop the motions in to times of unit_length, and introduce small variations
        if self.unit_length < 10:
            coin2 = np.random.choice(["single", "single", "double"])
        else:
            coin2 = "single"
        
        if coin2 == "double":
            m_length = (m_length // self.unit_length - 1) * self.unit_length
        elif coin2 == "single":
            m_length = (m_length // self.unit_length) * self.unit_length

        idx = random.randint(0, len(motion) - m_length)
        motion = motion[idx:idx + m_length]
        
        # Z Normalization
        motion = (motion - self.mean) / self.std

        # for eval.
        # if m_length < self.max_motion_length:
        #     motion = np.concatenate([motion,
        #                              np.zeros((self.max_motion_length - m_length, motion.shape[1]), dtype=np.float32)
        #                              ], axis=0)

        # return name, motion, m_length, m_tokens, m_tokens_len, caption, sent_len, "_".join(tokens), word_embeddings, pos_one_hots, all_captions, cot, task
        return name, motion, m_length, None, None, caption, sent_len, "_".join(tokens), word_embeddings, pos_one_hots, all_captions, cot, None


# class Text2MotionDatasetV2(Dataset):

#     def __init__(
#         self,
#         motion_feat_path,
#         text_path,
#         cot_path,
#         split_path,
#         split,
#         mean,
#         std,
#         min_motion_length,
#         max_motion_length,
#         unit_length,
#         fps,
#         max_text_len,
#         w_vectorizer,
#         debug=False,
#         mean_eval=None,
#         std_eval=None,
#         # truncate=False,
#         # test_bs=32,
#         **kwargs,
#     ):
#         motion_dir = motion_feat_path
#         split_file = f"{split_path}/{split}.txt"
#         text_dir = text_path
        
#         self.w_vectorizer = w_vectorizer
#         # self.max_length = 20
#         self.pointer = 0
#         self.max_motion_length = max_motion_length
#         # min_motion_len = 40 if dataset_name =='t2m' else 24
#         self.min_motion_length = min_motion_length
#         self.max_text_len = max_text_len
#         self.unit_length = unit_length

#         data_dict = {}
#         id_list = []
#         with cs.open(split_file, "r") as f:
#             for line in f.readlines():
#                 id_list.append(line.strip())
#         self.id_list = id_list
#         print (f"Total {len(self.id_list)} Items.")
        
#         if debug:
#             enumerator = enumerate(self.id_list)
#             maxdata = 100
#             subset = '_tiny'
#         else:
#             enumerator = enumerate(
#                 track(
#                     self.id_list,
#                     f"Loading Dataset {split_file}",
#                 ))
#             maxdata = 1e10
#             subset = ''

#         # if progress_bar:
#         #     enumerator = enumerate(
#         #         track(
#         #             id_list,
#         #             f"Loading HumanML3D {split_file.split('/')[-1].split('.')[0]}",
#         #         ))
#         # else:
#         #     enumerator = enumerate(id_list)
            
#         count = 0
#         bad_count = 0
#         new_name_list = []
#         length_list = []
#         for i, name in enumerator:
#             if count > maxdata:
#                 break
#             try:
#                 motion = np.load(pjoin(motion_dir, name + ".npy"))
#                 if np.isnan(motion).any():
#                     bad_count += 1
#                     continue
                
#                 if (len(motion)) < self.min_motion_length or (len(motion) >=
#                                                               300):
#                     bad_count += 1
#                     continue
                
#                 text_data = []
#                 flag = False
#                 with cs.open(pjoin(text_dir, name + ".txt")) as f:
#                     for line in f.readlines():
#                         text_dict = {}
#                         line_split = line.strip().split("#")
#                         caption = line_split[0]
#                         tokens = line_split[1].split(" ")
#                         f_tag = float(line_split[2])
#                         to_tag = float(line_split[3])
#                         f_tag = 0.0 if np.isnan(f_tag) else f_tag
#                         to_tag = 0.0 if np.isnan(to_tag) else to_tag

#                         text_dict["caption"] = caption
#                         text_dict["tokens"] = tokens
#                         if f_tag == 0.0 and to_tag == 0.0:
#                             flag = True
#                             text_data.append(text_dict)
#                         else:
#                             try:
#                                 n_motion = motion[int(f_tag * 30):int(to_tag *
#                                                                       30)]
#                                 if (len(n_motion)
#                                     ) < self.min_motion_length or (
#                                         (len(n_motion) >= 300)):
#                                     continue
#                                 new_name = (
#                                     random.choice("ABCDEFGHIJKLMNOPQRSTUVW") +
#                                     "_" + name)
#                                 while new_name in data_dict:
#                                     new_name = (random.choice(
#                                         "ABCDEFGHIJKLMNOPQRSTUVW") + "_" +
#                                                 name)
#                                 data_dict[new_name] = {
#                                     "motion": n_motion,
#                                     "length": len(n_motion),
#                                     "text": [text_dict],
#                                 }
#                                 new_name_list.append(new_name)
#                                 length_list.append(len(n_motion))
#                             except:
#                                 # None
#                                 print(line_split)
#                                 print(line_split[2], line_split[3], f_tag,
#                                       to_tag, name)
#                                 # break

#                 if flag:
#                     data_dict[name] = {
#                         "motion": motion,
#                         "length": len(motion),
#                         "text": text_data,
#                     }
#                     new_name_list.append(name)
#                     length_list.append(len(motion))
#                     # print(count)
#                     count += 1
#                     # print(name)
#             except:
#                 pass
#         # print (len(new_name_list), len(length_list))
#         # exit(0)
        
#         name_list, length_list = zip(
#             *sorted(zip(new_name_list, length_list), key=lambda x: x[1]))

#         self.mean = mean
#         self.std = std
#         self.length_arr = np.array(length_list)
#         self.data_dict = data_dict
#         self.nfeats = motion.shape[1]
#         self.name_list = name_list
#         # self.reset_max_len(self.max_length)
#         print (f">>> Load {len(self.name_list)} Samples.")

#     def reset_max_len(self, length):
#         assert length <= self.max_motion_length
#         self.pointer = np.searchsorted(self.length_arr, length)
#         print("Pointer Pointing at %d" % self.pointer)
#         self.max_length = length

#     def inv_transform(self, data):
#         return data * self.std + self.mean

#     def __len__(self):
#         return len(self.name_list) - self.pointer

#     def __getitem__(self, item):
#         idx = self.pointer + item
#         name = self.name_list[idx]
        
#         # name = '013514'
        
#         data = self.data_dict[name]
#         motion, m_length, text_list = data["motion"], data["length"], data[
#             "text"]
        
#         # print (">>> text list: ", text_list)
        
#         # Randomly select a caption
#         text_data = random.choice(text_list)
        
#         caption, tokens = text_data["caption"], text_data["tokens"]

#         if len(tokens) < self.max_text_len:
#             # pad with "unk"
#             tokens = ["sos/OTHER"] + tokens + ["eos/OTHER"]
#             sent_len = len(tokens)
#             tokens = tokens + ["unk/OTHER"
#                                ] * (self.max_text_len + 2 - sent_len)
#         else:
#             # crop
#             tokens = tokens[:self.max_text_len]
#             tokens = ["sos/OTHER"] + tokens + ["eos/OTHER"]
#             sent_len = len(tokens)
#         pos_one_hots = []
#         word_embeddings = []
#         for token in tokens:
#             word_emb, pos_oh = self.w_vectorizer[token]
#             pos_one_hots.append(pos_oh[None, :])
#             word_embeddings.append(word_emb[None, :])
#         pos_one_hots = np.concatenate(pos_one_hots, axis=0)
#         word_embeddings = np.concatenate(word_embeddings, axis=0)

#         # Crop the motions in to times of 4, and introduce small variations
#         if self.unit_length < 10:
#             coin2 = np.random.choice(["single", "single", "double"])
#         else:
#             coin2 = "single"

#         if coin2 == "double":
#             m_length = (m_length // self.unit_length - 1) * self.unit_length
#         elif coin2 == "single":
#             m_length = (m_length // self.unit_length) * self.unit_length
#         idx = random.randint(0, len(motion) - m_length)
#         motion = motion[idx:idx + m_length]
#         "Z Normalization"
#         motion = (motion - self.mean) / self.std

#         # # padding
#         # if m_length < self.max_motion_length:
#         #     motion = np.concatenate(
#         #         [
#         #             motion,
#         #             np.zeros((self.max_motion_length - m_length, motion.shape[1])),
#         #         ],
#         #         axis=0,
#         #     )
#         # print(word_embeddings.shape, motion.shape, m_length)
#         # print(tokens)

#         # debug check nan
#         if np.any(np.isnan(motion)):
#             raise ValueError("nan in motion")

#         return name, motion, m_length, None, None, caption, sent_len, "_".join(tokens), word_embeddings, pos_one_hots, None, None, None
    
        # return (
        #     word_embeddings,
        #     pos_one_hots,
        #     caption,
        #     sent_len,
        #     motion,
        #     m_length,
        #     "_".join(tokens),
        # )
        # return caption, motion, m_length

def set_seed(seed=42):
    """
    固定随机种子以确保结果可复现
    
    参数:
        seed (int): 随机种子，默认为42
    """
    # Python内置random模块
    random.seed(seed)
    
    # Numpy
    np.random.seed(seed)
    
    # PyTorch
    torch.manual_seed(seed)
    
    # 如果使用CUDA（GPU）
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)  # 如果使用多GPU
        # 额外的CUDA设置以确保确定性
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    
    # 设置Python哈希种子（用于字典等数据结构的哈希）
    os.environ['PYTHONHASHSEED'] = str(seed)
    
    print(f"所有随机种子已设置为: {seed}")

def unit_test():
    set_seed(42)
    
    from hGPT.data.default.word_vectorizer import WordVectorizer
    w_vectorizer = WordVectorizer('/inspire/hdd/project/embodied-multimodality/public/hgpt/pli/HumanoidGPT/deps/glove_t2m/', "our_vab")

    mld_dataset = Text2MotionDatasetV2(
        motion_feat_path = '/inspire/hdd/project/embodied-multimodality/public/pli/FRoM-W1/datasets/humanml3d-x/data/new_joint_vecs',
        text_path = '/inspire/hdd/project/embodied-multimodality/public/pli/FRoM-W1/datasets/humanml3d-x/data/texts',
        cot_path = '/inspire/hdd/project/embodied-multimodality/public/pli/FRoM-W1/datasets/humanml3d-x/data/cot-v3',
        split_path = '/inspire/hdd/project/embodied-multimodality/public/pli/FRoM-W1/datasets/humanml3d-x/data',
        split = 'test',
        mean = 0.0,
        std = 1.0,
        min_motion_length = 60,
        max_motion_length = 300,
        unit_length = 4,
        fps = 30,
        max_text_len = 20,
        w_vectorizer = w_vectorizer,
        debug=False,
    )
    print ("MLD: ", len(mld_dataset))
    print (mld_dataset[0])

    set_seed(42)
    test_dataset = Text2MotionDatasetEval(
        motion_feat_path = '/inspire/hdd/project/embodied-multimodality/public/pli/FRoM-W1/datasets/humanml3d-x/data/new_joint_vecs',
        text_path = '/inspire/hdd/project/embodied-multimodality/public/pli/FRoM-W1/datasets/humanml3d-x/data/texts',
        cot_path = '/inspire/hdd/project/embodied-multimodality/public/pli/FRoM-W1/datasets/humanml3d-x/data/cot-v3',
        split_path = '/inspire/hdd/project/embodied-multimodality/public/pli/FRoM-W1/datasets/humanml3d-x/data',
        split = 'test',
        mean = 0.0,
        std = 1.0,
        min_motion_length = 60,
        max_motion_length = 300,
        unit_length = 4,
        fps = 30,
        max_text_len = 20,
        w_vectorizer = w_vectorizer,
        debug=False,
    )
    print ("mGPTs: ", len(test_dataset))
    print (test_dataset[0])
    
if __name__ == "__main__":
    unit_test()