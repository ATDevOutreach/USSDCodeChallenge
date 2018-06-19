<?php 
    class MyCooperative
    {
        public function __construct() {
            // 
        }

        public function displaymenu () {
            $ussd_text = "CON My Cooperative\n1. Check Balance\n2. Request Loan\n3. Make Deposit";
            ussd_proceed($ussd_text);
        }

        public function myCooperative() {
            if (count($details) == 1) {
                switch($ussdString_explode[1]) {
                    case 1:
                        $ussd_text = "END Your balance is $400,000,888";
                        ussd_proceed($ussd_text);
                        break;
                    case 2:
                        break;
                    case 3:
                        break;
                    default:
                        break;
                }
            }
        }
    }

?>