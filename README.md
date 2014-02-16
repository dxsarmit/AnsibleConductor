Conductor
=========

A simple flask  API wrapper for Ansible. Conductor provides a HTTP interface for running your playbooks, and real time output of the results.

Things Conductor does not have yet, but really wants to have:
1. Dynamic hosts file support
2. Ad-hoc task creation and execution
3. A web UI
4. A simple installer

## Installation
These are roughly from memory
```
git clone git@github.com/jonathanwgoodwin/AnsibleConductor.git Conductor
cd Conductor
virtualenv .
source bin/activate
pip install flask
cd app
git clone git@github.com/ansible/ansible.git ansible
git clone git@github.com/[ USERNAME ]/[ Ansible Playbook Repo ].git git
```

## To Do's
1. Get internet on the train so I do not have to use this file
2. Use github Issues / Milestones
3. Fix the finding of stuff in the app/git/ folder
4. Figure out what the dependencies are and write an install script
5. Have some sort of 'fast' in memory list of what tasks are running right now.
   On top of this; have some way of pushing updates to clients without having
them poll every .1s 
6. Find a way to respond when things break with the appropriate http request
   code.
7. Put the running of the playbook (main.py) inside a try block.
8. Write header and footer to file as JSON
9. Find a way to color output (output will probably not come w/ color code if
   the output is not a tty, this is probably a javascript problem.


## Running the app
```
cd app
./main.py
```
Now you can `curl` json at localhost:5001 and start Conducting!


## Contributing
I'm not sure what to put here yet.

## License
I need to learn how / what to put here
