# Hack-The-North
E-Destination is an app designed to make recycling e-waste simple and rewarding.

To start the app, run app.py. 
terminal:
>python3 app.py

Design:

The data(currently dummy data is being used) is collected and stored in google's BigQuery SQL databased. 
In reference to the location the user chooses and model of the device or applicance they wish to recycle, a query will be generated that will order
the closest locations.

The cleaned and ordered data will be then sent to the flask front end that will be displayed to the user. 
