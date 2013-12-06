
      subroutine read_turns_grid_dimensions(gridfile, jmax, kmax, lmax)
      character *40 gridfile
      integer jmax,kmax,lmax

!f2py intent(in) gridfile
!f2py intent(out) jmax,kmax,lmax

      open(unit=1, file=gridfile, form='unformatted')
      read(1) jmax, kmax, lmax
      rewind(1)
      close(1)

      end subroutine

      subroutine read_turns_grid_data(gridfile,includes_iblank,
     >                                X,iblank,jmax,kmax,lmax)
!      subroutine read_turns_grid_data(gridfile,X,jmax,kmax,lmax)

      character *40 gridfile
      logical includes_iblank
      double precision :: X(jmax,kmax,lmax,3)
      integer :: iblank(jmax,kmax,lmax)
!f2py intent(in) gridfile, jmax, kmax, lmax
!f2py intent(in,out) X, iblank
      integer j,k,l,n
      integer jm,km,lm

      open(unit=1, file=gridfile, form='unformatted')
      read(1) jm,km,lm

      if (includes_iblank) then
        read(1) ((((X(j,k,l,n),j=1,jmax),k=1,kmax),l=1,lmax),n=1,3), 
     >           (((iblank(j,k,l),j=1,jmax),k=1,kmax),l=1,lmax)
      else
        read(1) ((((X(j,k,l,n),j=1,jmax),k=1,kmax),l=1,lmax),n=1,3)
      endif

      close(1)
      
      end subroutine
