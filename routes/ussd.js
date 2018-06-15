var express = require('express');

var router = express.Router();
var ussd = require('../controllers/ussdController')


/* POST users listing. */
router.post('/', ussd.init);

module.exports = router;
