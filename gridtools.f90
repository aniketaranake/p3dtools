!
! ---------------------------------------------------------------------------
!
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

      subroutine write_turns_grid_(outfile, X, iblank, jmax, kmax, lmax)
      character *40 outfile
      integer jmax,kmax,lmax
      double precision X(jmax,kmax,lmax,3)
      integer iblank(jmax,kmax,lmax)
!f2py intent(in) outfile, X, iblank, jmax,kmax,lmax
      integer j,k,l
      open(unit=1, file=outfile, form='unformatted')
      write(1) jmax,kmax,lmax
      write(1) ((((X(j,k,l,n),j=1,jmax),k=1,kmax),l=1,lmax),n=1,3),
     >       (((iblank(j,k,l),j=1,jmax),k=1,kmax),l=1,lmax)
      close(1)
      end subroutine

      subroutine write_turns_sol_(outfile, Q, mach, alfa, rey, time, 
     >                            jmax, kmax, lmax)
      character *40 outfile
      integer jmax,kmax,lmax
      double precision Q(jmax,kmax,lmax,5), mach, alfa, rey, time
!f2py intent(in) outfile, Q, mach, alfa, rey, time, jmax, kmax, lmax
      integer j,k,l,n
      open(unit=1, file=outfile, form='unformatted')
      write(1) jmax, kmax, lmax
      write(1) mach, alfa, rey, time 
      write(1) ((((Q(j,k,l,n),j=1,jmax),k=1,kmax),l=1,lmax),n=1,5)
      close(1)
      end subroutine

!
! ---------------------------------------------------------------------------
!

      subroutine read_moose_grid_ngrids(infile,ngrids)
      character *40 infile
      integer ngrids
!f2py intent(in) infile
!f2py intent(out) ngrids
      open(unit=1, file=infile, form='unformatted')
      read(1) ngrids
      close(1)
      end subroutine

      subroutine read_moose_grid_dimensions(infile,jmax,kmax,lmax,ngrids)
      character *40 infile
      integer ngrids
      integer jmax(ngrids), kmax(ngrids), lmax(ngrids)
!f2py intent(in) infile, ngrids
!f2py intent(out) jmax,kmax,lmax
      integer n
      open(unit=1, file=infile, form='unformatted')
      read(1) ngrids
      read(1) (jmax(n), kmax(n), lmax(n), n=1,ngrids)
      close(1)
      end subroutine

      subroutine read_moose_grid_data(infile,X,iblank,
     >              include_iblank,jmax,kmax,lmax,ngrids,jmm,kmm,lmm)
      character *40 infile
      integer jmm,kmm,lmm
      integer ngrids
      integer jmax(ngrids), kmax(ngrids), lmax(ngrids)
      double precision X(jmm,kmm,lmm,3,ngrids)
      integer iblank(jmm,kmm,lmm,ngrids)
      logical include_iblank
!f2py intent(in) infile, include_iblank,jmm,kmm,lmm
!f2py intent(out) X, iblank
      integer j,k,l,n,ng

      open(unit=1, file=infile, form='unformatted')
      read(1) ngrids
      read(1) (jmax(n), kmax(n), lmax(n), n=1,ngrids)

      do ng=1,ngrids
      if (include_iblank) then
        read(1) ((((X(j,k,l,n,ng),j=1,jmax(ng)),k=1,kmax(ng)), l=1,lmax(ng)),n=1,3),
     >        (((iblank(j,k,l,ng),j=1,jmax(ng)),k=1,kmax(ng)),l=1,lmax(ng))
      else
        read(1) ((((X(j,k,l,n,ng),j=1,jmax(ng)),k=1,kmax(ng)), l=1,lmax(ng)),n=1,3)
      endif
      enddo
      
      end subroutine

      subroutine read_moose_solution(Q, solfile, jmax, kmax, lmax, nvar,
     >                               jmm,kmm,lmm,ngrids)
      character *40 solfile
      integer nvar, ngrids
      integer jmax(ngrids), kmax(ngrids), lmax(ngrids)
      double precision Q(jmm,kmm,lmm,nvar,ngrids)
!f2py intent(in)  solfile, jmax,kmax,lmax,nvar,jmm,kmm,lmm,ngrids
!f2py intent(out) Q
      integer j,k,l,n,ng

      open(unit=1, file=solfile, form='unformatted')
      read(1) ngrids
      read(1) (jmax(ng),kmax(ng),lmax(ng),nvar,ng=1,ngrids)

      do ng = 1,ngrids
      read(1) ((((Q(j,k,l,n,ng),j=1,jmax(ng)),
     >                          k=1,kmax(ng)),
     >                          l=1,lmax(ng)),
     >                          n=1,3)
      enddo

      close(1)

      end subroutine


      subroutine write_moose_grid_dimensions(outfile,jmax,kmax,lmax,ngrids)
      character *40 outfile
      integer ngrids
      integer jmax(ngrids), kmax(ngrids), lmax(ngrids)
!f2py intent(in) outfile, ngrids, jmax, kmax, lmax
      integer n

      open(unit=1, file=outfile, form='unformatted')
      write(1) ngrids
      write(1) (jmax(n), kmax(n), lmax(n), n=1,ngrids)
      close(1)

      end subroutine

      subroutine write_moose_grid_data(outfile, X, iblank, 
     >               include_iblank, jmax, kmax, lmax)
      character *40 outfile
      double precision X(jmax,kmax,lmax,3)
      integer iblank(jmax,kmax,lmax)
      logical include_iblank
      integer jmax,kmax,lmax
!f2py intent(in) outfile, X, iblank, include_iblank, jmax,kmax,lmax
      integer j,k,l,n

      open(unit=1, file=outfile, form='unformatted',position='append')
      write(1) ((((X(j,k,l,n),j=1,jmax),k=1,kmax),l=1,lmax),n=1,3),
     >       (((iblank(j,k,l),j=1,jmax),k=1,kmax),l=1,lmax)
      close(1)

      end subroutine

