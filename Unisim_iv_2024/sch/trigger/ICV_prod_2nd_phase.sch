TRIGGER 'P17_IS_OPEN' ON_WELL 'P17' STO-RP > 5.0 
    TRIGGER 'ICV-P17-Z1' ON_CTRLLUMP 'P17_Z1' GOR > 1600 
        CLUMPSETTING 'P17_Z1' 0.0
    END_TRIGGER
    TRIGGER 'ICV-P17-Z2' ON_CTRLLUMP 'P17_Z2' GOR > 1600
        CLUMPSETTING 'P17_Z2' 0.0
    END_TRIGGER
    TRIGGER 'ICV-P17-Z3' ON_CTRLLUMP 'P17_Z3' GOR > 1600 
        CLUMPSETTING 'P17_Z3' 0.0
    END_TRIGGER
END_TRIGGER

TRIGGER 'P18_IS_OPEN' ON_WELL 'P18' STO-RP > 5.0 
    TRIGGER 'ICV-P18-Z1' ON_CTRLLUMP 'P18_Z1' GOR > 1600 
        CLUMPSETTING 'P18_Z1' 0.0
    END_TRIGGER
    TRIGGER 'ICV-P18-Z2' ON_CTRLLUMP 'P18_Z2' GOR > 1600 
        CLUMPSETTING 'P18_Z2' 0.0
    END_TRIGGER
    TRIGGER 'ICV-P18-Z3' ON_CTRLLUMP 'P18_Z3' GOR > 1600 
        CLUMPSETTING 'P18_Z3' 0.0
    END_TRIGGER
END_TRIGGER