** FPSO - LIRA1/SECTOR1
*GCONP  'P-PLAT1'
	MAX STO 28617 CONT REPEAT	       ** 180000 bbd
	MAX STL 28617 CONT REPEAT	       ** 180000 bbd
	MAX STW 23848 CONT REPEAT	       ** 150000 bbd

*GCONI 'I-PLAT1'
	MAX STW 35771 CONT REPEAT	       ** 225000 bpd

*GCONI  'PLAT1'
	PMAINT WATER
	PMSECT 'CAMPO'
	PMTARG 450.

*GCONP  'P-PLAT1'
	MAX STG 12000000. CONT REPEAT	 **limitado a capacidade maxima da plataforma
*GCONI 'PLAT1'
	RECYCLE GAS 0.95

BHPDEPTH '*' 5400.     ** todos os registradores de pressao na mesma cota.

APPOR-METHOD PROD '*' IP
APPOR-METHOD GASI '*' IP
APPOR-METHOD WATI '*' IP

** GPRODGROUP 'GRP-1' *FROM 'RP-1'
