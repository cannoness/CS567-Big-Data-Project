// Get the right database.

// Find one thingie and print.  
use USATweets;
show collections;
db.tweets.count();
//db.tweets.findOne({}, {"user.id_str":1 , "id_str":1, "_id":0});
var myCursor = db.tweets.find({}, {"user.id_str":1 , "id_str":1, "_id":0});

while (myCursor.hasNext()) {
	print(tojson(myCursor.next()));
}
> 
