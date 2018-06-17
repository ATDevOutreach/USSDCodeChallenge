exports.initiateCall = (voice, dialerNumber, destPhoneNumber, callTextResponse, res) => {
  voice.call({
    callFrom: dialerNumber, // My AT virtual number
    callTo: destPhoneNumber
  })
    .then(function (call) {
      if (call.isActive == 1) {
        let response = '<?xml version="1.0" encoding="UTF-8"?>'
        response += '<Response>'
        response += '<Say>' + callTextResponse + '</Say>'
        response += '</Response>'
        res.send(response)
      }
      res.send(`END Call has been initiated successfully.
      Status: ${call.entries[0].status}
      You'd receive a call shortly.`)
    })
    .catch(function (error) {
      console.log(error.message)
    })
}
