/*Insertion Order FOR database loading:
            users_static
            twitterraw
            activities
            users_dynamic
            hash_tags
*/


/*Deletion order*/
DROP TABLE IF EXISTS Hash_Tags;
DROP TABLE IF EXISTS Users_Dynamic;
DROP TABLE IF EXISTS Activities;
DROP TABLE IF EXISTS TwitterRaw;
DROP TABLE IF EXISTS Users_Static CASCADE;



/*static data of user that is unlikely to change over time
*/
CREATE TABLE Users_Static (
    id SERIAL,
    user_id TEXT NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT '1900-01-01 00:00:00', /*user account create time(twitter.user.created_at)*/
    screen_name TEXT DEFAULT NULL, 								/*screen name*/
    twitter_lang TEXT DEFAULT NULL, 							/*language used in tweeter*/
    location TEXT DEFAULT NULL,   								/*twitter profile location*/

    PRIMARY KEY(user_id)
);

/*create B+ tree index on user_id
*/
CREATE INDEX user_id_idx ON Users_Static (user_id);


/*twitter whole rawjson dump, in case need other fields in the whole twitter json in the future
*/
CREATE TABLE TwitterRaw (
      id SERIAL,
      activity_id TEXT NOT NULL DEFAULT 0,
      raw_json BYTEA DEFAULT NULL,                /*entire json for storage*/

      PRIMARY KEY (activity_id)
 );


/*twitter main content
*/
CREATE TABLE Activities (
	    id SERIAL,
      activity_id TEXT NOT NULL DEFAULT 0,
      created_at TIMESTAMP NOT NULL DEFAULT '1900-01-01 00:00:00', 	/*twitter create time(twitter.created_at)*/
      body TEXT DEFAULT NULL, 										/*activity body text(twitte.text)*/
      user_id TEXT NOT NULL DEFAULT 0,
      urls TEXT DEFAULT NULL,             							 /*urls, unstructured data*/

      PRIMARY KEY (activity_id),
      FOREIGN KEY (activity_id) REFERENCES TwitterRaw,
      FOREIGN KEY (user_id) REFERENCES Users_Static
);



/*dynamic data of user that is likely to change over time*/
/*1 to 1 with activity
*/
CREATE TABLE Users_Dynamic (
    id SERIAL,
    user_id TEXT NOT NULL DEFAULT 0,
    activity_id TEXT NOT NULL DEFAULT 0, 					/*key into activities table*/
    followers_count INT NOT NULL DEFAULT 0,
    friends_count INT NOT NULL DEFAULT 0,
    statuses_count INT NOT NULL DEFAULT 0,

    PRIMARY KEY (activity_id),
    FOREIGN KEY (activity_id) REFERENCES Activities
);


/*Hashtags of one single twitter
many to many hashtags versus activities
*/
CREATE TABLE Hash_Tags (
    activity_id TEXT NOT NULL DEFAULT 0,
    hashtag TEXT DEFAULT NULL,               	 /*single hashtag*/
    FOREIGN KEY (activity_id) REFERENCES Activities

);




