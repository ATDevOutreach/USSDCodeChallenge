<?php
    // If this comment is removed the program will blow up! Watch out!

    // Ensure ths code runs only after a POST from AT
    if(TRUE){
        require_once('dbConnector.php');
        require_once('AfricasTalkingGateway.php');
        require_once('config.php');

        // Custom classes
        require_once('MyCooperative.php');
        require_once('WazobiaLoans.php');
        require_once('JoinAgbetuntu.php');
        require_once('RequestACall.php');

        // Receive the POST from AT
        // $sessionId     =$_POST['sessionId'];
        // $serviceCode   =$_POST['serviceCode'];
        // $phoneNumber   =$_POST['phoneNumber'];
        // $ussdString    =$_POST['text'];

        $phoneNumber = $_GET['MSISDN'];  
        $sessionId = $_GET['sessionId'];  
        $serviceCode = $_GET['serviceCode'];  
        $ussdString = $_GET['text'];

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
                    $myCooperative = new MyCooperative($ussdString_explode,$phoneNumber, $conn);
                    $myCooperative->myCooperative($ussdString_explode);
                    break;
                case 2:
                    $wazobiaLoan = new WazobiaLoans();
                    $wazobiaLoan->wazobiaLoans($ussdString_explode);
                    break;
                case 3: 
                    $join = new JoinAgbetuntu();
                    $join->joinAgbetuntu($ussdString_explode,$phoneNumber, $conn);
                    break;
                case 4:
                    $requestACall = new RequestAcall($ussdString_explode,$phoneNumber, $conn);
                    $requestACall->requestACall();
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