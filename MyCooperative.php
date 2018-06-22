<?php 
    class MyCooperative
    {
        public function __construct($details,$phone, $conne) {
            $this->phone = $phone;
            $this->conne = $conne;
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
            $sql = "SELECT * FROM account WHERE phonenumber LIKE '%".$this->phone."%'ORDER BY id DESC LIMIT 1";
            $result = $this->conne->query($sql);

            $newBal = 0.00; $newLoan = 0.00;

            if ($result->num_rows > 0) {
                $row = $result->fetch_assoc();
                //calculations
                $newBal = $row["balance"];
                $newLoan = $row["loan"];
                
            } else {
                $ussd_text = "No results";
                ussd_proceed($ussd_text);
            }
            
            $ussd_text = "CON Balance: ".$newBal."\nLoan: ".$newLoan."\n";
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