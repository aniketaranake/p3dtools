
      subroutine read_turns_grid_dimensions(filename, jmax, kmax, lmax)
      character *40 filename
      integer jmax,kmax,lmax

!f2py intent(in) filename
!f2py intent(out) jmax,kmax,lmax

      open(unit=1, file=filename, form=unformatted)
      read(1) jmax, kmax, lmax
      rewind(1)
      close(1)

      end subroutine
