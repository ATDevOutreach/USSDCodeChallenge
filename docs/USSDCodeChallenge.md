# USSD Code Challenge
## Due: 22nd June, 2018 or Earlier
#### This code challenge is due on the 22nd of June, 2018 or earlier. 

#### Task
- Create a USSD application, using the [Africa's Talking API](https://africastalking.com/) and [Simulator](), that has the following menus and sub menus:

| Menu           | Sub menu      |  
| -------------- |:-------------:|  
| My Cooperative | Check Balance |  
|                | Request Loan  |       
|                | Make Deposit  |       
|                |               |       
| Wazobia Loans  | Register      |       
|                | Repay Loan    |       
|                | Make Deposit  |       
|                | Request Loan  |       
|                | Request a Call|       
|                |               |       
| Join Agbetuntu |               |       
|                |               |       
| Request a Call |               |       

- Generate a USSD channel on the Sandbox and create your USSD App from [the USSD API](http://docs.africastalking.com/ussd)
- Connect the USSD Application to a database of your choice for maintaining state
- Host the database on a publicly available server(choose any including Heroku, Digital Ocean, Openshift) and place the callback with Africa's talking
- Implement the [Bank checkout API from Africa's Talking](http://docs.africastalking.com/bank/checkout) in the USSD App
- Implement the [voice API from Africa's Talking](http://docs.africastalking.com/voice)
- Run the application on [the Africa's Talking Simulator](https://simulator.africastalking.com:1517/)

#### Resources
- FAQs on Setting up the [Voice API](http://help.africastalking.com/voice)
- FAQs on setting up the [USSD API](http://help.africastalking.com/ussd)
- More on [Logging in, Signing up/Registration, Verifying/Activating your account, Managing Teams and applications](http://help.africastalking.com/website)
- Videos on getting started [on the Africa's Talking Sandbox](https://www.dropbox.com/sh/qq086503d5zaq7l/AADEo-oazNF_PgYIPRjPpeCua?dl=0)
- USSD Example Apps:
    - [PHP](https://github.com/JaniKibichi/microfinance-ussd-app), 
    - [Python-Django](https://github.com/RuthNjeri/Microfinance-ussd-django), 
    - [Python-Flask](https://github.com/Piusdan/USSD-Python-Demo),
    - [Ruby-Sinatra](https://github.com/JaniKibichi/sandbox-manenos/tree/master/ussd-rb), 
    - [Spark-Java](https://github.com/JaniKibichi/sandbox-manenos/tree/master/ussd-java)