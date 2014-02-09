#!/Users/jgoodwin/git/jwg.NorseFire/bin/python

from flask import Flask
import flask
from flask import request
from flask import jsonify
from flask import Response
import json
import sys
import imp
import subprocess
import os
import time


'''

Need to create a class.
Give class info from posted blob.
Class then has a .run()
Need to keep track of current running state in the instanciated class
Then save to disk once its done

'''

os.environ['PATH'] ='/Users/jgoodwin/git/jwg.ansible/bin:/Users/jgoodwin/git/jwg.NorseFire/bin:/Users/jgoodwin/.bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin'
os.environ['PYTHONPATH'] ='/Users/jgoodwin/git/jwg.ansible/lib:'
os.environ['ANSIBLE_LIBRARY'] = '/Users/jgoodwin/git/jwg.ansible/library'
os.environ['MANPATH'] = '/Users/jgoodwin/git/jwg.ansible/docs/man:'


app=Flask(__name__)
accepted_keys = [ "path",
        "hosts",
        "extra_vars",
        "tags",
        "skip_tags",
        "syntax_check",
        "step",
        "start_at"
        ]

flag_map = { "hosts" : "-i",
        "extra_vars" : "--extra-vars",
        "tags" : "--tags",
        "skip_tags" : "--skip-tags",
        "syntax_check" : "--syntax-check",
        "start_at" : "--start-at"
        }

playbook_path  = '/Users/jgoodwin/git/jwg.NorseFire/app/ansible/bin/ansible-playbook'

def run(blob):
    '''
    Here we will subprocess.Popen and such
    '''

'''
Converts a posted (safe) blob into an argstring for execution against
the ansible-playbook binary.
'''
def json_to_argstring(blob):
    argstring = []
    for key in accepted_keys:
        if key in blob:
            val = blob[key]
            if key == 'path':
                argstring.append(val)
            else:
                prefix = flag_map[key]
                argstring.append(prefix)
                argstring.append(val)
    # argstring.append('--syntax-check')
    return argstring

@app.route('/run_playbook', methods=['POST'])
def run_playbook():
    blob = json.loads(request.form['data'])
    '''
    { "path" :"/path/to/playbook",
      "hosts":"/path/to/hosts/file",
    "extra_vars" : [ "key=val", "key2=val2" ],
    "tags" : [ "tags", "list" ]
    "skip_tags" : ["also", "a", "list"],
    # "syntax_check" : boolean,
    "step" : "NOT SUPPORTED"
    "start_at" : "task_name" }
    '''
    safe_blob = True
    for key in blob:
        if key in accepted_keys:
            safe_blob = safe_blob and True

        else:
            print 'key %s not found' % (key)
            print 'json rejcted'
            safe_blob = False

    return_obj = {}
    return_obj['blob']= blob
    if safe_blob:
        argstring = json_to_argstring(blob)
        return_obj['state']='started'
        '''
        Here goes the streaming output part
        '''
        def runner():
            proc = subprocess.Popen(
                [playbook_path]+ argstring,
                    # shell = True, # Paul says no; no bash for you
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                   bufsize=-1
            )

            for line in iter(proc.stdout.readline, ''): # Paul says yes
                yield line.rstrip()

        return flask.Response(runner(), mimetype='text/html')




    else:
        return_obj['state']='incorrect blob format'
        return jsonify(return_obj)


if __name__ == '__main__':
    app.debug = True
    app.run()
