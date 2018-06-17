require('dotenv').config({ path: 'variables.env' })
exports.selectBank = (res) => {
  let response = `CON Select Your Bank
        1. FCMB
        2. Zenith Bank
        3. Access Bank
        4. Providus Nigeria
        5. Sterling Nigeria`
  res.send(response)
}

exports.initiateBankCheckout = (payments, accountNumber, selectedBank, transactionId, res) => {
  let bankCheckoutOptions = {
    'username': 'sandbox',
    'productName': 'Agbetuntu',
    'bankAccount': {
      'accountName': 'Your Test Account',
      'accountNumber': '1231231231',
      'bankCode': 234001,
      'dateOfBirth': '2017-11-22'
    },
    'currencyCode': 'NGN',
    'amount': 500.5,
    'narration': 'Join Agbebuntu Fee'
  }
  payments.bankCheckout(bankCheckoutOptions)
    .then((data) => {
      process.env.transactionId = data.transactionId
      console.log(data)
      res.send(`CON OTP code for transaction of ID: ${transactionId} has been sent.
       Current status: ${data.description}.
       Kindly enter your OTP Code to validate transaction`)
    })
    .catch((e) => {
      console.log(e)
      res.send('END Oooooops!!! Your OTP Generation has failed at this time. Try again later')
      console.log(e.message)
    }
    )
}

exports.validateTransaction = (payments, validationOptions, res) => {
  payments.validateBankCheckout(validationOptions)
    .then((data) => {
      res.send(`END Validation ${data.status}
      ${data.description}`)
    })
    .catch((e) => {
      res.send('END OTP validation failed')
    })
}
