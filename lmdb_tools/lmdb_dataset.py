import torch.utils.data as data
from .buffer_helper import buffer2cv
from .manager import DBManager


class ImageLMDB(data.Dataset):
    def __init__(self, db_path):
        self.db_path = db_path
        self.manager = DBManager(db_path, {".png": buffer2cv})
        self.keys = self.manager.keys

    def __getitem__(self, index):
        name = self.keys[index]
        pix = self.manager.get(name, buffer=False)
        return pix

    def __len__(self):
        return len(self.keys)


if __name__ == "__main__":
    dataset = ImageLMDB("a.lmdb")
    from torch.utils.data import DataLoader

    loader = DataLoader(dataset, shuffle=True)
    for data in loader:
        print(data.shape)
