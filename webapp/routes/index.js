const express = require('express'),
      router = express.Router()

// Index Page
router.get('/', (req, res) => {
  res.render('index')
});

// User Page
router.get('/user', (req, res) => {
  res.send('user page')
});

module.exports = router;
