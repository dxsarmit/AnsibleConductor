#!/Users/jgoodwin/git/jwg.Conductor/bin/python
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
os.environ['PYTHONPATH'] = './ansible/lib:'
os.environ['ANSIBLE_LIBRARY'] = './ansible/library'
# This is mandatory
os.environ['PYTHONUNBUFFERED'] = 'True'
# The path to our binary for ansible
playbookpath  = './ansible/bin/ansible-playbook'
runsdir= './ConductorRuns'

def main(runid, ansibleargs):
  pb = playbook_request(runid, ansibleargs)
  pb.run()

'''
THIS IS DOCUMENTATION

A Playbook Request is a (unique) pair of (id,args).
playbook_request.run(self):
Creates a subprocess that runs the requestd ansible command and writes its output to a file
'''

# Function: writes the header to our run files
          # expects an open file handle

class playbook_request():
    def __init__(self, id, args):
        self.id = runid
        self.args = args
        self.starttime = time.time()
        if not os.path.exists(runsdir):
          os.makedirs(runsdir)
          if not os.path.exists(runsdir+'/'+id):
            os.makedirs(runsdir+'/'+id)

    def run(self):
      f = open(runsdir+'/'+self.id, 'w+')
      self.write_header(f)
      proc = subprocess.Popen(
              [playbookpath] + self.args,
              stdout=subprocess.PIPE,
              stderr=subprocess.STDOUT
              )
      # TODO: handle '' and then write an indication to the end of the file that the run is over.
      for line in iter(proc.stdout.readline, ''):
        f.write(line)
        f.flush()
      self.write_footer(f)

    def write_header(self, F):
        bar = '-'*100+'\n'
        F.write(bar)
        F.write('Run Id: ' + self.id + '\n')
        F.write('Ansible args: ' + str(self.args) + '\n')
        F.write('Start Time: ' + str(self.starttime) + '\n')
        F.write(bar)
    def write_footer(self, F):
        finishtime = time.time()
        bar = '-'*100+'\n'
        F.write(bar)
        F.write('Run Id: ' + self.id + '\n')
        F.write('Ansible args: ' + str(self.args) + '\n')
        F.write('Stop Time: ' + str(finishtime) + '\n')
        F.write('Seconds Taken: ' + str(finishtime - self.starttime) + '\n')
        F.write(bar)

if __name__ == '__main__':
    runid = sys.argv[1]
    ansibleargs = sys.argv[2:]
    sys.exit(main(runid,ansibleargs))
