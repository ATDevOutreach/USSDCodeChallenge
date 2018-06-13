# USSD Code Challenge [Lagos, Nigeria]
## Due: 22nd June 2018 or Earlier
#### This code challenge is due on the 22nd of June or earlier. 

## Simple Unchanging Rules
The code challenge is and will always be judged using the following criteria
  - A Correct fork, branch and pull request
  - Using the GitHub Pull Request Time Stamp and correct code quality & structure, the first developer whose code runs successfully on the sandbox/simulator wins
  - Other developers who submit successfully MAY also get rewarded with secondary items
  - Code quality and structure will be evaluated
  - The order for pull requests will be followed, first come first win basis!
  - Do not share any code that you cannot opensource on the Git Repository as its open source and Africa's Talking will not be liable for any breach of intellectual property (if any) once shared on the platform.

## Terms and Conditions
You can participate on as many challenges as you wish:
  - Everyone can participate for secondary prices, BUT the winner must reside in Lagos, and have Nigerian citizenship 
  - Africa's Talking reserves the right to announce the winners
  - Africa's Talking reserves the right to reward the winners based on Africa's Talking Criterion
  - Do not share any code that you cannot opensource on the Git Repository as its open source and Africa's Talking will not be liable for any breach of intellectual property (if any) once shared on the platform.
  - Code Challenges are time bound - the time restriction is specified on the challenge
  - Additional rules MAY be provided on the code challenge and will vary for each challenge
  - You are free to use all manner of tools
  - Successive interviews for projects MAY be run to satisfy participating Africa's Talking Partners

## Code Challenge Bounty:
  - Project worth 300$ for USSD App creation + Deployment
  - Possible developer job based on completion of USSD App
  - Airtime and Swag for the first 100 successful participants

## Task
- Create a USSD application, using the [Africa's Talking API](https://africastalking.com/) and [Simulator](https://simulator.africastalking.com:1517/), that has the following menus and sub menus:

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
- Use the format for submitting your code outlined [here](http://atdevoutreach.viewdocs.io/USSDCodeChallenge/USSDCodeChallengeSteps/) to submit your solution
- Make sure when creating a branch to use your correct phone Number, as this is what we will use to get back to you. NB: As a branch-name you can also use your email.

## Resources
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
- [Medium Post on Building USSD Apps using JS + Africa's Talking APIs](https://medium.com/@jalasem/ussd-app-development-with-javascript-a59554e16a03)
- [Medium Post on USSD+BankPayments+Airtime APIs on Africa's Talking for Nigeria](https://medium.com/@lizkathure/68f9503bed81)

## About Africa's Talking Code Challenges
Please read the overview [here.](http://atdevoutreach.viewdocs.io/USSDCodeChallenge/)


## Get Support on the Africa's Talking Slack
In case you have any questions, join our Slack [here](https://slackin-africastalking.now.sh/)
