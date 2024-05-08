# import os
# import accimage
import pathlib
import numpy as np
import pandas as pd

# import torch
from torch.utils.data import DataLoader, Dataset
# from torchvision import transforms
# import torchvision.transforms as T
# import albumentations as A

from PIL import Image
# from transformers import AutoProcessor

def get_tuberlin_dataset(split:str, cls_list):
    '''
    split: 'train', 'val', 'test'
    '''

    assert split in ['train', 'val', 'test'], print("use proper split: train, val, test")
    ann_file_path = pathlib.Path(__file__).parent.resolve()
    ann_file = ann_file_path / 'test_tuberlin.csv' if split=='test' else ann_file_path / 'train_tuberlin.csv'
    
    return TUDataset(ann_file, cls_list)

class TUDataset(Dataset):
    
    def __init__(self, ann_file, cls_list):
        self.cls_list = cls_list
        self.ann = self._filter_cls(pd.read_csv(ann_file))
        print(f'[INFO] {len(self.ann)} number of image-label pairs({len(cls_list)} classes) loaded')
    
    def _filter_cls(self, annot_file):
        return annot_file[annot_file['label'].isin(self.cls_list)] if len(self.cls_list)>0 else annot_file

    def __getitem__(self, index):
        sample = self.ann.iloc[[index]]
        
        text = sample.text.values[0]
        img_path = sample.img_path.values[0]
        
        # image = Image.open(img_path)
        image = Image.open(img_path).convert('RGB')
        # transformed = self.transform(image=np.array(image, dtype=np.uint8))
        
        output = {}
        output["text"] = text
        # output["image"] = transformed["image"]
        output["image"] = image
        output["mod_idx"] = [sample.m1.values[0], sample.m2.values[0]],
        output["label"] = sample.label.values[0]
        
        return output

    def __len__(self):
        return len(self.ann)
    