__all__ = ["turnsgrid","turnsblade","turns2moose"]
import struct
import numpy as np

class turnsgrid(object):
  '''Class to read and work with a TURNS formatted grid'''

  def __init__(self, gridfile):

    try:

      # Read the grid dimensions 
      


class turnsblade(turnsgrid):
  '''turnsgrid class with extra features specific to a blade'''

  def __init__(self,gridfile):

    # Read grid
    super(turnsblade,self).__init__(gridfile)

    # Compute jtail1, jtail2, jlead
    self.jlead = self.jmax/2
    khalf      = self.kmax/2
    tol = 1e-11
    for j in range(self.jlead):
      j2 = self.jmax-1-j
      if abs(self.xyzdata[j,khalf,0,2]-self.xyzdata[j2,khalf,0,2])>tol:
        self.jtail1 = j-1
        self.jtail2 = j2+1
        break
    print "jtail1, jtail2 (python/C++ indexes):", self.jtail1, self.jtail2


def turns2moose(gridfiles, outfile):
  '''Routine to convert files from TURNS format to that required for MOOSE '''

  ngrids = len(gridfiles)

  turnsgrids = []
  for n,grid in enumerate(gridfiles):

    # Read grid and add it to list
    turnsgrids.append(turnsgrid(grid))

  # Write moose file
  f = open(outfile,'wb')

  # ngrids and records
  f.write(struct.pack('i',4))
  f.write(struct.pack('i',ngrids))
  f.write(struct.pack('i',4))

  # Grid dimensions
  record = ngrids*3*4 # 3=ndim, 4=size(int)
  f.write(struct.pack('i',record))
  for ng in range(ngrids):
    f.write(struct.pack('i',turnsgrids[ng].jmax))
    f.write(struct.pack('i',turnsgrids[ng].kmax))
    f.write(struct.pack('i',turnsgrids[ng].lmax))
  f.write(struct.pack('i',record))

  # Grid data
  for ng in range(ngrids):
    record = (turnsgrids[ng].jmax*turnsgrids[ng].kmax*turnsgrids[ng].lmax)*(8*3+4) # 8=sizeof(double), 3=ndim, 4=sizeof(int) for iblank
    f.write(struct.pack('i',record))
    # Loop to write xyz data
    for n in range(3):
      for l in range(turnsgrids[ng].lmax):
        for k in range(turnsgrids[ng].kmax):
          for j in range(turnsgrids[ng].jmax):
            f.write(struct.pack('d',turnsgrids[ng].xyzdata[j,k,l,n]))

    # Loop to write iblank data
    for l in range(turnsgrids[ng].lmax):
      for k in range(turnsgrids[ng].kmax):
        for j in range(turnsgrids[ng].jmax):
          f.write(struct.pack('i',turnsgrids[ng].ibdata[j,k,l]))
    f.write(struct.pack('i',record))


if __name__=="__main__":
    
