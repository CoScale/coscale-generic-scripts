// Configuration mode: return the custom metrics data should be defined
function config()
{
    var settings = {
        "maxruntime": 5000, //  How long the script is allowed to run
        "period": 60, // The period the script will run, in this case it will run every 60 seconds
        "metrics": [
            {
                "id": 1,
                "datatype": "DOUBLE",
                "name": "Testmetric 1",
                "description": "An example description",
                "groups": "Statistics",
                "unit": "",
                "tags": "",
                "calctype": "Instant"
            },
            {
                "id": 2,
                "datatype": "DOUBLE",
                "name": "Testmetric 2",
                "description": "An example description",
                "groups": "Statistics",
                "unit": "",
                "tags": "",
                "calctype": "Instant"
            },
            {
                "id": 3,
                "datatype": "DOUBLE",
                "name": "Testmetric 3",
                "description": "An example description",
                "groups": "Statistics",
                "unit": "",
                "tags": "",
                "calctype": "Instant"
            }
        ]
    };

    console.log(JSON.stringify(settings));
}

// Data retrieval mode: return the data for the custom metrics
function data()
{
    console.log("M1 " + Math.random(1, 100));
    console.log("M2 " + Math.random(1, 100));
    console.log("M3 " + Math.random(1, 100));
}

// Switch to check in which mode the script is running
switch (process.argv[2]) {
    case '-d':
        data();
        break;
    case '-c':
        config();
        break;
}
