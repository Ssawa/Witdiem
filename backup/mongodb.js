var express = require('express');
var app = express();
var MongoClient = require('mongodb').MongoClient;

/*MongoClient.connect("mongodb://localhost:27017/witdiem", function(err, db) {
  if(!err) {
    console.log("We are connected");
    var collection = db.collection('tweets');
    var stream = collection.find({}, {text: 1, created_at: 1, 'user.screen_name': 1 }).stream();
    stream.on("data", function(item) {console.log(item)});
    stream.on("end", function() {});
  }
});*/