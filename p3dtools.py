__all__ = ["p3dGrid","TurnsGrid","TurnsBlade","turns2moose"]

import struct
import numpy as np

sizeint = 4
sizedbl = 8

class p3dGrid(object):
  '''Parent class for plot3d grids'''
  X      = np.array([])
  iblank = np.array([],dtype=np.int32)

class TurnsGrid(p3dGrid):
  '''Class to read and work with a TURNS formatted grid'''

  def __init__(self, gridfile):
    f = open(gridfile, "rb")

    try:

      # Read the grid dimensions 
      byte = f.read(sizeint)
      assert(struct.unpack('i',byte)[0]==12)
      self.jmax = struct.unpack('i',f.read(sizeint))[0] 
      self.kmax = struct.unpack('i',f.read(sizeint))[0] 
      self.lmax = struct.unpack('i',f.read(sizeint))[0] 
      byte = f.read(sizeint)
      assert(struct.unpack('i',byte)[0]==12)

      # Some byte-math
      self.npoints = self.jmax*self.kmax*self.lmax
      self.xyzsize = self.npoints*3*sizedbl
      self.ibsize  = self.npoints*sizeint

      # Read the grid data
      record  = struct.unpack('i',f.read(sizeint))[0]
      if record==self.xyzsize:
        print "XYZ data only. "
        self.X       = np.zeros((self.jmax,self.kmax,self.lmax,3))
        self.iblank  = np.zeros((self.jmax,self.kmax,self.lmax),dtype=np.int32)
       
        # Loop to read xyz data
        for n in range(3):
          for l in range(self.lmax):
            for k in range(self.kmax):
              for j in range(self.jmax):
                self.X[j,k,l,n] = struct.unpack('d',f.read(sizedbl))[0]

      elif record==self.xyzsize+self.ibsize:
        print "iblank data included"
        self.X = np.zeros((self.jmax,self.kmax,self.lmax,3))
        self.iblank  = np.zeros((self.jmax,self.kmax,self.lmax),dtype=np.int32)
       
        # Loop to read xyz data
        for n in range(3):
          for l in range(self.lmax):
            for k in range(self.kmax):
              for j in range(self.jmax):
                self.X[j,k,l,n] = struct.unpack('d',f.read(sizedbl))[0]

        # Loop to read iblank data
        for l in range(self.lmax):
          for k in range(self.kmax):
            for j in range(self.jmax):
              self.iblank[j,k,l] = struct.unpack('i',f.read(sizeint))[0]

      else:
        print "I don't understand your grid file!"
        exit(1)
        
    finally:
      f.close()


class TurnsBlade(TurnsGrid):
  '''TurnsGrid class with extra features specific to a blade'''

  def __init__(self,gridfile):

    # Read grid
    super(TurnsBlade,self).__init__(gridfile)

    # Compute jtail1, jtail2, jlead
    self.jlead = self.jmax/2
    khalf      = self.kmax/2
    tol = 1e-11
    for j in range(self.jlead):
      j2 = self.jmax-1-j
      if abs(self.X[j,khalf,0,2]-self.X[j2,khalf,0,2])>tol:
        self.jtail1 = j-1
        self.jtail2 = j2+1
        break
    print "jtail1, jtail2 (python/C++ indexes):", self.jtail1, self.jtail2

def p3dGrids(object):
  '''Container class for multiple plot3d grids'''

  def write_moose_file(outfile):
    pass

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
    record = (turnsgrids[ng].jmax*turnsgrids[ng].kmax*turnsgrids[ng].lmax)*(sizedbl*3+sizeint) # 8=sizeof(double), 3=ndim, 4=sizeof(int) for iblank
    f.write(struct.pack('i',record))
    # Loop to write xyz data
    for n in range(3):
      for l in range(turnsgrids[ng].lmax):
        for k in range(turnsgrids[ng].kmax):
          for j in range(turnsgrids[ng].jmax):
            f.write(struct.pack('d',turnsgrids[ng].X[j,k,l,n]))

    # Loop to write iblank data
    for l in range(turnsgrids[ng].lmax):
      for k in range(turnsgrids[ng].kmax):
        for j in range(turnsgrids[ng].jmax):
          f.write(struct.pack('i',turnsgrids[ng].iblank[j,k,l]))
    f.write(struct.pack('i',record))


if __name__=="__main__":
    
    gfs = ['grid.0','grid.1']
    outfile = 'grid.xyz'

    turns2moose(gfs,outfile)
