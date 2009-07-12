from google.appengine.ext import db

"""
Example record

{
ihash: '3jdHes',
url: 'http://urquell-fn.appspot.com/lib/sub/3/4.json
}
"""

class Invocation(db.Model):
  ihash = db.StringProperty(required=True)
  url = db.StringProperty(required=True)