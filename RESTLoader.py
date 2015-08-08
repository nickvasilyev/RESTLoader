import sys
import os
import requests
import logging
from multiprocessing import Process, Queue, Pool, JoinableQueue
from time import sleep,time
import json
#from pprint import pprint
import random
from concurrent.futures import ProcessPoolExecutor


class RESTLoader():
    
    def __init__(self,
                config,
                func=None,
                verbose=False,
                time=1,
                procs=2,
                reps=None,
                delay=0,
                **kwargs):
        if type(config) is dict:
            self.conf = self._parse_config(config)
        elif type(config) is str:
            self.conf = self._load_config(config)        
        for k,v in self.conf['params'].items():
            logging.debug("{}({}):{}{}".format(k,str(len(v)),str(v)[:25],'...' if len(str(v))>25 else ''))
        self.verbose = verbose
        self.conf['func'] = func
        self.conf['time'] = time
        self.conf['procs'] = procs
        self.conf['reps'] = reps
        self.conf['delay'] = delay
        self.data = []
        
    def _load_config(self,file):
        logging.debug("Loading Configuration from {}".format(file))
        with open(file) as f:
            conf = self._parse_config(json.load(f))
        return conf
    
    def _parse_config(self,conf):
        logging.debug("Parsing Config")
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

    
    def run(self):
        logging.debug("Starting Worker Processes")
        self._base_gen = self._query_gen(self.conf['params'])
        self.procs = []
        self.results = JoinableQueue()
        for p in range(self.conf['procs']):
            p = Process(target=self._wrap, args=(self._base_gen(),self.results),kwargs=())
            self.procs.append(p)
            p.start()
            
        #Have to clear the queue before the processes will join
        self._q_mon(self.results,self.data)
        while True in [p.is_alive() for p in self.procs]:
            if self.verbose:
                logging.info("checking queues")
            for p in (p for p in self.procs if p.is_alive()):
                logging.info("Trying to join Procs")
                p.join()
            sleep(1)
        logging.info("Successfully Finished Running and joined workers. Result set is {} items".format(len(self.data)))
            
            
    def _q_mon(self,results,data):
        while True:
            if results.qsize() > 0:
                if self.verbose:
                    logging.debug('q mon is collecting')
                data.append(results.get())
                results.task_done()
            else:
                if self.verbose:
                    logging.debug('qmon sleeping')
                    sleep(1)
                if True not in [p.is_alive() for p in self.procs]:
                    if self.verbose:
                        logging.debug("qmon is termianting")
                    return
            
            
    def _query_gen(self,c):
        logging.debug("Making Query Generator")
        def gen():
            while True:
                yield {k:random.choice(c[k]) for k in c}
        return gen
        
    def _wrap(self,gen,results,**kwargs):
        pid = os.getpid()
        logging.info("Started a new worker process [{}]".format(pid))
        if self.conf['func']:
            logging.info("Will be running supplied function")
        else:
            logging.debug("Running using default parameters")
            rs = requests.Session()
            stime = time()
            count = 0
            for data in gen:
                if self.conf['time'] and (time() - stime) > self.conf['time']:
                    logging.info("{} Process reached time limit of [{}]".format(pid,self.conf['time']))
                    break
                if self.conf['reps'] and count >= self.conf['reps']: 
                    logging.info("{} Process reached iteration limit of [{}]".format(pid,self.conf['reps']))
                    break
                else:
                    ttime = time()
                    r = rs.get(self.conf['base'],params=data)
                    results.put({
                        'status_code': r.status_code,
                        'url': r.url,
                        'msecs': r.elapsed.microseconds / 1000,
                        'pid':pid,
                        'time': time()-ttime
                        })
                    count += 1
                    if self.conf['delay'] > 0:
                        sleep(self.conf['delay'])
            r.close()
            rs.close()
        logging.info("Terminating worker process.")
        
        
    def get_results_list(self):
        return self.data
    
    def get_results_avg(self,fields=['msecs','time']):
        out = {}
        for field in fields:
            tl = [x[field] for x in self.data if x[field]]
            out[field] = sum(tl)/len(tl)
        return out
            