var _ = require('lodash')
var { User } = require('../models/User')
var ussdHandler = require('../helpers/ussdProcessor')

exports.init = (req, res) => {
// Select needed properties from post object
  var body = _.pick(req.body, ['sessionId', 'serviceCode', 'phoneNumber', 'text'])

  // Authenticate User
  // Check if session exists
  var query = User.find({ 'sessionId': body.sessionId })
  if (!query) {
    var user = new User(body)
    user.save()
      .then(() => {
        console.log('User Saved successfully')
      }).catch((e) => {
        console.log(e.message)
      })
  }

  ussdHandler.processUSSD(body, res)
}
