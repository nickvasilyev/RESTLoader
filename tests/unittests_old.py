#!/apps/solr/python/bin/python3
import unittest
import REST_loader
import logging
logging.basicConfig(loglevel=logging.DEBUG)
class REST_Loader_UnitTests(unittest.TestCase):
    '''
    Will Test basic functionality of the Rest Loader
    '''
    @unittest.skip('works')
    def test_bad_config(self):
        with self.assertRaises(FileNotFoundError):
            d = REST_loader.parse_config({
                "name": "Test Query Dev Load",
                "params": {
                    "start": [0],
                    "q": "q.json",
                }
            })
    
    @unittest.skip('works')
    def test_bad_config1(self):
        with self.assertRaises(ValueError):
            d = REST_loader.parse_config({
                "name": "Test Query Dev Load",
                "params": {
                    "start": [0],
                    "q": "tests/test_queries_bad_json.json",
                }
            })
    
    @unittest.skip('works')
    def test_parse_config(self):
        self.assertEqual(
            REST_loader.parse_config({
                "name": "Test Query Dev Load",
                "params": {
                    "start": [0,25,50],
                    "q": "tests/test_queries.json",
                }
            }),
            {'params': {'q': ["_query_:{!edismax+v%3D'(ergonomic+keyboard)'+mm%3D$mm}", 'ergonomic+keyboard', "_query_:{!edismax+v%3D'(drip+pan)'+mm%3D$mm}", 'drip+pan', "_query_:{!edismax+v%3D'(fxa)'+mm%3D$mm}", 'fxa', "_query_:{!edismax+v%3D'(drip+pan)'+mm%3D$mm}", 'drip+pan', "_query_:{!edismax+v%3D'(standalone+photo+backup+drive)'+mm%3D$mm}", 'standalone+photo+backup+drive', "_query_:{!edismax+v%3D'(drip+pan)'+mm%3D$mm}", 'drip+pan', "_query_:{!edismax+v%3D'(vynil+shower+curtains)'+mm%3D$mm}", 'vynil+shower+curtains', "_query_:{!edismax+v%3D'(monitors)'+mm%3D$mm}", 'monitors', "_query_:{!edismax+v%3D'(portable+treatment+table)'+mm%3D$mm}", 'portable+treatment+table'], 'start': [0, 25, 50]}, 'name': 'Test Query Dev Load'}
            )
        
    #@unittest.skip('works')
    def test_load_conf(self):
        s = REST_loader.load_config('tests/test_conf.json')
        self.assertEqual(
        s,
        {'params': {'q': ["_query_:{!edismax+v%3D'(ergonomic+keyboard)'+mm%3D$mm}", 'ergonomic+keyboard', "_query_:{!edismax+v%3D'(drip+pan)'+mm%3D$mm}", 'drip+pan', "_query_:{!edismax+v%3D'(fxa)'+mm%3D$mm}", 'fxa', "_query_:{!edismax+v%3D'(drip+pan)'+mm%3D$mm}", 'drip+pan', "_query_:{!edismax+v%3D'(standalone+photo+backup+drive)'+mm%3D$mm}", 'standalone+photo+backup+drive', "_query_:{!edismax+v%3D'(drip+pan)'+mm%3D$mm}", 'drip+pan', "_query_:{!edismax+v%3D'(vynil+shower+curtains)'+mm%3D$mm}", 'vynil+shower+curtains', "_query_:{!edismax+v%3D'(monitors)'+mm%3D$mm}", 'monitors', "_query_:{!edismax+v%3D'(portable+treatment+table)'+mm%3D$mm}", 'portable+treatment+table'], 'single': ['single'], 'start': [0, 25, 50, 75, 100, 125, 150]}, 'name': 'Test Conf Dev Load'})
        return s
    
    def test_make_gen(self):
        s = self.test_load_conf()
        print("BLHAAA")
        print(s)
        
        
        
    
    def end(self):
        pass