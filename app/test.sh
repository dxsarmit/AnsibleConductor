#!/bin/bash
#-H "Content-Type: application/json"
# curl -X POST \
#  -d 'data={ "path": "git/playbook.yml", "extra_vars":["key=val"],"tags":[], "skip_tags":[], "syntax_check": "False", "start_at" : "task"}' \
#   http://localhost:5001/run_playbook
curl -X POST http://localhost:5001/run_playbook \
 -d 'data={ "path": "/Users/jgoodwin/git/jwg.NorseFire/app/git/test.yml", "hosts" : "/Users/jgoodwin/git/jwg.NorseFire/app/git/hosts"}' &
# ansible-playbook ./git/test.yml -i hosts --extra-vars "key=val"
curl -X POST http://localhost:5001/run_status -d 'data={ "id": "foo" }'



