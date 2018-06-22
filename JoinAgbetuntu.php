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
        public function joinAgbetuntu($details,$phone, $conne) {
            if (count($details)==1){   
                $ussd_text="CON \n Reply with your full name";
                ussd_proceed($ussd_text);
     
            } 
            else if(count($details) == 2){
                $ussd_text="CON Reply with your ID number\n";
                ussd_proceed($ussd_text);
            }
            else if(count($details) == 3){  
                $name=$details[1];
                $id_number=$details[2];
    
                //Validate and sanitize
                if(!filter_var($name, FILTER_SANITIZE_STRING) === TRUE){
                    $name = NULL;
                }
                
                if(!filter_var($id_number, FILTER_VALIDATE_INT) === TRUE){
                    $id_number = NULL;
                }
    
                // Save to database
                $sql = "INSERT INTO users (name, phonenumber, id_number) 
                        VALUES ('$name', '$phone', '$id_number')";
                if($conne->query($sql) == TRUE){
                    $ussd_text = "CON Registration success!";
                    ussd_proceed($ussd_text);
                }
                else{
                    echo "error: ".$sql ."\n" .$conne->error;
                }
            }  
        }
    }

?>