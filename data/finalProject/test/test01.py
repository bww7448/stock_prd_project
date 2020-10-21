    elif closeP >= 0.9*openP:


        if openP < highP :
            if closeP > lowP :
                return "M05"
            if highP -3*openP +2*closeP < 0:
                return "M03"
            return "M04"
        if closeP > lowP :
            if 3*closeP - lowP - 2*openP < 0:
                return "M01"
            return "M02"
        return "M00"