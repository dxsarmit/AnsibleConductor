#!/bin/bash
#-H "Content-Type: application/json"
# curl -X POST \
#  -d 'data={ "path": "git/playbook.yml", "extra_vars":["key=val"],"tags":[], "skip_tags":[], "syntax_check": "False", "start_at" : "task"}' \
#   http://localhost:5001/run_playbook
####
# Testing main.py
####
curl -X POST http://localhost:5001/run_playbook -d 'data={ "path": "/Users/jgoodwin/git/jwg.Conductor/app/git/test.yml", "hosts" : "/Users/jgoodwin/git/jwg.Conductor/app/git/hosts"}' &
# ansible-playbook ./git/test.yml -i hosts --extra-vars "key=val"
# sleep 2
# curl -X POST http://localhost:5001/run_status -d 'data={ "id": "foo" }'

####
# Testing Conductor.py
####
# ./Conductor.py 'SomeRunId' '/Users/jgoodwin/git/jwg.Conductor/app/git/test.yml' '-i' '/Users/jgoodwin/git/jwg.Conductor/app/git/hosts' &
# sleep 1
# tail -f ./ConductorRuns/foo

# ansible-playbook /Users/jgoodwin/git/jwg.Conductor/app/git/test.yml -i /Users/jgoodwin/git/jwg.Conductor/app/git/hosts
