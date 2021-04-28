//server control main file
const mysql = require('mysql');
const express = require('express');
const bodyParser = require('body-parser');
const mysqlConnection = require('./connection');
const home = require('./routes/home');

//using express framework
var app = express();

//render ejs file
app.set('view engine', 'ejs');

app.use(bodyParser.json());

//transfer control to home.js if any link is localhost:8000/home
app.use("/home", home);

//listen on port 8000
app.listen(8000);

/*
is the port is being used, you can kill the process by:
sudo lsof -i :8000
kill -9 pid
*/
