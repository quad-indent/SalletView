"""Functionalities for handling the .cfg file and its contents"""

def remedyHash(stringie):
    """Prepends a hash to a string if it doesn't have one already"""
    if stringie[0] != '#':
        return f"#{stringie}"
    return stringie

def validateHex(stringie):
    """Why use regex when you can do several checks in a row?"""
    if not (len(stringie) == 3 or len(stringie) == 4 or len(stringie) == 6 or len(stringie) == 7):
        return False
    if stringie[0] != '#':
        if not (len(stringie) == 3 or len(stringie) == 6):
            return False
        for i in stringie:
            if not ((ord(i) >= 48 and ord(i) <= 57) or (ord(i) >= 65 and ord(i) <= 70) or (ord(i) >= 97 and ord(i) <= 102)):
                return False
        return True
    for i in stringie[1:]:
        if not ((ord(i) >= 48 and ord(i) <= 57) or (ord(i) >= 65 and ord(i) <= 70) or (ord(i) >= 97 and ord(i) <= 102)):
            return False
    return True

def updateCfg(widther:int, heighter:int, alphie:float, FrameColourPicker:str, FramerBGColourPicker:str):
    """Only cares about the last 5 lines of the .cfg file"""
    try:
        lines = []
        with open("SalletConfig.cfg", "r", encoding="utf-8") as f:
            lines = f.readlines()
        lines[14] = f"widther = {widther}\n"
        lines[15] = f"heightr = {heighter}\n"
        lines[16] = f"alphie = {alphie}\n"
        if validateHex(FrameColourPicker):
            lines[17] = f"FramerColourPicker = {remedyHash(FrameColourPicker)}\n"
        if validateHex(FramerBGColourPicker):
            lines[18] = f"FramerBGColourPicker = {remedyHash(FramerBGColourPicker)}\n"
        with open("SalletConfig.cfg", "w", encoding="utf-8") as f:
            f.writelines(lines)
        return
    except Exception as e:
        print(e)
        return

def initConfigFile():
    """Creates the .cfg file if it doesn't exist and fills it with default values"""
    try:
        with open("SalletConfig.cfg", "r", encoding="utf-8") as f:
            return
    except Exception:
        with open("SalletConfig.cfg", "w", encoding="utf-8") as f:
            f.write("| The options before the ___ line are ones you cannot change in the program. "\
                    "The ones after are ones you can change in the program and are stored here for safekeeping\n")
            f.write("| If you change these parameters, the program may crash or otherwise malfunction!\n")
            f.write("| Ratio of width and height of the main window to the width of the popup\n")
            f.write("divRatioW = 4/6\n")
            f.write("divRatioH = 4/6\n")
            f.write("| The font to be used\n")
            f.write("fontFamily = Arial\n")
            f.write("fontSize = 14\n")
            f.write("fontWeight = bold\n")
            f.write("| Resolution for the following means the minimum amount by which the sliders will change. WH should be int, alpha - float\n")
            f.write("WHResolution = 10\n")
            f.write("alphaResolution = 0.05\n")
            f.write("| _______________________________________________\n")
            f.write("| The following options can be changed in the program\n")
            f.write("widther = 3840\n")
            f.write("heightr = 100\n")
            f.write("alphie = 0.35\n")
            f.write("FramerColourPicker = #666\n")
            f.write("FramerBGColourPicker = #123\n")
    return

def ratiotofloat(stringie):
    """Because I originally decided to write ratios for it as divRatioW = 4/6, and honestly it looks neat so I made this function"""
    temp1, temp2 = stringie.split("/")
    return int(temp1) / int(temp2)

def retrieveConfigVals():
    """Retrieves the values from the .cfg file if it's accessible and returns them as a dict, otherwise prepares a default dict"""
    try:
        with open("SalletConfig.cfg", "r", encoding="utf-8") as f:
            lines = f.readlines()
            divRatioW = float(ratiotofloat(lines[3].split("=")[1].strip()))
            divRatioH = float(ratiotofloat(lines[4].split("=")[1].strip()))
            fontFamily = lines[6].split("=")[1].strip()
            fontSize = int(lines[7].split("=")[1].strip())
            fontWeight = lines[8].split("=")[1].strip()
            WHResolution = int(lines[10].split("=")[1].strip())
            alphaResolution = float(lines[11].split("=")[1].strip())
            widther = int(float(lines[14].split("=")[1].strip()))
            heightr = int(float(lines[15].split("=")[1].strip()))
            alphie = float(lines[16].split("=")[1].strip())
            FramerColourPicker = lines[17].split("=")[1].strip()
            FramerBGColourPicker = lines[18].split("=")[1].strip()
            dicky = {
                "divRatioW": divRatioW,
                "divRatioH": divRatioH,
                "fontFamily": fontFamily,
                "fontSize": fontSize,
                "fontWeight": fontWeight,
                "WHResolution": WHResolution,
                "alphaResolution": alphaResolution,
                "widther": widther,
                "heightr": heightr,
                "alphie": alphie,
                "FramerColourPicker": FramerColourPicker,
                "FramerBGColourPicker": FramerBGColourPicker
            }
            return dicky
    except Exception as e:
        print(e)
        dicky = {
            "divRatioW": 4/6,
            "divRatioH": 4/6,
            "fontFamily": "Arial",
            "fontSize": 14,
            "fontWeight": "bold",
            "WHResolution": 10,
            "alphaResolution": 0.05,
            "widther": 3840,
            "heightr": 100,
            "alphie": 0.35,
            "FramerColourPicker": "#666",
            "FramerBGColourPicker": "#123"
        }
        return dicky
