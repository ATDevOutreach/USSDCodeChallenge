<?php
    // Ensure ths code runs only after a POST from AT
    if(!empty($_POST) && !empty($_POST['phoneNumber'])){
        require_once('dbConnector.php');
        require_once('AfricasTalkingGateway.php');
        require_once('config.php');

        // Custom classes
        require_once('MyCooperative.php');
        require_once('WazobiaLoans.php');

        // Receive the POST from AT
        $sessionId     =$_POST['sessionId'];
        $serviceCode   =$_POST['serviceCode'];
        $phoneNumber   =$_POST['phoneNumber'];
        $ussdString    =$_POST['text'];

        $level =0; 

        if($ussdString != ""){  
            $ussdString=  str_replace("#", "*", $ussdString);  
            $ussdString_explode = explode("*", $ussdString);
            $level = count($ussdString_explode);  
        }

        //echo ussd_text
        function ussd_proceed ($ussd_text){  
            echo $ussd_text;  
            //exit(0);  
        }

        if ($level==0){				
            displaymenu();
        } 
        
        elseif ($level > 0) {
            switch ($ussdString_explode[0]) {
                case 1: 
                    $myCooperative = new MyCooperative();
                    $myCooperative->myCooperative($ussdString_explode);
                    break;
                case 2:
                    $wazobiaLoan = new WazobiaLoans();
                    $wazobiaLoan->wazobiaLoans($ussdString_explode);
                    break;
                case 3: 
                    break;
                case 4:
                    break;
                default:
                    $ussd_text = "Yikes! Invalid choice.";
                    ussd_proceed($ussd_text);
            }
        }
    }

    // Main menu
    function displaymenu() {             
        $ussd_text="CON \n1: My Cooperative\n2: Wazobia Loans\n3: Join Agbetuntu\n4: Request a call";  
        ussd_proceed($ussd_text);  
    }

?>