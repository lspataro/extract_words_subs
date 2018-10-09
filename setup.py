# coding: utf-8
""" Setup script for installing fastai """
from setuptools import setup, find_packages

setup(
    name="extract_words_subs",
    packages=find_packages(),
    version='0.0.1',
    install_requires=['spacy', 'click'],
)
