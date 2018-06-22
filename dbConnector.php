<?php 
//theUssdDb.php
//Connection Credentials
$servername = 'localhost';
$username = 'root';
$password = "";
$database = "ussdcodechallenge";
$dbport = 3306;
    // Create connection
    $conn = new mysqli($servername, $username, $password, $database, $dbport);
    // Check connection
    if ($conn->connect_error) {
        header('Content-type: text/plain');
        //log error to file/db $e-getMessage()
        die("END An error was encountered. Please try again later");
    } 
    //echo "Connected successfully (".$db->host_info.")";
?>