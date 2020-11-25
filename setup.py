from os import path as os_path
from setuptools import setup
import lmdb_tools

this_directory = os_path.abspath(os_path.dirname(__file__))


# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding="utf-8") as f:
        long_description = f.read()
    return long_description


# 获取依赖
def read_requirements(filename):
    return [
        line.strip()
        for line in read_file(filename).splitlines()
        if not line.startswith("#")
    ]


setup(
    name="lmdb_tools",
    version=lmdb_tools.__version__,
    description="LMDB wrapper for faster and easier dataloading",
    author="Elliott Zheng",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    author_email="admin@hypercube.top",
    url="",
    license="MIT",
    keywords="lmdb",
    packages=["lmdb_tools"],
    install_requires=["lmdb", "tqdm"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
