import psycopg2

#Class which have methods to read records in DB
class DBRead:
	def __init__(self, conn):
		self.conn = conn
	def read_user_by_id(self, id):
		""" read data from a user_static and user_dynamic Table """
		try:
			cur = self.conn.cursor()
			# edge case check
			if len(id) == 0:
				return []

			if type(id[0]) == 'str' and not id[0].isdigit():
				return []

			sql = """ SELECT * FROM users_dynamic left join users_static on
					users_static.user_id = users_dynamic.user_id where users_static.id = (%s) """

			cur.execute(sql, (id[0],))
			rows = cur.fetchall()
			container = []
			for row in rows:
				item = {}
				item['id'] = row[0]
				item['user_id'] = row[1]
				item['activity_id'] = row[2]
				item['followers_count'] = row[3]
				item['friends_count'] = row[4]
				item['statuses_count'] = row[5]
				item['created_at'] = row[8]
				item['screen_name'] = row[9]
				item['twitter_lang'] = row[10]
				item['location'] = row[11]
				container.append(item)
			return container
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)

	def read_users(self):
		""" read data from a user_static and user_dynamic Table """
		try:
			cur = self.conn.cursor()
			sql = """ SELECT * FROM users_dynamic left join users_static on users_static.user_id =
						users_dynamic.user_id"""

			cur.execute(sql)
			rows = cur.fetchall()
			container = []
			for row in rows:
				item = {}
				item['id'] = row[0]
				item['user_id'] = row[1]
				item['activity_id'] = row[2]
				item['followers_count'] = row[3]
				item['friends_count'] = row[4]
				item['statuses_count'] = row[5]
				item['created_at'] = row[8]
				item['screen_name'] = row[9]
				item['twitter_lang'] = row[10]
				item['location'] = row[11]
				container.append(item)
			return container
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)

	def read_activities(self):
		""" read data from activities Table """
		try:
			cur = self.conn.cursor()
			sql = """ SELECT * FROM activities, hash_tags where activities.activity_id = hash_tags.activity_id """
			cur.execute(sql)
			rows = cur.fetchall()
			container = []
			for row in rows:
				if any(item.get('activity_id', None) == row[1] for item in container):
					# id activity already exists, append hashtag
					container[-1]['hash_tags'] += "," + row[7]
					continue
				item = {}
				item['id'] = row[0]
				item['activity_id'] = row[1]
				item['created_at'] = row[2]
				item['body'] = row[3]
				item['user_id'] = row[4]
				item['urls'] = row[5]
				item['hash_tags'] = row[7]
				container.append(item)
			return container
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)


	def read_activities_by_id(self, id):
		""" read data from a activities and hash_tags Table """
		try:
			cur = self.conn.cursor()
			# edge case check
			if len(id) == 0:
				return []

			if type(id[0]) == 'str' and not id[0].isdigit():
				return []

			sql = """ SELECT * FROM activities, hash_tags where activities.activity_id = hash_tags.activity_id and id = (%s)"""

			cur.execute(sql, (id[0],))
			rows = cur.fetchall()
			container = []
			for row in rows:
				if any(item.get('activity_id', None) == row[1] for item in container):
					# id activity already exists, append hashtag
					container[-1]['hash_tags'] += "," + row[7]
					continue
				item = {}
				item['id'] = row[0]
				item['activity_id'] = row[1]
				item['created_at'] = row[2]
				item['body'] = row[3]
				item['user_id'] = row[4]
				item['urls'] = row[5]
				item['hash_tags'] = row[7]
				container.append(item)
			return container
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)

	def read_activities_by_hashtag(self, hashtag):
		""" read data from activities and hash_tags Table """
		try:
			cur = self.conn.cursor()
			# edge case check
			if len(hashtag) == 0:
				return []

			sql = """ SELECT * FROM activities, hash_tags where activities.activity_id = hash_tags.activity_id
						and lower(hash_tags.hashtag) like (%s)"""

			cur.execute(sql, (hashtag[0],))
			rows = cur.fetchall()
			container = []
			for row in rows:
				if any(item.get('activity_id', None) == row[1] for item in container):
					# id activity already exists, append hashtag
					container[-1]['hash_tags'] += "," + row[7]
					continue
				item = {}
				item['id'] = row[0]
				item['activity_id'] = row[1]
				item['created_at'] = row[2]
				item['body'] = row[3]
				item['user_id'] = row[4]
				item['urls'] = row[5]
				item['hash_tags'] = row[7]
				container.append(item)
			return container
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)

	def read_userID_activities(self, id):
		""" read data from activities and users_static Table """
		try:
			cur = self.conn.cursor()
			# edge case check
			sql = """ SELECT activities.id  FROM users_static left join activities
						on users_static.user_id = activities.user_id where users_static.id = (%s) """

			cur.execute(sql, (id,))
			rows = cur.fetchall()
			container = []
			for row in rows:
				# print row[0]
				item = self.read_activities_by_id(row)
				if len(item) == 1:
					container.append(item[0])

			return container
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
