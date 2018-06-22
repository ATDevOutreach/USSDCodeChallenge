<?php
    class JoinAgbetuntu
    {
        public function __construct() {
            // 
        }


        /*
         *  Join 
         *
         */
        public function joinAgbetuntu() {
            $ussd_text = "CON Coming soon!";
            ussd_proceed($ussd_text);
        }
    }

?>