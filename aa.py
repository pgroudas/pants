# To activate:
"""

import sys
sys.path.append(os.getcwd())
import a

emma's coverage yields fweer results



"""

import os
def a(self, targets, tests):
  print self._context.target_roots[0].address.buildfile
  for tgt in targets:
    if self.is_coverage_target(tgt):
      self._context.log.debug('target: %s' % tgt)

def b(self, targets, tests):
  top_level_dir = os.path.dirname(self._context.target_roots[0].address.buildfile.relpath)
  print 'top_level_dir = %s' % top_level_dir

  i = 0
  for tgt in targets:
    if self.is_coverage_target(tgt):
      # self._context.log.debug('target: %s' % tgt)
      if tgt.address.buildfile.relpath.startswith(top_level_dir):
        print i, tgt.address.buildfile.relpath, tgt
    i += 1

      

def c(self, targets, tests):
  rec = self.get_coverage_patterns(targets, recursive=True)
  nrec =  self.get_coverage_patterns(targets, recursive=False)
  print len(rec)
  print len(nrec)
  file('/tmp/bg', 'w').write(rec)
