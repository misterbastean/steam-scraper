const express         = require('express'),
      app             = express(),
      mongoose        = require('mongoose'),
      bodyParser      = require('body-parser'),
      config          = require('./config'),
      methodOverride  = require('method-override'),
      passport        = require('passport'),
      LocalStrategy   = require('passport-local');

// Require Routes
const indexRoutes = require('./routes/index'),
      authRoutes = require('./routes/auth')

mongoose.Promise = global.Promise;
mongoose.connect(`mongodb://${config.database.username}:${config.database.password}@${config.database.dbhost}`, {useNewUrlParser: true});
app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());
app.set('view engine', 'ejs');
app.use('/public', express.static(__dirname + '/public'));
app.use(methodOverride('_method'));

// Passport config
app.use(require('express-session')({secret: config.passport.secret, resave: false, saveUninitialized: false}));
app.use(passport.initialize());
app.use(passport.session());
// passport.use(new LocalStrategy(User.authenticate()));
// passport.serializeUser(User.serializeUser());
// passport.deserializeUser(User.deserializeUser());

// Routes
app.use(indexRoutes);
app.use(authRoutes);

// Port/IP Listening
const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log("SteamScrape frontend server started, listening on port", port);
})
