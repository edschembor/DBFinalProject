from flask import Flask, render_template, request, json
import MySQLdb as db
import pdb
import decimal

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/tweetsHashtag",methods=['POST','GET'])
def tweetsHashtag():
	try:
		hashtag = request.form['tweetsHashtagInput']
		#call stored procedure
		conn = db.connect(host = 'localhost', user="dbproject", passwd="edvictor", db="twitterdata")
		cur = conn.cursor(db.cursors.DictCursor)
		cur.callproc('FindTweetsGivenHashTag', (hashtag,))
		# If the procedure is executed successfully, then we'll commit the changes and return the success message. 
		data = cur.fetchall()
		if(len(data) > 0):
			tuples = list()
			for row in data:
				tuples.append(row)
			return json.dumps({'success': tuples})
		else:
			return json.dumps({'error': "The hashtag does not exist"})
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cur.close()
		conn.close()

@app.route("/tweetsWord",methods=['POST','GET'])
def tweetsWord():
	try:
		word = request.form['tweetsWordInput']
		#call stored procedure
		conn = db.connect(host = 'localhost', user="dbproject", passwd="edvictor", db="twitterdata")
		cur = conn.cursor(db.cursors.DictCursor)
		cur.callproc('FindTweetsGivenWord', (word,))
		# If the procedure is executed successfully, then we'll commit the changes and return the success message. 
		data = cur.fetchall()
		if(len(data) > 0):
			tuples = list()
			for row in data:
				tuples.append(row)
			return json.dumps({'success': tuples})
		else:
			return json.dumps({'error': "The word is not part of any tweet"})
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cur.close()
		conn.close()

@app.route("/userLongest",methods=['POST','GET'])
def userLongest():
	try:
		count = request.form['userLongestInput']
		#call stored procedure
		conn = db.connect(host = 'localhost', user="dbproject", passwd="edvictor", db="twitterdata")
		cur = conn.cursor(db.cursors.DictCursor)
		cur.callproc('TweetCountAndLongest', (count,))
		# If the procedure is executed successfully, then we'll commit the changes and return the success message. 
		data = cur.fetchall()
		if(len(data) > 0):
			tuples = list()
			for row in data:
				tuples.append(row)
			return json.dumps({'success': tuples})
		else:
			return json.dumps({'error': "Something went wrong"})
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cur.close()
		conn.close()

@app.route("/userSentiment",methods=['POST','GET'])
def userSentiment():
	try:
		user = request.form['userSentimentInput']
		#call stored procedure
		conn = db.connect(host = 'localhost', user="dbproject", passwd="edvictor", db="twitterdata")
		cur = conn.cursor(db.cursors.DictCursor)
		cur.callproc('FindUserSentiment', (user,))
		# If the procedure is executed successfully, then we'll commit the changes and return the success message. 
		data = cur.fetchall()
		if(len(data) > 0):
			tuples = list()
			for row in data:
				tuples.append(row)
			return json.dumps({'success': tuples})
		else:
			return json.dumps({'error': "Something went wrong"})
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cur.close()
		conn.close()

@app.route("/mentionFollowers",methods=['POST','GET'])
def mentionFollowers():
	try:
		#call stored procedure
		conn = db.connect(host = 'localhost', user="dbproject", passwd="edvictor", db="twitterdata")
		cur = conn.cursor(db.cursors.DictCursor)
		cur.execute('''
			SELECT Users.ScreenName
			FROM Users
			WHERE Users.UserId IN(
				SELECT Mentions.WhoIsMentioned
				FROM Mentions
				JOIN Followers ON Mentions.WhoIsMentioned = Followers.WhoIsFollowed
				JOIN Retweets ON Mentions.TweetId = Retweets.TweetId AND RetweeterId = Mentions.WhoMentions
			)
			''')
		# If the procedure is executed successfully, then we'll commit the changes and return the success message. 
		data = cur.fetchall()
		if(len(data) > 0):
			tuples = list()
			for row in data:
				tuples.append(row)
			return json.dumps({'success': tuples})
		else:
			return json.dumps({'error': "No such user"})
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cur.close()
		conn.close()

@app.route("/palindromeUser",methods=['POST','GET'])
def palindromeUser():
	try:
		#call stored procedure
		conn = db.connect(host = 'localhost', user="dbproject", passwd="edvictor", db="twitterdata")
		cur = conn.cursor(db.cursors.DictCursor)
		cur.execute('''
			SELECT T.TweetId, U.ScreenName, U.NumPosts 
			FROM Tweets as T, Users as U 
			WHERE T.UserId = U.UserId and T.TweetId = Reverse(T.TweetId);
			''')
		# If the procedure is executed successfully, then we'll commit the changes and return the success message. 
		data = cur.fetchall()
		if(len(data) > 0):
			tuples = list()
			for row in data:
				tuples.append(row)
			return json.dumps({'success': tuples})
		else:
			return json.dumps({'error': "No palindrome users"})
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cur.close()
		conn.close()

@app.route("/userLiked",methods=['POST','GET'])
def userLiked():
	try:
		#call stored procedure
		conn = db.connect(host = 'localhost', user="dbproject", passwd="edvictor", db="twitterdata")
		cur = conn.cursor(db.cursors.DictCursor)
		cur.execute('''
			SELECT H.Hashtag 
			FROM (SELECT UserId, count(TweetId) AS FavCount, M.maxFav FROM Favorites, 
				(SELECT max(F.FavCount) AS maxFav 
					FROM (SELECT count(TweetId) AS FavCount From Favorites group by UserId) AS F) 
				AS M group by UserId) 
			AS countAndMax, Tweets AS T, Hashtags AS H 
			WHERE countAndMax.FavCount = countAndMax.maxFav and T.UserId = countAndMax.UserId and T.TweetId = H.TweetId;
			''')
		# If the procedure is executed successfully, then we'll commit the changes and return the success message. 
		data = cur.fetchall()
		if(len(data) > 0):
			tuples = list()
			for row in data:
				tuples.append(row)
			return json.dumps({'success': tuples})
		else:
			return json.dumps({'error': "No such user for userLiked"})
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cur.close()
		conn.close()

@app.route("/webscaleMongo",methods=['POST','GET'])
def webscaleMongo():
	try:
		#call stored procedure
		conn = db.connect(host = 'localhost', user="dbproject", passwd="edvictor", db="twitterdata")
		cur = conn.cursor(db.cursors.DictCursor)
		cur.execute('''
			SELECT DISTINCT U.ScreenName 
			FROM Tweets as T, Users as U, Hashtags as H 
			WHERE T.UserId = U.UserId AND T.TweetId = H.TweetId AND T.Content LIKE '%mongo db%' OR T.Content LIKE '%webscale%' 
			OR U.ScreenName LIKE '%mongo db%' OR U.ScreenName LIKE '%webscale%' OR H.Hashtag LIKE '%mongo db%' OR H.Hashtag LIKE '%webscale%';
			''')
		# If the procedure is executed successfully, then we'll commit the changes and return the success message. 
		data = cur.fetchall()
		if(len(data) > 0):
			tuples = list()
			for row in data:
				tuples.append(row)
			return json.dumps({'success': tuples})
		else:
			return json.dumps({'error': "No one believes in mongo db and webscale"})
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cur.close()
		conn.close()

@app.route("/userNBA",methods=['POST','GET'])
def userNBA():
	try:
		#call stored procedure
		conn = db.connect(host = 'localhost', user="dbproject", passwd="edvictor", db="twitterdata")
		cur = conn.cursor(db.cursors.DictCursor)
		cur.execute('''
			SELECT T.Content 
			FROM Users as U, Tweets as T 
			WHERE U.ScreenName Like '%NBA%' AND U.UserId = T.UserId;
			''')
		# If the procedure is executed successfully, then we'll commit the changes and return the success message. 
		data = cur.fetchall()
		if(len(data) > 0):
			tuples = list()
			for row in data:
				tuples.append(row)
			return json.dumps({'success': tuples})
		else:
			return json.dumps({'error': "No such content for NBA"})
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cur.close()
		conn.close()

@app.route("/posClinton",methods=['POST','GET'])
def posClinton():
	try:
		#call stored procedure
		conn = db.connect(host = 'localhost', user="dbproject", passwd="edvictor", db="twitterdata")
		cur = conn.cursor(db.cursors.DictCursor)
		cur.execute('''
			SELECT Tot.Total, pos.Positive, (pos.positive/Tot.total) as PercentPositive 
			FROM (SELECT count(T.TweetId) as Total 
				FROM Tweets as T, Hashtags as H WHERE T.TweetId = H.TweetId AND H.Hashtag = 'Clinton') as Tot, 
					(SELECT count(T.TweetId) as Positive FROM Tweets as T, Hashtags as H 
				WHERE T.TweetId = H.TweetId AND H.Hashtag = 'Clinton' AND T.Sentiment = "Positive") as pos;
			''')
		# If the procedure is executed successfully, then we'll commit the changes and return the success message. 
		data = cur.fetchall()
		if(len(data) > 0):
			tuples = list()
			for row in data:
				tuples.append(row)
			return json.dumps({'success': tuples}, default=decimal_default)
		else:
			return json.dumps({'error': "No one likes Clinton"})
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cur.close()
		conn.close()

@app.route("/userRank",methods=['POST','GET'])
def userRank():
	try:
		#call stored procedure
		conn = db.connect(host = 'localhost', user="dbproject", passwd="edvictor", db="twitterdata")
		cur = conn.cursor(db.cursors.DictCursor)
		cur.execute('''
			SELECT UserId, ScreenName, NumFollowers/NumFollowing AS FollowersToFollowingRatio FROM Users ORDER BY FollowersToFollowingRatio;
			''')
		# If the procedure is executed successfully, then we'll commit the changes and return the success message. 
		data = cur.fetchall()
		if(len(data) > 0):
			tuples = list()
			for row in data:
				tuples.append(row)
			return json.dumps({'success': tuples}, default=decimal_default)
		else:
			return json.dumps({'error': "Something went wrong with user rank"})
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cur.close()
		conn.close()

@app.route("/posSentiment",methods=['POST','GET'])
def posSentiment():
	try:
		#call stored procedure
		conn = db.connect(host = 'localhost', user="dbproject", passwd="edvictor", db="twitterdata")
		cur = conn.cursor(db.cursors.DictCursor)
		cur.execute('''
			SELECT U.ScreenName, count(TweetId) as PositiveTweetCount 
			FROM Users AS U, Tweets as T WHERE U.UserId = T.UserId 
			AND T.Sentiment = "positive" group by U.ScreenName 
			ORDER BY PositiveTweetCount LIMIT 5;
			''')
		# If the procedure is executed successfully, then we'll commit the changes and return the success message. 
		data = cur.fetchall()
		if(len(data) > 0):
			tuples = list()
			for row in data:
				tuples.append(row)
			return json.dumps({'success': tuples}, default=decimal_default)
		else:
			return json.dumps({'error': "The world is a sad place"})
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cur.close()
		conn.close()

@app.route("/largestPic",methods=['POST','GET'])
def largestPic():
	try:
		#call stored procedure
		conn = db.connect(host = 'localhost', user="dbproject", passwd="edvictor", db="twitterdata")
		cur = conn.cursor(db.cursors.DictCursor)
		cur.execute('''
			SELECT M.Link as LargestPictureLink 
			FROM Media as M, (SELECT max(Height*Width) 
			AS maxArea FROM Media) as Max 
			WHERE M.Height*M.Width = Max.maxArea;
			''')
		# If the procedure is executed successfully, then we'll commit the changes and return the success message. 
		data = cur.fetchall()
		if(len(data) > 0):
			tuples = list()
			for row in data:
				tuples.append(row)
			return json.dumps({'success': tuples}, default=decimal_default)
		else:
			return json.dumps({'error': "No pictures available"})
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cur.close()
		conn.close()

@app.route("/hashtagNBA",methods=['POST','GET'])
def hashtagNBA():
	try:
		#call stored procedure
		conn = db.connect(host = 'localhost', user="dbproject", passwd="edvictor", db="twitterdata")
		cur = conn.cursor(db.cursors.DictCursor)
		cur.execute('''
			SELECT U.ScreenName
			FROM Media as M, Tweets as T, Users as U, Hashtags as H 
			WHERE M.TweetId = T.TweetId AND H.TweetId = T.TweetId
			AND H.Hashtag = "NBA" AND U.UserId = T.UserId;
			''')
		# If the procedure is executed successfully, then we'll commit the changes and return the success message. 
		data = cur.fetchall()
		if(len(data) > 0):
			tuples = list()
			for row in data:
				tuples.append(row)
			return json.dumps({'success': tuples}, default=decimal_default)
		else:
			return json.dumps({'error': "No pictures with the NBA hashtag"})
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cur.close()
		conn.close()

@app.route("/posBarcelona",methods=['POST','GET'])
def posBarcelona():
	try:
		#call stored procedure
		conn = db.connect(host = 'localhost', user="dbproject", passwd="edvictor", db="twitterdata")
		cur = conn.cursor(db.cursors.DictCursor)
		cur.execute('''
			SELECT T.Content 
			FROM Tweets AS T, Hashtags AS H 
			WHERE T.TweetId = H.TweetId 
			AND T.Sentiment = "positive" AND H.Hashtag LIKE '%Barcelona%';
			''')
		# If the procedure is executed successfully, then we'll commit the changes and return the success message. 
		data = cur.fetchall()
		if(len(data) > 0):
			tuples = list()
			for row in data:
				tuples.append(row)
			return json.dumps({'success': tuples}, default=decimal_default)
		else:
			return json.dumps({'error': "No one likes Barcelona"})
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cur.close()
		conn.close()

if __name__ == "__main__":
    app.run()