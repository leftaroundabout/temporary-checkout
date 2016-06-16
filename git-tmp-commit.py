#!/usr/bin/env python2

import subprocess
import sys
import datetime
import re

if __name__ == "__main__":
   t = datetime.datetime.now()
   branchn = subprocess.check_output([ 'git'
                                     , 'rev-parse'
                                     , '--abbrev-ref'
                                     , 'HEAD']
                       ).split('\n') [0]
   tempbranch = re.match('temporary-commits/(.*)', branchn)

   if tempbranch:
    if '-r' in sys.argv:
     tbn = tempbranch.group(1)
     print('Coming from temporary branch at '+tbn)
     origBranch, tmpDate = re.match('(.*?)/([0-9]*-[0-9]*-[0-9]*.[0-9]*-[0-9]*-[0-9]*)$', tbn).groups()
     subprocess.call([ 'git', 'checkout', '--detach' ])
     subprocess.call([ 'git', 'reset', '--soft', 'HEAD^' ])
     subprocess.call([ 'git', 'checkout', '-b', origBranch ])
     subprocess.call([ 'git', 'reset' ])

   else:
    if '-r' not in sys.argv:
     subprocess.call([ 'git'
                     , 'checkout'
                     , '-b'
                     , 'temporary-commits/'+branchn+'/'+t.strftime('%Y-%m-%d_%H-%M-%S')
                     ])
     subprocess.call([ 'git'
                     , 'commit'
                     , '-am'
                     , 'Temporary commit' if len(sys.argv) == 1
                        else sys.argv[1]
                     ])
