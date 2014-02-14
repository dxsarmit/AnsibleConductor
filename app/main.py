#!/Users/jgoodwin/git/jwg.NorseFire/bin/python

import flask, json, sys, subprocess, os, time, md5
from flask import Flask
from flask import request
from flask import jsonify
from flask import Response

# Adding to our environment the required ansible path stuff
os.environ['PATH'] ='/Users/jgoodwin/git/jwg.ansible/bin:/Users/jgoodwin/git/jwg.NorseFire/bin:/Users/jgoodwin/.bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin'
os.environ['PYTHONPATH'] ='/Users/jgoodwin/git/jwg.ansible/lib:'
os.environ['ANSIBLE_LIBRARY'] = '/Users/jgoodwin/git/jwg.ansible/library'
os.environ['MANPATH'] = '/Users/jgoodwin/git/jwg.ansible/docs/man:'
# The path to our binary for ansible
playbook_path  = '/Users/jgoodwin/git/jwg.NorseFire/app/ansible/bin/ansible-playbook'

'''
This is the datastore for currently running playbooks.
When a playbook finishes it should remove itself from here & store itself in some 
persistant storage space.

This is a mapping of:
    "unique id" : playbook instance
    "md5.new(str(time.time()).hexdigest()" : {playbook instance}

save_playbook is to persist a pb into the hashmap
remove_playbook is to remove a pb from the mapping and persist to disk
'''
playbooks_requested = {}
# Saves to hashmap
def save_playbook(pb):
    playbooks_requested[pb.id]=pb
# Saves from hashmap to disk (NOT RIGHT NOW)

def remove_playbook(pb):
    playbooks_requested[pb.id]={}
    # TODO: actually un-instanciate that instance && persist to disk
    print 'DID NOT REMOVE; just deleted instance of class from hashmap'

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

'''
Converts a posted (safe) blob into an array, argarray, which will be executed as our ansible command
the ansible-playbook binary.
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

@app.route('/run_playbook', methods=['POST'])
def run_playbook():
    blob = json.loads(request.form['data'])
    '''
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
    safe_blob = True
    # convert the blob into a 'safe' blob
    # ie. check if we were sent bogus data
    for key in blob:
        if key in accepted_keys:
            safe_blob = safe_blob and True

        else:
            print 'key %s not found' % (key)
            print 'json rejcted'
            safe_blob = False

    response = {}
    response['blob']= blob
    # if its safe; make an argarray out of it
    # TODO: Need to find a way to do 400 (bad request)
    if safe_blob:
        argarray = json_to_argarray(blob)
        pb = playbook_request(argarray)
        print pb.args
        response['state']='started'
        # TODO: remove after finding better tests
        pb.set_id('foo')
        save_playbook(pb)
        response['request_id']=pb.id
        pb.run()
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

'''
Create a class.
Give class info from posted blob.
Class then has a .run()
Need to keep track of current running state in the instanciated class
'''

# TODO: Then save to disk once its done
class playbook_request():
    def __init__(self, args):
        id = md5.new(str(time.time())).hexdigest()
        self.output = []
        self.args = args
        self.id = id

    def run(self):
      proc = subprocess.Popen(
              [playbook_path] + self.args,
              stdout=subprocess.PIPE,
              stderr=subprocess.STDOUT,
              bufsize=-1
              )
      for line in iter(proc.stdout.readline, ''):
        line = line.rstrip()
        self.output = self.output + [line]

    def set_id(self, id):
        self.id = id

    def append_output(self, output, app):
        self.output = output.append(app)

if __name__ == '__main__':
    app.debug = True
    app.run(port=5001)
