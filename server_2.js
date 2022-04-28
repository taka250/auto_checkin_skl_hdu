var express = require("express");
var app = express();
var des = require("./des");
var upwd = "";
app.get("/", function (req, res) {
  var a = req.query;
  if (a["lt"] && a["upwd"]) {
    var rsa = des(a["upwd"] + a["lt"], "1", "2", "3");
    res.send(rsa);
  }
});

var server = app.listen(2022);
