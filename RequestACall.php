<?php
    class RequestACall
    {
        public function __construct() {
            // 
        }


        /*
         *  Request a call 
         *
         */
        public function requestACall() {
            // Specify your Africa's Talking phone number in international format
            $from = "+254723953897";
            // Specify the numbers that you want to call to in a comma-separated list
            // Please ensure you include the country code (+254 for Kenya in this case)
            $to   = "+254728938138";
            // Create a new instance of our awesome gateway class
            $gateway = new AfricasTalkingGateway($username, $apikey);
            /*************************************************************************************
             NOTE: If connecting to the sandbox:
            1. Use "sandbox" as the username
            2. Use the apiKey generated from your sandbox application
                https://account.africastalking.com/apps/sandbox/settings/key
            3. Add the "sandbox" flag to the constructor
            $gateway  = new AfricasTalkingGateway($username, $apiKey, "sandbox");
            **************************************************************************************/
            // Any gateway errors will be captured by our custom Exception class below, 
            // so wrap the call in a try-catch block
            try 
            {
            // Make the call
            $results = $gateway->call($from, $to);
            //This will loop through all the numbers you requested to be called
            foreach($results as $result) {
                // //Only status "Queued" means the call was successfully placed
                // echo $result->status;
                // echo $result->phoneNumber;
                // echo "<br/>";
            }
                    
            }
            catch ( AfricasTalkingGatewayException $e )
            {
            echo "Encountered an error while making the call: ".$e->getMessage();
            }
            // DONE!!! 
                    }
                }

?>