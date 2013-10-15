pyBERGCloud
===========

Python library for building web application using the BERGCloud platform. 

How to test the example.

Setting up
    1. Download the directory 'googleAppEngine', inside 'Examples'
    2. Download the directory 'bergcloud', containing the library, and copy it into 'googleAppEngine'. 

GAE side
    3. Create a GAE webapp.
    4. Edit the 'app.yaml' file and change the application name to the one for the GAE webapp.
    5. Deploy the application.

    Notes:  
    'eventreceivergae' module and the example script file use indexed queries. It takes some time (even more then one hour) to GAE to upload index 
    information on the server. Please be patient. 


BERGCloud side
    6. On the BERGCloud developer website create a new product. Set the newly created GAE website as base URL.
    7. Create a new command with code ‘0’ and name ‘testcommand’ and a new event with code ‘0’ and name ‘testevent’.
    8. Save the settings. 

Arduino side
    9. Load the 'pyBERGCloudArduino' sketch (it's inside 'Examples/googleAppEngine') and edit it updating the ‘product id’ and the ‘command’ and ‘event’ codes.
    10. Upload the code into an (arduino) board with a BERGCloud devshield.
