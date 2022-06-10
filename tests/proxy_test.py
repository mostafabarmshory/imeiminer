import unittest
from imeiminer.proxy import UptimerBotProxy

class TestUptimerBotProxy(unittest.TestCase):

    def test_update_proxy_list(self):
        proxy_to_test = UptimerBotProxy()
        proxy_to_test.update_proxy_list()
        self.assertTrue(len(proxy_to_test.proxy_list)>0)
        self.assertTrue(proxy_to_test.last_update_time > 0)
        
    def test_ip_change(self):
        proxy_to_test = UptimerBotProxy()
        first_ip = proxy_to_test.get_ip()
        second_ip = proxy_to_test.get_ip()
        self.assertNotEqual(first_ip, second_ip, "IP is not change")

if __name__ == '__main__':
    unittest.main()