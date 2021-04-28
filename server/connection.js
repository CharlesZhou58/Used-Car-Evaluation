//connection to db
const mysql = require('mysql');

//create connection to mysql db
var mysqlConnection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'passpasspass',
  database: 'p2',
  port: '3306',
  multipleStatements: true
});

//check if connected successfully
mysqlConnection.connect((err) => {
  if (!err) {
    console.log("Connected");
  }
  else {
    {
      console.log("Connection Fail: ");
    }
  }
});

//export module mysqlConnection
module.exports = mysqlConnection;
