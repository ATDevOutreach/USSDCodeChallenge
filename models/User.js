const mongoose = require('mongoose')
// const _ = require('lodash')

var UserSchema = new mongoose.Schema({
  phoneNumber: {
    type: String,
    required: true,
    trim: true,
    minlength: 8,
    unique: true
  },
  sessionId: {
    type: String,
    required: true
  }
})

UserSchema.methods.toJSON = function () {
  var user = this
  var userObject = user.toObject()

  return _.pick(userObject, ['phoneNumber', 'session_id'])
}

let User = mongoose.model('Users', UserSchema)

module.exports = {
  User
}
