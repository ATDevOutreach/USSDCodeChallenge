var _ = require('lodash')

//= ==================== APP CONSTANTS
const message = 'I am a fisherman. I sleep all day and work all night!'
const myNumber = '+2348141919191'
// Your login credentials
const shortCode = '41919'
const username = 'sandbox'
const apikey = 'a5b2374285f235ef8b8822dd3c20ad981610dbfd2a127143a13d8832304b253c'
const options = {
  apiKey: apikey,
  username: username
}
const AfricasTalking = require('africastalking')(options)
const voice = AfricasTalking.VOICE;

exports.init= (req, res) => {
    //select needed properties from post object
  var body = _.pick(req.body, ['sessionId', 'serviceCode', 'phoneNumber', 'text'])

  if (body.text == '') {
    // This is the first request. Note how we start the response with CON
    let response = `CON What would you like to do
    1. My Co-operative
    2. Wazobia Loans
    3. Join Agbebuntu
    4. Request a call`
    res.send(response)
  } else if (body.text == '1') {
    // Logic for first level response 
    let response = `CON Select My Co-operative Option
    1. Check Balance
    2. Request Loan
    3. Make Deposit`
    res.send(response)
  } else if (body.text == '2') {
    // Logic for first level response
    let response = `CON Select My Co-operative Option
    1. Register
    2. Repay Loan
    3. Make Deposit
    4. Request Loan
    5. Request a Call`
    res.send(response)
  }else if (body.text == '3') {
    // Logic for first level response
    let response = `CON Select My Co-operative Option
    1. Register
    2. Repay Loan
    3. Make Deposit
    4. Request Loan
    5. Request a Call`
    res.send(response)
  }else if (body.text == '4') {
    // Logic for first level response
    let response = `END Initiating Call Request`
    res.send(response)

  } else if (body.text == '1*1') {
    // Business logic for first level response
    let accountNumber = 'ACC1001'
    // This is a terminal request. Note how we start the response with END
    let response = `END Your account number is ${accountNumber}`
    res.send(response)
    initiateCall(body.phoneNumber)
  } else if (body.text == '1*2') {
    // This is a second level response where the user selected 1 in the first instance
    let balance = 'NGN 10,000'
    // This is a terminal request. Note how we start the response with END
    let response = `END Your balance is ${balance}`
    res.send(response)
  } else {
    res.status(400).send('Bad request!')
}
}

function initiateCall (destPhoneNumber) {
  voice.call({
    callFrom: myNumber, // My AT virtual number
    callTo: destPhoneNumber 
  })
  .then(function(s) {
    // persist call Info
    console.log(s);
  })
  .catch(function(error) {
    console.log(error);
  });
}