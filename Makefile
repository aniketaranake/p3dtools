all:
	#f2py --debug-capi --fcompiler=gfortran --f90flags="-fdefault-real-8" -m gridtools -c gridtools.f90
	#f2py --debug-capi --fcompiler=ifort --f90flags="-r8 -132" -m gridtools -c gridtools.f90
	f2py --fcompiler=ifort --f90flags="-r8 -132" -m gridtools -c gridtools.f90
