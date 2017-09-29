#!/usr/bin/env php
<?php

# Configuration mode: return the custom metrics data should be defined
function config()
{
    $settings = [
        "maxruntime" => 5000, #  How long the script is allowed to run
        "period" => 60, # The period the script will run, in this case it will run every 60 seconds
        "metrics" => [
            [
                "id" => 0,
                "datatype" => "DOUBLE",
                "name" => "Random number",
                "description" => "Random number from 1 to 100",
                "groups" => "Statistics",
                "unit" => "ms",
                "tags" => "",
                "calctype" => "Instant"
            ],
            [
                "id" => 1,
                "datatype" => "DOUBLE",
                "name" => "Server time",
                "description" => "Current time in hours",
                "groups" => "Time",
                "unit" => "hours",
                "tags" => "",
                "calctype" => "Instant"
            ],
            [
                "id" => 2,
                "datatype" => "DOUBLE",
                "name" => "Server time",
                "description" => "Current time in minutes",
                "groups" => "Time",
                "unit" => "minutes",
                "tags" => "",
                "calctype" => "Instant"
            ]
        ]
    ];

    echo json_encode($settings).PHP_EOL;
}

# Data retrieval mode: return the data for the custom metrics
function data()
{
    echo "M1 ".rand(1, 100).PHP_EOL;
    echo "M2 ".date("G").PHP_EOL;
    echo "M3 ".date("i").PHP_EOL;
}

# Switch to check in which mode the script is running
switch($argv[1]) {
    case '-d':
        data();
        break;
    case '-c':
        config();
        break;
}
