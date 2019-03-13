const express         = require('express'),
      app             = express(),
      mongoose        = require('mongoose'),
      bodyParser      = require('body-parser'),
      config          = require('./config'),
      methodOverride  = require('method-override'),
      passport        = require('passport'),
      LocalStrategy   = require('passport-local');




// Port/IP Listening
const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log("SteamScrape frontend server started, listening on port", port);
})
