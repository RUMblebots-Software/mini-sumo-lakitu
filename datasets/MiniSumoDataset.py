import os
import torch
import numpy as np
from tqdm import tqdm
from torchvision import datasets, transforms
from torch.utils.data import Dataset, Subset
from sklearn.model_selection import train_test_split
from collections import defaultdict
from datasets.CustomDataset import BoundingBoxDataset

class MiniSumoDataset(BoundingBoxDataset):
    """
    Custom dataset for Mini-Sumo real time bounding box classification.

    Args:
        transform (`transforms.Compose`): Transformations to apply to images.
        mode (`str`): Dataset split (`train`, `val`, `test`).  
    """
    
    rootDir = "G:\\Shared drives\\RB\\2025-2026\\Spring 2026\\Software\\MiniSumoDataset\\"

    def __init__(
        self, 
        transform=None, 
        mode="train", 
    ):
        self.name = "Mini-Sumo Dataset"
        self.mode = mode

        super().__init__(
            self.rootDir, 
            json_file=os.path.join(self.rootDir, f"info.json"),
            transform=transform, 
        )
    
    @classmethod
    def getDir(cls):
        return cls.rootDir
    

class TestMiniSumoDataset:
    def __init__(self, mode="train", split_ratios={'train': 0.8, 'val': 0.1, 'test': 0.1}, random_state=18):
        self.mode = mode
        self.split_ratios = split_ratios
        self.random_state = random_state

        self.ds = MiniSumoDataset(mode=self.mode)
        targets = self.ds.targets

        train_idx, temp_idx = train_test_split(
            np.arange(len(targets)),
            test_size=1 - split_ratios['train'],
            stratify=targets,
            random_state=random_state
        )
        val_idx, test_idx = train_test_split(
            temp_idx,
            test_size=split_ratios['test'] / (split_ratios['val'] + split_ratios['test']),
            # stratify=targets[temp_idx], # Commented out due to the small sample size of some species
            random_state=random_state
        )

        if mode == "train":
            self.indices = train_idx
        elif mode == "val":
            self.indices = val_idx
        elif mode == "test":
            self.indices = test_idx
        
        self.totalImages = len(self.indices)
        self.class_to_idx = self.ds.class_to_idx
        self.numClasses = len(self.class_to_idx)

        self.idx_to_class = {v: k for k, v in self.class_to_idx.items()}

        self.validationDict = defaultdict(int)
        for idx in self.indices:
            label = targets[idx] 
            self.validationDict[label] += 1

        self.dataSubset = Subset(self.ds, self.indices)

    def runTests(self):
        print(("Testing %s dataset: subset %s")%(self.ds.getName(),self.mode))
        
        assert len(self.dataSubset) == self.totalImages, f"Expected {self.totalImages} images, got {len(self.dataSubset)}"
        print(("\t%s:%s Length validated")%(self.ds.getName(),self.mode))
        
        assert len(self.ds.class_to_idx) == self.numClasses, f"Expected {self.numClasses} classes, got {len(self.ds.class_to_idx)}"
        print(("\t%s:%s Num classes validated")%(self.ds.getName(),self.mode))

        dsDict = defaultdict(int)
        for i in tqdm(range(len(self.dataSubset)), desc="Processing dataset"):
            img, label = self.dataSubset[i] 
            label = int(label)
            dsDict[label] += 1
        for key, val in self.validationDict.items():
            assert dsDict[key] == val, f"Expected {val} images for label {key}, got {dsDict[key]}"

        print(("\t%s:%s Image qty per label validated")%(self.ds.getName(),self.mode))

def testDataset():
    split_ratios = {"train": 0.8, "val": 0.1, "test": 0.1}
    for mode in ["train", "val", "test"]:
        test = TestMiniSumoDataset(mode=mode, split_ratios=split_ratios)
        test.runTests()

if __name__ == '__main__':
    testDataset()
