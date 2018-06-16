exports.initiateCall = (voice, dialerNumber, destPhoneNumber, callTextResponse) => {
  voice.call({
    callFrom: dialerNumber, // My AT virtual number
    callTo: destPhoneNumber
  })
    .then(function (call) {
      // persist call Info
      if (call.isActive == 1) {
        let response = '<?xml version="1.0" encoding="UTF-8"?>'
        response += '<Response>'
        response += '<Say>' + callTextResponse + '</Say>'
        response += '</Response>'
        res.send(response)
      }
      console.log(...call.entries)
    })
    .catch(function (error) {
      console.log(error.message)
    })
}
