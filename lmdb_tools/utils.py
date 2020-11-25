import pickle


def bin_reader(path):
    with open(path, "rb") as f:
        bin_data = f.read()
    return bin_data


def dumps_pickle(obj):
    """
    Serialize an object.
    Returns:
        Implementation-dependent bytes-like object
    """
    data = pickle.dumps(obj)
    return data


def loads_pickle(buf):
    """
    Args:
        buf: the output of `dumps`.
    """
    return pickle.loads(buf)


class DefaultDataLoader:
    def __init__(self, dataset, **kwargs):
        self.dataset = dataset
        assert kwargs["batch_size"] == 1
        self.index = 0

    def __iter__(self):
        self.index=0
        return self

    def __next__(self):
        if self.index < len(self.dataset):
            self.index += 1
            return [self.dataset[self.index - 1]]
        else:
            raise StopIteration

    def __len__(self):
        return len(self.dataset)
