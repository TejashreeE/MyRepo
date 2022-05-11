var MongoClient = require('mongodb').MongoClient;  
var url = "mongodb+srv://admin:SMUQis3ismx7zN4b@cluster44.zotew.mongodb.net/myFirstDatabase?retryWrites=true&w=majority";  
MongoClient.connect(url, function(err, db) {  
if (err) throw err;  
console.log("Database created!");  
db.close();  
});  