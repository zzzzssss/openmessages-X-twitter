from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse
from db.dbread import DBRead
from db.dbwrite import DBWrite
from db.dbconnect import DBConnect
import json
from datetime import datetime

# http://localhost:8000/v1/
class SimpleRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
    	dbconn = DBConnect()
    	conn = dbconn.getDB()
    	dbrd = DBRead(conn)

        strmp = urlparse.urlparse(self.path)
        queryDict = urlparse.parse_qs(strmp.query)
        print strmp.path
        print queryDict

        result = {}
        # only suport v1 now
        if "/v1/" not in strmp.path:
            print "404 not found"
            self.send_response(404)
            self.end_headers()

        if "/users" in strmp.path:
            if not queryDict:
                # queryDict is empty
                url_parts = strmp.path.split('/')
                if "/activities" in strmp.path \
                    and len(url_parts)==5 \
                    and url_parts[-1] == 'activities':
                        result = dbrd.read_userID_activities(url_parts[3])
                elif len(url_parts) == 3:
                    result = dbrd.read_users()
            elif 'id' in queryDict:
        	   result = dbrd.read_user_by_id(queryDict['id'])
        if "/twitterActivities" in strmp.path:
            if not queryDict:
                result = dbrd.read_activities()
            elif 'id' in queryDict:
               result = dbrd.read_activities_by_id(queryDict['id'])
            elif 'hashtag' in queryDict:
               result = dbrd.read_activities_by_hashtag(queryDict['hashtag'])

        # close database connection
        dbconn.closeDB()
        if not result:
            print "404 not found"
            self.send_response(404)
            self.end_headers()
        else:
            print "200 succeed"
            self.send_response(200)
            self.end_headers()
        self.wfile.write(json.dumps(result, indent = 4, sort_keys = True, default = str))

    def do_POST(self):
    	"""POST Method; port: 8000; endpoint: /users/
    	 example url: http://localhost:8000/users"""
        strmp = urlparse.urlparse(self.path)
        queryDict = urlparse.parse_qs(strmp.query)

        print strmp.path
        print queryDict

        dbconn = DBConnect()
    	conn = dbconn.getDB()
        dbrt = DBWrite(conn)

        # only accept Json format body
        if self.headers.getheader('Content-Type',0) != "application/json":
            dbconn.closeDB()
            self.send_response(406)
            self.end_headers()
            return

        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        decoded = json.loads(post_body)

        # only create when user_id is integer
        if not decoded['user_id'].isdigit():
            dbconn.closeDB()
            self.send_response(404)
            self.end_headers()
            return

        # handler
        if "/users" in strmp.path:
            dbrt.write_user_static(decoded['user_id'], str(datetime.now()),decoded['username'],
                decoded['twitter_lang'],decoded['location'])

        dbconn.closeDB()

        self.send_response(201)
        self.end_headers()
        self.wfile.write(json.dumps(decoded))
        return
