pyqdb-tests
===========

Just playing with [CherryPy](http://cherrypy.org) and making quote database.

####What is pyqdb?
It's just a simple project written in python3 with cherrypy. I made it because I was bored and wanted to
try something new. I don't know how did you get here, but I know that it's not what you're looking for.

In my opinion CherryPy is interesting, but isn't suitable for apps like that (unless you have a lot of time or know
cherrypy and have tools/plugins). If I have to do real qdb, I will go with django.

**It's just my playground** inspired by Twiseless.

####Requirements:
- python3.3
- sqlite3
- cherrypy
- mako

####Install
````bash
virtualenv -p python3.3 qdb
cd qdb
source bin/activate
pip install cherrypy
pip install mako
pip install sqlite3
git clone https://github.com/mescam/pyqdb-tests.git
cd pyqdb-tests
./quotes.py #this should be done inside screen session, because pyqdb still lacks 'run in background' mode.
````
This will launch http server on port 8080 (see conf/http.cfg), you can use mod_proxy so your webserver can pass :80 requests
Example for lighttpd:
````
$HTTP["host"] == "qdb.example.net" {
  proxy.server = ( "" => (( "host"=>"127.0.0.1", "port"=>8080 )) )
}
````
####Screenshot:
![scr](http://dev.mescam.pl/Screenshots/qdb-github.png "pyqdb")
