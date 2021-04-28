//control all the web pages
const express = require('express');
const mysqlConnection = require('../connection');
const router = express.Router();

//handle the /home page by render the home.ejs
router.get("/", function (req, res) {
  res.render('home')
});

//global variables for each query
var gmanufacturer;
var gmodel;
var gyear;
var godometer;
var gprice;

//the home page goes to /home/middle request, which handles here for taking the manufacturer input
//then redirect to /home/home2 page for user to input more, which is handle by the next router function
//req is the returned value pack
router.get('/middle', function (req, res) {
  gmanufacturer = req.query.manufacturer;
  res.redirect("/home/home2");
});

//handle the /home/home2 page request which send by the lase router function
//in this function, it takes the user input for manufacturer, and query in db to find corresponding model list to show in the front-end
//then render the file home2.ejs with model list and manufacturer
router.get('/home2', async (req, res) => {
  var sqlmodel = "SELECT model from vehicles WHERE manufacturer = '" + gmanufacturer + "'" + "GROUP BY model ORDER BY count(*) DESC"
  //Query
  mysqlConnection.query(sqlmodel, (err, rows, fields) => {
    if (!err) {
      //console.log(rows)
      res.render('home2', { title: 'Real Data', userData: rows, gmanufacturer });
    }
    else {
      console.log(err);
    }
  })
});

//this function handles the form submitted by the home2 page
//in this function, it calculate the car evaluation price
//by query in the db to get the corresponding assigned value by machine learning process for each manufacturer and model to be used in the calculation
//after calculation, it redirect to page /home/result to show the result
//req is the returned form parameter
router.get('/process_get', async (req, res) => {
  console.log('Request Come: ****************************')
  console.log(gmanufacturer)
  console.log(req.query)
  gmodel = req.query.model;
  gyear = req.query.year;
  godometer = req.query.odometer;
  var reference = "SELECT value FROM manufacturer WHERE name = '" + gmanufacturer + "'" + "; " + "SELECT value FROM model WHERE name = '" + gmodel + "'"
  mysqlConnection.query(reference, [1, 2], (err, rows, fields) => {
    if (!err) {
      //console.log(rows)
      //console.log(fields)
      var mmanufacturer = rows[0][0].value;
      var mmodel = rows[1][0].value;
      console.log(mmanufacturer)
      console.log(mmodel)
      console.log(gyear)
      console.log(godometer)
      gprice = Math.round(Math.abs((Number(gyear) - 1900) * 1061 + Number(mmanufacturer) * (-170) + Number(mmodel) * (-183) + (Number(godometer) / 5000) * 2.7 - 99660));
      console.log(gprice)
      res.redirect("/home/result");
    }
    else {
      console.log(err);
    }
  })
});

//this function handle the request to /home/result 
//is first shows the calculated estimate price
//then query into our db try to find some similar data to user input
//then send it to front to render the similar car info for user compare
router.get('/result', async (req, res) => {
  var sqlquery = "SELECT * from vehicles WHERE manufacturer = '" + gmanufacturer + "'" + " and model = '" + gmodel + "'" + " and year = '" + gyear + "'"
  var sqlquery2 = "SELECT * from vehicles WHERE manufacturer = '" + gmanufacturer + "'" + " and model = '" + gmodel + "'"
  //Query
  mysqlConnection.query(sqlquery, (err, rows, fields) => {
    if (!err) {
      //if result is not empty
      if (rows != "") {
        res.render('result', { title: 'Real Data', userData: rows, gprice });
      }
      else {
        mysqlConnection.query(sqlquery2, (err, rows, fields) => {
          if (!err) {
            res.render('result', { title: 'Real Data', userData: rows, gprice });
          }
          else {
            console.log(err);
          }
        })
      }
    }
    else {
      console.log(err);
    }
  })
});

/*table: manufacturer
name  text
value int
/*
/*table: model
name  text
value int
*/
/*table: vehicles
price        text
year         text
manufacturer text
model        text
odometer     text
image_url    text
id           double
*/

//export module router
module.exports = router;
