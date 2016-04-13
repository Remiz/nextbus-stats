# Nextbus stats

This application collect the waiting time predictions of vehicles from [Nextbus API](http://www.nextbus.com/) and allow you to visualize the average waiting time by day of the week or hour.

Demonstration of the app is available at [nextbus-stats.tk](http://nextbus-stats.tk), it currently monitors the predictions for 2 streetcar routes in Toronto (510 Spadina and 512 St. Clair).

This project isn't really scientifically accurate but it can probably be extended for other uses, feel free to ad your suggestion in the issue tracker.

## Installation

A vagrant file is included in the project to create a functional environment, to use it follow these instructions

- Install [Vagrant](https://www.vagrantup.com/docs/installation/)
- Install [Ansible](http://docs.ansible.com/ansible/intro_installation.html) for the machine provisioning
- Run these commands:
```
cd nextbus-stats/vagrant/
vagrant up  # this may take a while
vagrant ssh
```
- Once in your Vagrant box
```
cd /vagrant
bower install
./manage.py migrate  # Initialize DB
./manage.py collectstatic  # Retrieve assets
./manage.py loadroutes  # Load routes information from API
./manage.py createsuperuser  # Create an admin user to access backend
```
- To run the different services
```
./manage.py runserver 0.0.0.0:8000  # Webserver
celery -A nextbusstats -B  # Celery worker (predictions collection)
```

## Usage

- The default transit agency is set to Toronto Transit Commission (TTC), if you want to change it, edit the settings.py file and change the AGENCY_TAG.
- Access the admin at http://127.0.0.1:8000/admin and manage the Routes. Pick the ones you want to monitor, **do not monitor too many routes at the same time or you'll trigger the rate limit of Nextbus API**.
- Access the frontend http://127.0.0.1:8000/ to visualize the routes performances once you collected enough data to see something interesting.