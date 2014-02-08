#!/Users/jgoodwin/git/jwg.NorseFire/bin/python

from flask import Flask
from flask import request
from flask import jsonify
import json
import sys
import imp
sys.path.append('/Users/jgoodwin/git/jwg.ansible/lib/')
AP = imp.load_source('ansible-playbook','/Users/jgoodwin/git/jwg.ansible/bin/ansible_playbook')
import ansible
import subprocess

# sys.path.append('/Users/jgoodwin/git/jwg.ansible/bin/')
# print sys.path
# import ansible_playbook


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

def run(blob):
    argstring = json_to_argstring(blob)
    out = AP.main(argstring)
    blob['out'] = out
    return jsonify(blob)

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
    argstring.append('--syntax-check')
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
    "syntax_check" : boolean,
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
    return_obj['blob']=blob
    if safe_blob:
        return_obj['state']='started'
        run(blob)
        return jsonify(return_obj)
    else:
        return_obj['state']='failed'
        return jsonify(return_obj)


if __name__ == '__main__':
    app.debug = True
    app.run()
