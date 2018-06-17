const constants = require('./constants')
const callHandler = require('./callFunctions')
const bankCheckoutHandler = require('./bankCheckoutFunctions')
require('dotenv').config({ path: 'variables.env' })
const AfricasTalking = require('africastalking')(
  {
    apiKey: process.env.APIKEY,
    username: 'sandbox'
  }
)
const voice = AfricasTalking.VOICE
const payments = AfricasTalking.PAYMENTS
let selectedBank = ''
let accountNumber = ''
let userSelection = ''
let phoneNumber = ''
let transactionId = process.env.transactionId

exports.processUSSD = (body, res) => {
  phoneNumber = body.phoneNumber
  let seperatedBody = body.text.split('*')
  let userResponse = seperatedBody[seperatedBody.length - 1]
  console.log(body.text)
  if (userResponse.length == 10) {
    accountNumber = userResponse
    console.log(accountNumber)
    bankCheckoutHandler.initiateBankCheckout(payments, accountNumber, selectedBank, transactionId, res)
  } else if (body.text.length >= 16) {
    let seperatedBody = body.text.split('*')
    let otp = seperatedBody[seperatedBody.length - 1]
    console.log(process.env.transactionId, otp)
    if (process.env.transactionId != undefined) {
      bankCheckoutHandler.validateTransaction(payments, {
        transactionId: process.env.transactionId,
        otp: otp
      }, res)
    } else {
      res.send('END Something went wrong with your OTP generation.Please try again later')
    }
  } else {
    switch (body.text) {
      case '' : {
        // This is the first request. Note how we start the response with CON
        let response = `CON What would you like to do
           1. My Co-operative
           2. Wazobia Loans
           3. Join Agbetuntu
           4. Request a call`
        res.send(response)
        break
      }
      case '1' : {
        let response = `CON Select My Co-operative Option
              1. Check Balance
              2. Request Loan
              3. Make Deposit`
        res.send(response)
        break
      }
      case '2' : {
        let response = `CON Select Wazobia Loans Option
              1. Register
              2. Repay Loan
              3. Make Deposit
              4. Request Loan
              5. Request a Call`
        res.send(response)
        break
      }
      case '3' : {
        bankCheckoutHandler.selectBank(res)
        break
      }
      case '3*1':
      case '3*2':
      case '3*3':
      case '3*4':
      case '3*5': {
        userSelection = body.text.slice(-1)

        if (userSelection > 0 && userSelection <= 5) {
          selectedBank = constants.bankList[userSelection - 1]
          console.log(selectedBank)
          res.send('CON Enter your 10 digit Account Number')
        } else {
          res.send('END Wrong input')
        }
        break
      }
      case '4' : {
        callHandler.initiateCall(voice, constants.dialerNumber, phoneNumber, constants.callTextResponse, res)
        break
      }
      default : {
        res.send('END We will be implementing that in the near future. Watch out!')
        break
      }
    }
  }
}
