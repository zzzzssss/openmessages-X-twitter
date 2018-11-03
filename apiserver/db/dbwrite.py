import psycopg2

activity_id_map = {}
user_id_map = {}
#Class which have methods to create records in DB
class DBWrite:
	def __init__(self, conn):
		self.conn = conn

	def write_user_static(self, user_id, created_at, screen_name, twitter_lang, location):
		try:
			if user_id not in user_id_map:
				# create a new cursor object
				cur = self.conn.cursor()
				# execute the INSERT statement
				cur.execute("INSERT INTO users_static(user_id,created_at,screen_name,twitter_lang,location) " +
							"VALUES(%s,%s,%s,%s,%s)",
							(user_id.encode('utf-8').strip(), created_at.encode('utf-8').strip(), screen_name.encode('utf-8').strip(),
							twitter_lang.encode('utf-8').strip(), location.encode('utf-8').strip()))
				# commit the changes to the database
				self.conn.commit()
				print "commited user_static"
				user_id_map[user_id] = True
				# close the communication with the PostgresQL database
				cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)


	def write_raw(self, activity_id, json_str):
		try:
			if activity_id not in activity_id_map:
				cur = self.conn.cursor()
				cur.execute("INSERT INTO twitterraw(activity_id,raw_json) " +
							"VALUES(%s,%s)",
							(activity_id, psycopg2.Binary(json_str)))
				self.conn.commit()
				print "commited write_raw"
				activity_id_map[activity_id] = True
				cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)


	def write_activity(self, activity_id, created_at, body, user_id, urls):
		try:
			cur = self.conn.cursor()
			cur.execute("INSERT INTO activities(activity_id,created_at,body,user_id,urls) " +
						"VALUES(%s,%s,%s,%s,%s)",
						(activity_id.encode('utf-8').strip(), created_at.encode('utf-8').strip(), body.encode('utf-8').strip(),
						user_id.encode('utf-8').strip(), urls.encode('utf-8').strip()))
			self.conn.commit()
			print "commited activity"
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)


	def write_user_dynamic(self, user_id, activity_id, followers_count, friends_count, statuses_count):
		try:
			cur = self.conn.cursor()
			cur.execute("INSERT INTO users_dynamic(user_id,activity_id,followers_count,friends_count,statuses_count) " +
						"VALUES(%s,%s,%s,%s,%s)",
						(user_id.encode('utf-8').strip(), activity_id.encode('utf-8').strip(), followers_count,
						friends_count, statuses_count))
			self.conn.commit()
			print "commited user_dynamic"
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)


	def write_hashtags(self, activity_id, hashtags):
		try:
			cur = self.conn.cursor()
			for i in range(len(hashtags)):
				hashtag = hashtags[i]['text']

				cur.execute("INSERT INTO hash_tags(activity_id, hashtag) " +
						"VALUES(%s,%s)",
						(activity_id.encode('utf-8').strip(), hashtag.encode('utf-8').strip()))
				self.conn.commit()
				print "commited hashtag"
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)

