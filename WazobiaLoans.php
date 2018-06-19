<?php
    class WazobiaLoans
    {
        public function __construct() {
            // 
        }

        /*
         *  Controller function
         *
         */
        public function wazobiaLoans($details) {
            if (count($details) == 1) {
                $this->displaymenu();
            }

            if (count($details) > 1) {
                switch($details[1]) {
                    case 1: 
                        $this->register();
                        break;
                    case 2:
                        $this->repayLoan();
                        break;
                    case 3: 
                        $this->makeDeposit();
                        break;
                    case 4:
                        $this->requestLoan();
                        break;
                    case 4:
                        $this->requestCall();
                        break;
                    default:
                        $ussd_text = "Yikes! Watchout your choices.";
                        ussd_proceed($ussd_text);
                }
            }
        }


        /*
         *  Register
         *
         */
        public function register() {
            // 
        }


        /*
         *  Repay loan
         *
         */
        public function repayLoan() {
            // 
        }


        /*
         *  Make Deposit
         *
         */
        public function makeDeposit() {
            // 
        }


        /*
         *  Request Loan
         *
         */
        public function requestLoan() {
            // 
        }


        /*
         *  Request Call
         *
         */
        public function requestCall() {
            // 
        }


        /*
         *  Display sub menu
         *
         */
        public function displaymenu() {
            $ussd_text = "CON Wazobia Loans\n1. Register\n2. Repay Loan\n3. Make Deposit\n4. Request Loan\n5. Request Call";
            ussd_proceed($ussd_text);
        }
    }

?>