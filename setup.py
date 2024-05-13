from setuptools import setup, find_packages

with open(file="requirements.txt", mode="r") as f:
    requirements = f.read().splitlines()

setup(
    name="WDFAP",
    version="1.1.0",
    packages=find_packages(),
    author="Ismael Mousa",
    author_email="ismaelramzimousa@gmail.com",
    description="Python tool for asynchronously fetching and storing articles from web sources"
                " in various formats such as csv, json, xlsx, and parquet",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/IsmaelMousa/WDFAP",
    install_requires=requirements,
    python_requires=">=3.10",
    license="MIT", )
