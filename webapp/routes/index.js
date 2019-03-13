const express = require('express'),
      router = express.Router()

// Index Page
router.get('/', (req, res) => {
  res.send('Index page')
});

module.exports = router;
