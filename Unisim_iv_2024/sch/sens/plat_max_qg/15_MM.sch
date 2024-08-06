** FPSO - LIRA1/SECTOR1
*GCONP  'P-PLAT1'
	*MAX *STO 28617 CONT REPEAT	       ** 180000 bbd
	*MAX *STL 28617 CONT REPEAT	       ** 180000 bbd
	*MAX *STW 23848 CONT REPEAT	       ** 150000 bbd

*GCONI 'I-PLAT1'
	*MAX *STW 35771 CONT REPEAT	       ** 225000 bpd

*GCONI  'PLAT1'
	PMAINT WATER
	PMSECT 'FIELD'
	PMTARG 61000.

*GCONP  'P-PLAT1'
	*MAX *STG 15000000. CONT REPEAT	 **limitado a capacidade maxima da plataforma
*GCONI 'PLAT1'
	*RECYCLE  GAS  1.0
	*RECYCLE *RECFRC  0.98 0.95 0.90 0.0 0.0     ** Gas Produzido

BHPDEPTH '*' 5400.     ** todos os registradores de pressao na mesma cota.

*APPOR-METHOD *PROD '*' *IP
*APPOR-METHOD *GASI '*' *IP
*APPOR-METHOD *WATI '*' *IP
