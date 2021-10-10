import os
import pickle
from google.cloud import storage

def write_local_files_to_gcloud(real_path: str, fake_path: str, bucket_path:str, blob_name:str):
    real_poets = os.listdir(real_path)
    fake_poets = os.listdir(fake_path)
    poetry_index = {}
    for poet in real_poets:
        if poet in fake_poets:
            real_files = os.listdir(real_path+poet)
            real_dict = {}
            for file in real_files:
                with open(real_path+poet+"/"+file,"r", encoding="utf-8") as t:
                    real_dict[" ".join(n.capitalize() for n in file.split("-")[:-1])] = t.read()
            fake_files = os.listdir(fake_path+poet)
            fake_dict = {}
            for file in fake_files:
                with open(fake_path+poet+"/"+file,"r", encoding="utf-8") as t:
                    fake_dict[" ".join(n.capitalize() for n in file.split("-")[:-1])] = t.read()
            poetry_index[poet] = {'real': real_dict,'fake': fake_dict}

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_path)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(pickle.dumps(poetry_index))

    