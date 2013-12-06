__all__ = ["turnsgrid","turnsblade","turns2moose"]
import struct
import numpy as np
from gridtools import *

class p3dGrids(object):
  '''Container for multiple Grid objects'''

  grids = []
  def __init__(self):
    self.grids = []

  def write_moose_grid(self,outfile):

    # Lists of jmax,kmax,lmax for all grids
    ngrids = len(self.grids)
    jmax = np.zeros([ngrids])
    kmax = np.zeros([ngrids])
    lmax = np.zeros([ngrids])
    for ng in range(ngrids):
      jmax[ng] = self.grids[ng].jmax
      kmax[ng] = self.grids[ng].kmax
      lmax[ng] = self.grids[ng].lmax

    write_moose_grid_dimensions(outfile,jmax,kmax,lmax)

    # Write each set of grid data
    for ng in range(ngrids):
      # TODO: Left off here!!!
      write_moose_grid_data(outfile,self.grids[ng].X,self.grids[ng].iblank,include_iblank)



class p3dGrid(object):

  def __init__(self):
    self.X      = np.empty([])
    self.iblank = np.empty([],dtyp='i4')

class TurnsGrid(p3dGrid):
  '''Class to read and work with a TURNS formatted grid'''

  def __init__(self, gridfile, includes_iblank=True):


    # Read the grid dimensions 
    jmax,kmax,lmax = read_turns_grid_dimensions(gridfile) 
    print "Reading %s: jmax,kmax,lmax = "%gridfile, jmax, kmax, lmax

    # Allocate grid
    self.X      = np.asfortranarray(np.empty([jmax,kmax,lmax,3],dtype='f8'))
    self.iblank = np.asfortranarray(np.zeros([jmax,kmax,lmax],dtype='i4'))

    # Read grid data
    read_turns_grid_data(gridfile, includes_iblank, self.X, self.iblank)
    # read_turns_grid_data(gridfile,self.X)

    self.jmax = jmax
    self.kmax = kmax
    self.lmax = lmax
    print self.X[0,0,0,:]


class TurnsBlade(TurnsGrid):
  '''turnsgrid class with extra features specific to a blade'''

  def __init__(self,gridfile):

    # Read grid
    super(TurnsBlade,self).__init__(gridfile)

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


if __name__=="__main__":
   pass 
