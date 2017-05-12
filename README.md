# Tournament Results
Udacity FSND Project - Build a Portfolio Site
---------------------
Python module using PostgreSQL database to keep track of players and matches in a game tournament.

The game tournament uses the Swiss system for pairing up players in each round:
* No player elimination
* Players are paired with equal (or close to) wins each round

## Requirements
* Python
* PostgreSQL
* Vagrant
* Virtual Box

## Usage
1. Ensure [Vagrant](https://www.vagrantup.com/), [Virtual Box](https://www.virtualbox.org/) and [Python](https://www.python.org/) are installed on your machine.
2. Clone the Udacity [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm)
3. Delete the `/tournament` directory in the clone.
4. [Clone](https://github.com/Jormangandur/udacity-fsnd-tournament.git) (or [download](https://github.com/Jormangandur/udacity-fsnd-tournament/archive/master.zip)) this repo into the `/vagrant` directory.
5. Open the `/vagrant` directory in the command line
6. Launch the VM:
  * `vagrant$ vagrant up`
7. SSH into the VM:
  * On Mac/Linux `vagrant$ vagrant ssh`
    * Gives SSH connection details on windows
  * Windows use Putty or similar SSH client
8. In the VM navigate to the `/vagrant/tournament` directory:
  * `$ cd /vagrant/tournament`
9. Run python scripts:
  * `$ python tournament.py`
  * `$ python tournament_test.py`

## File Description
 * `tournament.sql`: PostgreSQL database schema
 * `tournament.py`: Python module with functions to interact with the database.
 * `tournament_test.py`: Unit tests.
