# -*- coding: utf-8 -*-
import sys, unittest
sys.path.append('../Python')
sys.path.append('../../google_appengine')


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

    def test_query_addin(self):
        self.assertEqual(urlambda('http://www.example.com/', k=3).state, {'k':3})
        self.assertEqual(urlambda('http://www.example.com/?k=', k=None, v='s').state, {'k':None, 'v':'s'})
        self.assertEqual(urlambda('http://www.example.com/?k=v', k=4).state, {'k':4})
        self.assertEqual(urlambda('http://www.example.com/?k=v&t=34', x=4, t=[]).state, {'k':'v', 't':[], 'x':4})

    def test_processing(self):
        url = urlambda('http://www.example.com/')
        self.assertEqual(urlambda(url.prefix, *url.path, **url.state), url)
        url.path += ['another']
        self.assertEqual(urlambda(url.prefix, *url.path, **url.state), url)

    def test_representation_simple(self):
        self.roundtrip('http://www.example.com/', 'http://www.example.com/')
        self.roundtrip('http://www.example.com/path', 'http://www.example.com/path')
        self.roundtrip('http://www.example.com/path/path/', 'http://www.example.com/path/path/')
        self.roundtrip('http://www.example.com/path/path/p%20s', 'http://www.example.com/path/path/p%20s')
        self.roundtrip('http://www.example.com/20', 'http://www.example.com/', 20)
        self.roundtrip('http://www.example.com/20.25/3', 'http://www.example.com/', 20.25, 3)

    def test_representation_list(self):
        self.roundtrip('http://www.example.com/%5B%5D', 'http://www.example.com/', [])
        self.roundtrip('http://www.example.com/%5B20%5D', 'http://www.example.com/', [20])
        self.roundtrip('http://www.example.com/%5B%22hello%22%5D', 'http://www.example.com/', ["hello"])
        self.roundtrip('http://www.example.com/%5B%22hello%22%2C%2030%5D', 'http://www.example.com/', ["hello", 30])

    def test_representation_object(self):
        self.roundtrip('http://www.example.com/%7B%7D', 'http://www.example.com/', {})
        self.roundtrip('http://www.example.com/%7B%22k%22%3A%20%22v%22%7D', 'http://www.example.com/', dict(k='v'))

    def roundtrip(self, stringed, prefix, *path, **kwargs):
        """
            This abstracted test checks that we have proper round trips for various kinds of URL
        """
        self.assertEqual(stringed, repr(urlambda(stringed)))
        self.assertEqual(stringed, repr(urlambda(prefix, *path, **kwargs)))
        self.assertEqual(urlambda(stringed).path, urlambda(prefix, *path, **kwargs).path)

if __name__ == '__main__':
    unittest.main()
