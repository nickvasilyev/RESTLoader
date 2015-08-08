#!/apps/solr/python/bin/python3
import sys
import os
import requests
import logging
from multiprocessing import Process, Queue
from time import sleep,time
import argparse
import json
from pprint import pprint
import random

GLOB = {}
class RESTLoader():
    
    def __init__(self,conf,**kwargs):
        
    
    def main(self):
    GLOB['conf'] = load_config(args.conf)
    GLOB['base_gen'] = query_gen(GLOB['conf']['params'])
    GLOB['procs'] = []
    out = Queue()
    for p in range(GLOB['args'].procs):
        p = Process(target=wrap, args=(GLOB['base_gen'](),out,GLOB),kwargs=())
        GLOB['procs'].append(p)
        p.name = "Worker-{}".format(len(GLOB['procs']))
        p.start()
    #p.join()
    
def wrap(gen,queue,G,**kwargs):
    logging.info("Started a new worker process ")
    
    stime = time()
    for x in gen:
        if (time() - stime) <= G['args'].time:
            #logging.info(x)
            pass
        else:
            break
    logging.info("Terminating worker process")
        
def load_config(file):
    logging.debug("Loading Configuration from {}".format(file))
    with open(file) as f:
        conf = parse_config(json.load(f))
    logging.debug("Successfully Loaded Configuration")
    for k,v in conf['params'].items():
        logging.debug("{}({}):{}{}".format(k,str(len(v)),str(v)[:25],'...' if len(str(v))>25 else ''))
    return conf
    
def parse_config(conf):
    for c,cv in conf['params'].items():
        if type(cv) is str:
            if os.path.isfile(cv):
                try:
                    with open(cv) as f:
                        conf['params'][c] = json.loads(f.read())
                except ValueError as e:
                    logging.exception(e)
                    raise
            else:
                logging.error("Could not Find file [{}] for config parameter [{}]".format(cv,c))
                raise FileNotFoundError()
    return conf
    
def query_gen(c):
    logging.debug("Making Query Generator")
    def gen():
        while True:
            yield {k:random.choice(c[k]) for k in c}
    return gen
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse Product Excel Files')
    parser.add_argument('-url', type=str, default='http://localhost:7074/solr/', help='Base Url (e.x http://localhost:7074/solr/)')
    parser.add_argument('-procs', type=int, default=1, help='Number of Processes to Spawn')
    parser.add_argument('-time', type=int, default=1, help='Number of Seconds for the Test')
    parser.add_argument('-conf', type=str, help='Config File for the Test')
    parser.add_argument('-silent', action='store_true', default=False, help='Runs without any output')
    parser.add_argument('-v', action='store_true', default=False, help='Turns on Debug mode')
    args = parser.parse_args()
    loglevel = logging.INFO
    if args.v is True:
        loglevel=logging.DEBUG
    elif args.silent is True:
        loglevel=logging.ERROR
    logging.basicConfig(level=loglevel,format='%(asctime)s [%(levelname)s] (%(process)d) (%(threadName)s) %(message)s')
    logging.info("Starting REST Loader with config [{}]".format(args.conf))
    GLOB['args'] = args
    sys.exit(main())
    