#!/Users/jgoodwin/git/jwg.NorseFire/bin/python
import flask, json, sys, subprocess, os, time, md5

# TODO: Figure out how much of this we really need
# Adding to our environment the required ansible path stuff
os.environ['PATH'] ='/Users/jgoodwin/git/jwg.ansible/bin:/Users/jgoodwin/git/jwg.NorseFire/bin:/Users/jgoodwin/.bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin'
os.environ['PYTHONPATH'] ='/Users/jgoodwin/git/jwg.ansible/lib:'
os.environ['ANSIBLE_LIBRARY'] = '/Users/jgoodwin/git/jwg.ansible/library'
os.environ['MANPATH'] = '/Users/jgoodwin/git/jwg.ansible/docs/man:'
os.environ['PYTHONUNBUFFERED'] = 'True'
# The path to our binary for ansible
playbook_path  = '/Users/jgoodwin/git/jwg.NorseFire/app/ansible/bin/ansible-playbook'


'''
Create a class.
Give class info from posted blob.
Class then has a .run()
Need to keep track of current running state in the instanciated class
'''
directory = './NorseFireRuns'

# TODO: Pick a database
# TODO: Write output line storage function
# TODO: How do I run this as its own binary?
      # For like... atomic testing and such

def main(runid,ansibleargs):
  print '-'*100
  print 'Run Id:'
  print runid
  print 'Ansible args:'
  print ansibleargs
  print '-'*100
  pb = playbook_request(runid, ansibleargs)
  pb.run()

class playbook_request():
    def __init__(self, id, args):
        # id = md5.new(str(time.time())).hexdigest()
        # TODO: pass along the run id; maybe just date+time+playbook
              # or some unique counter for each playbook (more annoying)
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
              stderr=subprocess.STDOUT,
              # bufsize=-1,
              close_fds=True
              )

      for line in iter(proc.stdout.readline, ''):
        f.write(line)
        f.flush()


if __name__ == '__main__':
    runid = sys.argv[1]
    ansibleargs = sys.argv[2:]
    sys.exit(main(runid,ansibleargs))

'''
THIS IS DOCUMENTATION
Flag:
  Running:
    - True
    - False
Output:
  Blob of output lines... we'll figure that out later.
'''
