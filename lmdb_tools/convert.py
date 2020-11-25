from .folder2lmdb import folder2lmdb
import os
from distutils.util import strtobool


if __name__ == "__main__":
    # generate lmdb
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=str, help="input folder")
    parser.add_argument("db_path", type=str, help="output lmdb path")
    parser.add_argument(
        "map_size",
        type=float,
        help="mapsize(GB), please set carefully, especially in windows.",
    )
    args = parser.parse_args()
    if os.path.exists(args.db_path):
        response = input("{} {}".format(args.db_path, "already exists, delete?(Y/n)"))
        try:
            if not strtobool(response):
                pass
            else:
                raise NotImplementedError
        except:
            os.remove(args.db_path)
            print(args.db_path, "deleted")

    folder2lmdb(args.root, lmdb_path=args.db_path, map_size=args.map_size)
