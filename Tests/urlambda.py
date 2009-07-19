# -*- coding: utf-8 -*-
import sys, unittest
sys.path.append('../Python')

from urquell.url import urlambda

class Constructors(unittest.TestCase):
    def test_basic(self):
        self.assert_(urlambda('http://www.example.com/').prefix == 'http://www.example.com/')
        self.assert_(urlambda('http://www.example.com/path').prefix == 'http://www.example.com/')
        self.assert_(urlambda('http://www.example.com:456/').prefix == 'http://www.example.com:456/')

if __name__ == '__main__':
    unittest.main()
