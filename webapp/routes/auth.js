const express = require('express'),
      router = express.Router()

// Show register form
router.get('/register', (req, res) => {
  res.send('Register page')
});

module.exports = router;
