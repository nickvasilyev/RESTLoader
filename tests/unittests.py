#!/apps/solr/python/bin/python3
import unittest
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s [%(levelname)s] (%(process)d) (%(threadName)s) %(message)s')
from RESTLoader import RESTLoader


class RESTLoader_UnitTests(unittest.TestCase):
    @unittest.skip('works')
    def test_bad_config(self):
        with self.assertRaises(FileNotFoundError):
            rl = RESTLoader({
                "name": "Test Query Dev Load",
                "params": {
                    "start": [0],
                    "q": "tests/q.json",
                }
            })
            
            
    @unittest.skip('works')
    def test_bad_config1(self):
        with self.assertRaises(ValueError):
            d = RESTLoader({
                "name": "Test Query Dev Load",
                "params": {
                    "start": [0],
                    "q": "tests/test_queries_bad_json.json",
                }
            })
            
    @unittest.skip('works')
    def test_parse_config(self):
        self.assertEqual(
            RESTLoader({
                "name": "Test Query Dev Load",
                "params": {
                    "start": [0,25,50],
                    "q": "tests/test_queries.json",
                }
            }).conf,
            {'params': {'q': ["_query_:{!edismax+v%3D'(ergonomic+keyboard)'+mm%3D$mm}", 'ergonomic+keyboard', "_query_:{!edismax+v%3D'(drip+pan)'+mm%3D$mm}", 'drip+pan', "_query_:{!edismax+v%3D'(fxa)'+mm%3D$mm}", 'fxa', "_query_:{!edismax+v%3D'(drip+pan)'+mm%3D$mm}", 'drip+pan', "_query_:{!edismax+v%3D'(standalone+photo+backup+drive)'+mm%3D$mm}", 'standalone+photo+backup+drive', "_query_:{!edismax+v%3D'(drip+pan)'+mm%3D$mm}", 'drip+pan', "_query_:{!edismax+v%3D'(vynil+shower+curtains)'+mm%3D$mm}", 'vynil+shower+curtains', "_query_:{!edismax+v%3D'(monitors)'+mm%3D$mm}", 'monitors', "_query_:{!edismax+v%3D'(portable+treatment+table)'+mm%3D$mm}", 'portable+treatment+table'], 'start': [0, 25, 50]}, 'name': 'Test Query Dev Load'}
            )
      

    @unittest.skip('works')
    def test_load_conf(self):
        s = RESTLoader('tests/test_conf.json')
        self.assertEqual(
        s.conf,
        {'params': {'q': ["_query_:{!edismax+v%3D'(ergonomic+keyboard)'+mm%3D$mm}", 'ergonomic+keyboard', "_query_:{!edismax+v%3D'(drip+pan)'+mm%3D$mm}", 'drip+pan', "_query_:{!edismax+v%3D'(fxa)'+mm%3D$mm}", 'fxa', "_query_:{!edismax+v%3D'(drip+pan)'+mm%3D$mm}", 'drip+pan', "_query_:{!edismax+v%3D'(standalone+photo+backup+drive)'+mm%3D$mm}", 'standalone+photo+backup+drive', "_query_:{!edismax+v%3D'(drip+pan)'+mm%3D$mm}", 'drip+pan', "_query_:{!edismax+v%3D'(vynil+shower+curtains)'+mm%3D$mm}", 'vynil+shower+curtains', "_query_:{!edismax+v%3D'(monitors)'+mm%3D$mm}", 'monitors', "_query_:{!edismax+v%3D'(portable+treatment+table)'+mm%3D$mm}", 'portable+treatment+table'], 'single': ['single'], 'start': [0, 25, 50, 75, 100, 125, 150]}, 'name': 'Test Conf Dev Load'})
        return s
        
        
    def test_run(self):
        logging.info("Starting Test Run 1")
        rl = RESTLoader({
            "name":"Test_run 1",
            "base" : "http://fcoh1s-advapp01t.fas.gsa.gov:7073/solr/products/consolidated",
            "params": {
                "start": [
                    0,
                    25,
                    50,
                    75,
                    100,
                    125,
                    150
                ],
                "q": "queries.json",
            }
            },time=10,procs=10)

        rl.run()
        print(rl.get_results_avg())
        
    

    

#"base" : "http://fcoh1s-advapp01t.fas.gsa.gov:7071/solr/products/consolidated",


    