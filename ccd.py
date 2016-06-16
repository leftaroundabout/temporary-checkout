#!/usr/bin/env python2

import subprocess
import sys
import signal
import os
from os import path
import json

if __name__ == "__main__":
   if len(sys.argv) < 2:
      sys.exit(0)
   else:
      lntgt = sys.argv[1]

      reponame = path.basename(lntgt)
      
      ccdTmpdir = "/tmp/ccd"
      if not path.exists(ccdTmpdir):
        os.makedirs(ccdTmpdir)
      
      tmppath = path.join(ccdTmpdir, reponame)

      if not path.islink(lntgt):
         os.symlink(tmppath, lntgt)
      elif path.realpath(lntgt) != tmppath:
         os.unlink(lntgt)
         os.symlink(tmppath, lntgt)
      
      lntgt = path.abspath(lntgt)
      
      repoq = json.load( open (path.join(
          path.dirname(lntgt), '.'+path.basename(lntgt)+'.repo-q.json' )
        , 'r' ) )
      if repoq.get('origin-name') is None:
        repoq['origin-name'] = 'origin'

      # print repoq
      # sys.exit(0)

      os.chdir(path.dirname(lntgt))
      origin = path.abspath(repoq['origin'])

      latest = subprocess.check_output([ 'git'
                                       , '-C', origin
                                       , 'for-each-ref', '--sort=-committerdate'
                                       , 'refs/heads/', '--format=%(refname:short)' ]
                                      ).split('\n')[0]
      
      print "Checking out latest branch:", latest

      os.chdir(ccdTmpdir)

      if origin[-4:]=='.git':
        subprocess.call([ 'git', 'clone', origin, '-b', latest, repoq['basename'] ])
      else:
        subprocess.call([ 'cp', '-r', origin, repoq['basename'] ])
        subprocess.call([ 'git', 'remote', 'add', origin, repoq['origin-name'] ])

        

      os.chdir(lntgt)
      subprocess.call([ 'git-tmp-commit', '-r' ])

      onlineRemotes = repoq['online-remotes']
      if onlineRemotes is not None:
        for r, rurl in onlineRemotes.items():
          subprocess.call([ 'git', 'remote', 'add', r, rurl ])

      try:
        # The user shell, running inside the project dir.
        shell = subprocess.Popen("/bin/bash -c 'cd "+lntgt+"; /bin/bash'", shell=True)
        
        def terminateShell(signal, frame):
           shell.terminate()
           sys.exit(1)
        for s in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP]:
          signal.signal(s, terminateShell)
        
        shell.wait()
        
      finally:
        dirt = subprocess.check_output(['git', 'diff'])
       
        if len(dirt)>1:
          print "Unwise: you have uncommitted work."
          print "Making a temporary commit to prevent data loss..."
          subprocess.call(['git-tmp-commit'])
       
        subprocess.call(['git', 'push', '--all',  repoq['origin-name']])

        sys.exit(0)



