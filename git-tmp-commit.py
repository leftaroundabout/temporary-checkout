#!/usr/bin/env python2
# -*- coding: utf-8

#   Copyright 2016 Justus Sagemüller

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.


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
   print(tempbranch)

   if tempbranch:
     if '-r' in sys.argv:
       tbn = tempbranch.group(1)
       print('Coming from temporary branch at '+tbn)
       origBranch, tmpDate = re.match('(.*?)/([0-9]*-[0-9]*-[0-9]*.[0-9]*-[0-9]*-[0-9]*)$', tbn).groups()
       subprocess.call([ 'git', 'checkout', '--detach' ])
       if subprocess.call([ 'git', 'rev-parse', '--verify', origBranch ]) > 0:
         subprocess.call([ 'git', 'reset', '--soft', 'HEAD^' ])
         subprocess.call([ 'git', 'checkout', '-b', origBranch ])
       else:
         subprocess.call([ 'git', 'reset', '--soft', origBranch ])
         subprocess.call([ 'git', 'checkout', origBranch ])
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
