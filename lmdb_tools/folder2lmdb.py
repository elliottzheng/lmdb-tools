import os
import lmdb
import warnings

try:
    from torch.utils.data import DataLoader

    print("PyTorch found, using multi-processing to speed up loading.")
except:
    warnings.warn("PyTorch not found, fall back to single process loading.")
    from .utils import DefaultDataLoader as DataLoader

from tqdm import tqdm
from .utils import bin_reader, dumps_pickle
import platform


def is_win():
    return platform.system() == "Windows"


def grab_all(root):
    all_files = []
    for folder, dirs, files in os.walk(root, topdown=True):
        folder = folder.replace("\\", "/").replace(root, "").lstrip("/")
        all_files.extend(
            ["/".join([folder, name]) if len(folder) > 0 else name for name in files]
        )
    return all_files


class FolderDataset:
    def __init__(self, root, grab_func):
        root = root.replace("\\", "/")
        self.root = root
        self.files = grab_func(root)

    def __getitem__(self, index):
        name = self.files[index]
        file = os.path.join(self.root, name)
        return name, bin_reader(file)

    def __len__(self):
        return len(self.files)


def folder2lmdb(
    root, lmdb_path, grab_func=grab_all, write_frequency=5000, map_size=100
):
    print("Loading dataset from %s" % os.path.abspath(root))
    dataset = FolderDataset(root, grab_func)
    data_loader = DataLoader(
        dataset, batch_size=1, num_workers=0 if is_win() else 16, collate_fn=lambda x: x
    )
    assert lmdb_path.endswith(".lmdb")

    print("Generate LMDB to %s, map_size= %s GB" % (os.path.abspath(lmdb_path),map_size))
    db = lmdb.open(
        lmdb_path,
        subdir=False,
        map_size=int(1073741824 * map_size),
        readonly=False,
        meminit=False,
        map_async=True,
    )
    txn = db.begin(write=True)

    for idx, data in enumerate(tqdm(data_loader)):
        file_name, bin_data = data[0]
        txn.put(u"{}".format(file_name).encode("ascii"), bin_data)
        if (idx + 1) % write_frequency == 0:
            print("[%d/%d]" % (idx + 1, len(data_loader)))
            txn.commit()
            txn = db.begin(write=True)

    # finish iterating through dataset
    txn.commit()
    keys = [file_name for file_name in dataset.files]
    with db.begin(write=True) as txn:
        txn.put(b"__keys__", dumps_pickle(keys))
        txn.put(b"__len__", dumps_pickle(len(keys)))

    print("Flushing database ...")
    db.sync()
    db.close()
