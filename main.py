import datasets # import the package defined
import torch
from sklearn.model_selection import train_test_split
import numpy as np
from torch.utils.data import Subset

# using the package and imports from __init__.py call the attributes
ds = datasets.MiniSumoDataset(None, "train")
# dataloader = datasets.DataLoader(ds, 1, False)
targets = ds.targets
mode = ds.mode
split_ratios  = {'train': 0.8, 'val': 0.1, 'test': 0.1}

def count_splits(mode, split_ratios, targets, random_state):    

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
    # print(f"Train idx: {train_idx}, Val idx: {val_idx}, Test idx: {test_idx}")
    dataset_train_subset = Subset(ds, train_idx)
    dataset_val_subset = Subset(ds,val_idx)
    dataset_test_subset = Subset(ds,test_idx)

    data_loader_train = datasets.DataLoader(dataset_train_subset,1,True)
    data_loader_val = datasets.DataLoader(dataset_val_subset,1,True)
    data_loader_test = datasets.DataLoader(dataset_test_subset,1,True)

    print(f"Training Dataloader created with {len(data_loader_train)} samples.")
    print(f"Validation Dataloader created with {len(data_loader_val)} samples.")
    print(f"Test Dataloader created with {len(data_loader_test)} samples.")


count_splits(mode, split_ratios,targets, random_state=18)

