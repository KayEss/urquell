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

    def test_path_short(self):
        self.assertEqual(urlambda('http://www.example.com/', 'end').path, ['end'])
        self.assertEqual(urlambda('http://www.example.com/path', 'end').path, ['path', 'end'])
        self.assertEqual(urlambda('http://www.example.com:456//', 'end').path, ['', '', 'end'])
        self.assertEqual(urlambda('http://www.example.com:456//one', 'end').path, ['', 'one', 'end'])
        self.assertEqual(urlambda('http://www.example.com:456//one/', 'end').path, ['', 'one', '', 'end'])

    def test_path_longer(self):
        self.assertEqual(urlambda('http://www.example.com/', 'earlier', 'end').path, ['earlier', 'end'])
        self.assertEqual(urlambda('http://www.example.com/path', 'earlier', 'end').path, ['path', 'earlier', 'end'])
        self.assertEqual(urlambda('http://www.example.com:456//', 'earlier', 'end').path, ['', '', 'earlier', 'end'])
        self.assertEqual(urlambda('http://www.example.com:456//one', 'earlier', 'end').path, ['', 'one', 'earlier', 'end'])
        self.assertEqual(urlambda('http://www.example.com:456//one/', 'earlier', 'end').path, ['', 'one', '', 'earlier', 'end'])

    def test_query(self):
        self.assertEqual(urlambda('http://www.example.com/').state, {})
        self.assertEqual(urlambda('http://www.example.com/?k=').state, {'k':''})
        self.assertEqual(urlambda('http://www.example.com/?k=v').state, {'k':'v'})
        self.assertEqual(urlambda('http://www.example.com/?k=v&t=34').state, {'k':'v', 't':'34'})
        self.assertEqual(urlambda('http://www.example.com/?k=&k=v').state, {'k':['', 'v']})
        self.assertEqual(urlambda('http://www.example.com/?k=&v=k&k=v&k=v').state, {'k':['', 'v', 'v'], 'v':'k'})
        self.assertEqual(urlambda('http://www.example.com/?k=&v=k&k=v&k=p').state, {'k':['', 'v', 'p'], 'v':'k'})

if __name__ == '__main__':
    unittest.main()
