#!/Users/jgoodwin/git/jwg.NorseFire/bin/python
import flask, json, sys, subprocess, os, time, md5
from flask import Flask
from flask import request
from flask import jsonify
from flask import Response

app=Flask(__name__)
# List of the keys we accept in our blog
accepted_keys = [ "path",
        "hosts",
        "extra_vars",
        "tags",
        "skip_tags",
        "syntax_check",
        "step",
        "start_at"
        ]
# Map of key names to command line flags 
flag_map = { "hosts" : "-i",
        "extra_vars" : "--extra-vars",
        "tags" : "--tags",
        "skip_tags" : "--skip-tags",
        "syntax_check" : "--syntax-check",
        "start_at" : "--start-at"
        }

'''
THIS IS DOCUMENTATION
Converts a posted (safe) blob into an array called argarray,
which will be executed as our ansible command the ansible-playbook binary.
'''
def json_to_argarray(blob):
    argarray = []
    for key in accepted_keys:
        if key in blob:
            val = blob[key]
            if key == 'path':
                argarray.append(val)
            elif key == 'syntax_check' and val:
                argarray.append('--syntax-check')
            else:
                prefix = flag_map[key]
                argarray.append(prefix)
                argarray.append(val)
    return argarray
def check_blob(blob):
    safe_blob = True
    for key in blob:
        if key in accepted_keys:
            safe_blob = safe_blob and True

        else:
            print 'key %s not found' % (key)
            print 'json rejcted'
            safe_blob = False
            break

@app.route('/run_playbook', methods=['POST'])
def run_playbook():
    blob = json.loads(request.form['data'])
    '''
    THIS IS DOCUMENTATION
    {
    "path" :"/path/to/playbook",
    "hosts":"/path/to/hosts/file",
    "extra_vars" : [ "key=val", "key2=val2" ],
    "tags" : [ "tags", "list" ]
    "skip_tags" : ["also", "a", "list"],
    "syntax_check" : boolean,
    "step" : "NOT SUPPORTED"
    "start_at" : "task_name"
    }
    '''

    response = {}
    response['blob']= blob
    # If blob is safe; make an argarray out of it
    # TODO: Need to find a way to do 400 (bad request)
    # TODO: make this a try block
    if safe_blob:
        argarray = json_to_argarray(blob)
        response['state']='started'
        # TODO: we need to set the ID of the run before we pass it off to the runner
              # because we need to know how to look up what we were running... :/
        response['request_id']=pb.id
        # TODO: Run ansible using NorseFire.py
              # subprocess.popen(stuff)
        return jsonify(response)
    else:
        response['state']='incorrect blob format'
        return jsonify(return_obj)

@app.route('/run_status', methods=['post'])
def run_status():
    blob = json.loads(request.form['data'])
    response = {}
    if blob['id'] in playbooks_requested:
        response['output'] = playbooks_requested[blob['id']].output
    else:
        response['output'] = []
        response['state'] = 'did not find request'
    return jsonify(response)

# TODO: Then save to disk once its done
if __name__ == '__main__':
    app.debug = True
    app.run(port=5001)
