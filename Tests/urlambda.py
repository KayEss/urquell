# -*- coding: utf-8 -*-
import sys, unittest
sys.path.append('../Python')

from urquell.url import urlambda

class URLParsing(unittest.TestCase):
    def test_prefix(self):
        self.assertEqual(urlambda('http://www.example.com/').prefix, 'http://www.example.com/')
        self.assertEqual(urlambda('http://www.example.com/path').prefix, 'http://www.example.com/')
        self.assertEqual(urlambda('http://www.example.com:456/').prefix, 'http://www.example.com:456/')

    def test_path(self):
        self.assertEqual(urlambda('http://www.example.com/').path, [])
        self.assertEqual(urlambda('http://www.example.com/path').path, ['path'])
        self.assertEqual(urlambda('http://www.example.com:456//').path, ['', ''])
        self.assertEqual(urlambda('http://www.example.com:456//one').path, ['', 'one'])
        self.assertEqual(urlambda('http://www.example.com:456//one/').path, ['', 'one', ''])

if __name__ == '__main__':
    unittest.main()
