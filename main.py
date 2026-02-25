import datasets # import the package defined

# using the package and imports from __init__.py call the attributes
dataset = datasets.MiniSumoDataset(None, "train")
dataloader = datasets.DataLoader(dataset, 1, False)


