import os
import sys
import inspect
import io
import ntpath
import pickle
from os import listdir

import boto3
from sklearn import preprocessing

def get_pickle(path):
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    current_path = f"{currentdir}/tmp/{path}"

    if not os.path.exists(current_path):
        download_file_from_s3(current_path)
        
    with open(current_path, 'rb') as pickle_file:
        pkl = pickle.load(pickle_file)

    return pkl

def download_file_from_s3(path):
    s3_client = boto3.client('s3')
    s3_client.download_file(
        os.environ.get('Bucket'),
        ntpath.basename(path),
        path
    )

def normalize_features(X):
    transformer = preprocessing.Normalizer().fit(X)
    return transformer.transform(X).tolist()
