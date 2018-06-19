<?php 
    class MyCooperative
    {
        public function __construct() {
            // 
        }

        /*
         *  Controller function
         *
         */
        public function myCooperative($details) {
            if (count($details) == 1) {                
                $this->displaymenu();
            }

            if (count($details) == 2){

                switch($details[1]) {
                    case 1:
                        $this->checkBalance();
                        break;
                    case 2:
                        $this->requestLoan();
                        break;
                    case 3:
                        $this->makeDeposit();
                        break;
                    default:
                        break;
                }

            }
        }

        /*
         *  Display sub menu
         *
         */
        public function displaymenu () {
            $ussd_text = "CON My Cooperative\n1. Check Balance\n2. Request Loan\n3. Make Deposit";
            ussd_proceed($ussd_text);
        }

        /*
         *  Function to check Balance
         *
         */
        public function checkBalance() {
            $ussd_text = "END Your balance is $400,000,888";
            ussd_proceed($ussd_text); 
        }

        /*
         *  Function to request a loan
         *
         */
        public function requestLoan() {
            // 
        }

        /*
         *  Function to make a deposit
         *
         */
        public function makeDeposit() {
            // 
        }
    }

?>