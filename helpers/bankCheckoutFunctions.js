exports.initiateBankCheckout = (payments, bankList, opts, res) => {
    let response = `CON Select Your Bank
        1. Register
        2. Repay Loan
        3. Make Deposit
        4. Request Loan
        5. Request a Call`
    res.send(response)
    .then((data) => {
        let selectedBank = bankList[data.text - 1]
    })
    payments.bankCheckout(opts)
        .then(
            res.send('CON OTP code has been sent to authenticate transaction. Enter valid OTP')
        ).then((data) => {
           payments.va 
        })
        .catch(error);
}