#!/Users/jgoodwin/git/jwg.NorseFire/bin/python
import json, sys, subprocess, os, time, md5
'''
THIS IS DOCUMENTATION

This python binary file expects to be run from the command line.
sys.argv = [ 0:0 BinaryName,
             1:1 RunId
             2:- The argstring we're running against ansible-playbook ]


'''
# TODO: Figure out how much of this we really need
      # Adding to our environment the required ansible path stuff
os.environ['PATH'] ='/Users/jgoodwin/git/jwg.ansible/bin:/Users/jgoodwin/git/jwg.NorseFire/bin:/Users/jgoodwin/.bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin'
os.environ['PYTHONPATH'] ='/Users/jgoodwin/git/jwg.ansible/lib:'
os.environ['ANSIBLE_LIBRARY'] = '/Users/jgoodwin/git/jwg.ansible/library'
os.environ['MANPATH'] = '/Users/jgoodwin/git/jwg.ansible/docs/man:'
# This is mandatory
os.environ['PYTHONUNBUFFERED'] = 'True'
# The path to our binary for ansible
playbook_path  = '/Users/jgoodwin/git/jwg.NorseFire/app/ansible/bin/ansible-playbook'


directory = './NorseFireRuns'

def main(runid,ansibleargs):
  print '-'*100
  print 'Run Id:'
  print runid
  print 'Ansible args:'
  print ansibleargs
  print '-'*100
  pb = playbook_request(runid, ansibleargs)
  pb.run()

'''
THIS IS DOCUMENTATION

A Playbook Request is a (unique) pair of (id,args).
playbook_request.run(self):
Creates a subprocess that runs the requestd ansible command and writes its output to a file
'''

class playbook_request():
    def __init__(self, id, args):
        # TODO: pass along the run id; maybe just date+time+playbook
              # or some unique counter for each playbook (more annoying)
              # id = md5.new(str(time.time())).hexdigest()
        self.id = runid
        self.args = args
        if not os.path.exists(directory):
          os.makedirs(directory)
          if not os.path.exists(directory+'/'+id):
            os.makedirs(directory+'/'+id)

    def run(self):
      f = open(directory+'/'+self.id, 'a+')
      proc = subprocess.Popen(
              [playbook_path] + self.args,
              stdout=subprocess.PIPE,
              stderr=subprocess.STDOUT
              )
      # TODO: handle '' and then write an indication to the end of the file that the run is over.
      for line in iter(proc.stdout.readline, ''):
        f.write(line)
        f.flush()


if __name__ == '__main__':
    runid = sys.argv[1]
    ansibleargs = sys.argv[2:]
    sys.exit(main(runid,ansibleargs))
