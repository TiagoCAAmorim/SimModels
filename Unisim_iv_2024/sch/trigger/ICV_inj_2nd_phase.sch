TRGVAR 'I18_G_Z1' *ON_CTRLLUMP 'I18_Z1'   BHF-CI
TRGVAR 'I18_G_Z2' *ON_CTRLLUMP 'I18_Z2'   BHF-CI
TRGVAR 'I18_W_Z1' *ON_CTRLLUMP 'I18-W_Z1' BHF-CI
TRGVAR 'I18_W_Z2' *ON_CTRLLUMP 'I18-W_Z2' BHF-CI
TRGVAR 'I18_Z1'   'I18_G_Z1 + I18_W_Z1'
TRGVAR 'I18_Z2'   'I18_G_Z2 + I18_W_Z2'
TRGVAR 'I18'      'I18_Z1 / I18_Z2'

TRIGGER 'I18_IS_OPEN' ON_WELL 'I18' STG-RI > 5.0 OR ON_WELL 'I18-W' STW-RI > 5.0
	TRIGGER 'ICV-I18-A' 'I18' > 'Z1'
		*CLUMPSETTING 'I18_Z1'   0.01
		*CLUMPSETTING 'I18-W_Z1' 0.01
		*CLUMPSETTING 'I18_Z2'   1.0
		*CLUMPSETTING 'I18-W_Z2' 1.0
	END_TRIGGER

	TRIGGER 'ICV-I18-B' 'I18' < 'Z2'
		*CLUMPSETTING 'I18_Z1'   1.0
		*CLUMPSETTING 'I18-W_Z1' 1.0
		*CLUMPSETTING 'I18_Z2'   0.01
		*CLUMPSETTING 'I18-W_Z2' 0.01
	END_TRIGGER
END_TRIGGER


TRGVAR 'I19_G_Z1' *ON_CTRLLUMP 'I19_Z1'   BHF-CI
TRGVAR 'I19_G_Z2' *ON_CTRLLUMP 'I19_Z2'   BHF-CI
TRGVAR 'I19_W_Z1' *ON_CTRLLUMP 'I19-W_Z1' BHF-CI
TRGVAR 'I19_W_Z2' *ON_CTRLLUMP 'I19-W_Z2' BHF-CI
TRGVAR 'I19_Z1'   'I19_G_Z1 + I19_W_Z1'
TRGVAR 'I19_Z2'   'I19_G_Z2 + I19_W_Z2'
TRGVAR 'I19'      'I19_Z1 / I19_Z2'

TRIGGER 'I19_IS_OPEN' ON_WELL 'I19' STG-RI > 5.0 OR ON_WELL 'I19-W' STW-RI > 5.0
	TRIGGER 'ICV-I19-A' 'I19' > 'Z1'
		*CLUMPSETTING 'I19_Z1'   0.01
		*CLUMPSETTING 'I19-W_Z1' 0.01
		*CLUMPSETTING 'I19_Z2'   1.0
		*CLUMPSETTING 'I19-W_Z2' 1.0
	END_TRIGGER

	TRIGGER 'ICV-I19-B' 'I19' < 'Z2'
		*CLUMPSETTING 'I19_Z1'   1.0
		*CLUMPSETTING 'I19-W_Z1' 1.0
		*CLUMPSETTING 'I19_Z2'   0.01
		*CLUMPSETTING 'I19-W_Z2' 0.01
	END_TRIGGER
END_TRIGGER