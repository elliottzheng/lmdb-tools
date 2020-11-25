import lmdb
import os.path as osp
import lmdb
from .utils import loads_pickle


class DBManager:
    def __init__(self, db_path, buffer_funcs={}) -> None:
        self.env = lmdb.open(
            db_path,
            subdir=osp.isdir(db_path),
            readonly=True,
            lock=False,
            readahead=False,
            meminit=False,
        )
        with self.env.begin(write=False) as txn:
            self.length = loads_pickle(txn.get(b"__len__"))
            self.keys = [
                key.decode() if isinstance(key, bytes) else key
                for key in loads_pickle(txn.get(b"__keys__"))
            ]
        self.buffer_funcs = buffer_funcs

    def get(self, name, buffer: bool = True):
        env = self.env
        with env.begin(write=False) as txn:
            byteflow = txn.get(name.encode())

        if not buffer:
            ext = osp.splitext(osp.basename(name))[1]
            if ext in self.buffer_funcs:
                return self.buffer_funcs[ext](byteflow)
        return byteflow

    def __exit__(self, exc_type, exc_value, traceback):
        self.env.close()
        del self.env
        del self.length
        del self.keys
        del self.buffer_funcs
