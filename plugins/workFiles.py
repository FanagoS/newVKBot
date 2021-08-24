import random
import json
import os
import re
import math

users_dir = os.path.join(r"users/")

def loadjson(filepath):
    with open(filepath, 'r', encoding='utf-8') as jsonfile:
        return json.load(jsonfile, encoding='utf-8')

def dumpjson(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as jsonfile:
        return json.dump(data, jsonfile, ensure_ascii=False)