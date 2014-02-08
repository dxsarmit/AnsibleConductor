#!/bin/bash
#-H "Content-Type: application/json"
# curl -X POST \
#  -d 'data={ "path": "git/playbook.yml", "extra_vars":["key=val"],"tags":[], "skip_tags":[], "syntax_check": "False", "start_at" : "task"}' \
#   http://localhost:5000/run_playbook
curl -X POST \
 -d 'data={ "path": "/Users/jgoodwin/git/jwg.NorseFire/app/git/test.yml", "hosts" : "/Users/jgoodwin/git/jwg.NorseFire/app/git/hosts"}' \
  http://localhost:5000/run_playbook

# ansible-playbook ./git/test.yml -i hosts --extra-vars "key=val"
