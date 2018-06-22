<?php
    class RequestACall
    {
        public function __construct($details,$phone, $conne) {
            $this->details = $details;
            $this->phone = $phone;
            $this->conne = $conne;
        }


        /*
         *  Request a call 
         *
         */
        public function requestACall() {
            $ussd_text = "END Please wait while we place your call.\n";

            require_once('config.php');

            //Make a call
            $from="+254723953897"; $to=$this->phone;
            // Create a new instance of our awesome gateway class
            $gateway = new AfricasTalkingGateway($username, $apikey);
            try { $gateway->call($from, $to); }
            catch ( AfricasTalkingGatewayException $e ){echo "Encountered an error when calling: ".$e->getMessage();}
            // Print the response onto the page so that our gateway can read it
            header('Content-type: text/plain');
            ussd_proceed($ussd_text); 
        }
    }

?>