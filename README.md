# nextbus-stats
Collecting prediction from nextbus API and analyzing route efficiency over time.

A celery process is collecting the prediction of each stop for monitored route. A web interface allows to visualize all the predictions in a graph and to compare various factors like day of the week or hour of the day (more to come).

This project isn't really scientifically accurate but probably can be extended for other uses, feel free to add a suggestion in the issue tracker if you think of something.

## Requirements/Setup

For local development/deployment you can use the Vagrant configuration file with the Ansible provisioning file (in /vagrant/).

Once you have both installed, use your terminal and go within nextbusstats/vagrant/ and type `vagrant up`.
It should take a while and install all the required packages within a virtual machine (Ubuntu Trusty 64). Once it's completed type `vagrant ssh` and you should be able to launch the app from within the VM.

Once you are within the virtual machine you can use the following commands:
```
cd /vagrant
./manage.py migrate  # To initialize the database
./manage loadroutes  # To load the routes information from the NextBus API
./manage runserver 0.0.0.0:8000  # To run the Django local development server
celery -A nextbusstats -B  # To run the Celery worker which collect the predictions
```

## Important notes
- The default Agency is set to Toronto Transit Commission (TTC), but you can change it in the settings.py file to any agency supported by Nextbus.
- To start monitoring a route it needs to be flagged as "monitored". You can create and admin with the command `./manage.py createsuperuser` then access the admin interface at 127.0.0.1:8000/admin
- Do not monitor too many routes at the same time, it will triggers too many calls to Nextbus API and get your IP banned


