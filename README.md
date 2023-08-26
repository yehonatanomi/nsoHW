# nsoHW
I implemented the server with API's
 POST / AddMessage
 GET /GetMessage
 DELETE /DeleteMessage
I used  the controller repository service architecture , in the service i implements all the data things 
in the controller the server connection and the API's and the repository connect them.

## clone
Clone this repository to your local machine:

git clone https://github.com/yourusername/nsoHW.git

## requirements
to have all the library run this :
  pip install -r requirements.txt

## sql server 
you need a sql server , go to the env file and change it like this :
MYSQL_ROOT_PASSWORD=your_mysql_root_password
user=your_mysql_username
host=localhost


## run
to run the server : python controller.py
 
## test run
to run the test: python -m pytest

