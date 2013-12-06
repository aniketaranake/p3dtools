all:
	f2py --fcompiler=gfortran --f90flags="-fdefault-real-8" -m gridtools -c gridtools.f90
