# -*- coding: utf-8 -*-
"""
Download CholecTrack20 Dataset
author: Chinedu I. Nwoye
"""     
import requests
import synapseutils
import synapseclient
import os


def main():

    # 1. Login with Synapse credentials
    print("Authenticating user ...")
    syn = synapseclient.login()

    # 2. Request entity access
    print("Authenticating access key permission to download dataset ...")
    API_URL = "https://synapse-response.onrender.com/validate_access"
    USER_ID = syn.getUserProfile()['ownerId']
    response = requests.post(API_URL, json={"access_key": accesskey, "synapse_id": USER_ID})
    if response.status_code == 200:
        entity_id = response.json()['entity_id']
    else:
        print("❌ Failed to request access:", response.text)
        exit(1)

    # 3. Download dataset to your local folder
    print("Downloading dataset...")
    _ = synapseutils.syncFromSynapse(syn, entity=entity_id, path="/Users/deandrebailey/Downloads/Datasets/CholecTrack20")
    print("success!")


if __name__ == "__main__":

    # Configuration (Please complete these values and run the code)


    accesskey = os.environ["CHOLECTRACK_ACCESS_KEY"]

    main()
