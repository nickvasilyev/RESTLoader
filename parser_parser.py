#!/apps/solr/python/bin/python3
import sys
import os
import requests
import logging
from multiprocessing import Pool
from time import sleep
import argparse
import json

parser = argparse.ArgumentParser(description='Parse Product Excel Files')
parser.add_argument('-file', type=str, help='File')
args = parser.parse_args()

out = []

def parse_file(f,o):
    for x in f:
        try:
            if x.startswith('AfterQ'):
                o.append(x.split()[1])
            elif x.startswith('BeforeQ'):
                if 'AND' not in x and 'OR' not in x:
                    o.append(x.split()[1]+'}')
        except:
            print("Died at: " + x)
    
with open(args.file) as f:
    out.append(parse_file(f,out))

with open('data.txt', 'w') as outfile:
    json.dump(out, outfile)