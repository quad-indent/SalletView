from tkinter import Tk, Canvas, Frame, Button, Scale, Label, Entry, DoubleVar, StringVar, HORIZONTAL, TclError, font
import threading
from time import sleep
from SalletCfgHandlers import updateCfg, remedyHash, initConfigFile, retrieveConfigVals
from PIL import ImageTk, Image
import win32gui
import win32con

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

def movr(_bg:Canvas, _HiLiteRect:int, _root:Tk, Framer:Frame, width:int, height:int, widther:DoubleVar, heightr:DoubleVar, alphie:DoubleVar,
         FramerColourPicker:Entry, FramerBGColourPicker:Entry, divRatioW:float, divRatioH:float):
    """Incessantly stalks the cursor and updates the higlighter accordingly. Also takes care of popDown"""

    lastWorkingHiLite = ""
    lastWorkingBG = ""
    print("TALLY HO, LADS")
    while True:
        _bg.coords(_HiLiteRect, _root.winfo_pointerx() - widther.get() / 2, _root.winfo_pointery() - heightr.get() / 2,
                  _root.winfo_pointerx() + widther.get() / 2, _root.winfo_pointery() + heightr.get() / 2)
        #x0, y0, x1, y1
        _root.attributes('-alpha', alphie.get())
        if Framer.winfo_rootx() < width: #If is popped up
            if _root.winfo_pointerx() < width * divRatioW or _root.winfo_pointery() < (height - height * (1 - divRatioH)) / 2 or \
                                                                    _root.winfo_pointery() > (height + height * (1 - divRatioH)) / 2:
                # If cursor is outside of the frame
                popDown(Framer, width, widther.get(), heightr.get(), alphie.get(), lastWorkingHiLite, lastWorkingBG)
        if validateHex(FramerColourPicker.get()):
            try:
                _bg.itemconfig(_HiLiteRect, fill=remedyHash(FramerColourPicker.get()))
                lastWorkingHiLite = remedyHash(FramerColourPicker.get())
            except TclError:
                pass
        if validateHex(FramerBGColourPicker.get()):
            biggie = remedyHash(FramerBGColourPicker.get())
            try:
                _bg.configure(bg=biggie)
                _root.config(bg=biggie)
                _root.attributes('-transparentcolor', biggie)
                lastWorkingBG = biggie
            except TclError:
                pass
        sleep(0.01)

def setClickthrough(hwnd):
    """Divine code, borrowed from https://stackoverflow.com/questions/67544105/click-through-tkinter-windows\n
    Mad shoutout to Thingamabobs"""
    try:
        styles = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        styles = win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, styles)
        win32gui.SetLayeredWindowAttributes(hwnd, 0, 255, win32con.LWA_ALPHA)
    except Exception as e:
        print(e)

def popUp(Framer:Frame, width, divRatioW):
    """Shifts the frame into view"""
    Framer.place(x=width * divRatioW)

def popDown(Framer:Frame, width, widther:int, heighter:int, alphie:float, FramerColourPicker:str, FramerBGColourPicker:str):
    """Shifts the frame out of view and updates the .cfg"""
    Framer.place(x=width)
    threading.Thread(target=updateCfg, args=(widther, heighter, alphie, FramerColourPicker, FramerBGColourPicker)).start()
    
def preExit(root:Tk, widther:int, heighter:int, alphie:float, FrameColourPicker:str, FramerBGColourPicker:str):
    """Updates the .cfg and exits the program"""
    updateCfg(widther, heighter, alphie, FrameColourPicker, FramerBGColourPicker)
    root.destroy()
    return
    
def initWindow(dicky:dict):
    """Constructs main window, its background, and the font, and sets their attributes"""

    root = Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry(f"{width}x{height}")
    root.title("SalletView")
    try:
        root.attributes('-transparentcolor', dicky['FramerBGColourPicker'], '-topmost', 1, '-fullscreen', True)
    except TclError:
        dicky['FramerBGColourPicker'] = "#123"
        dicky['FramerColourPicker'] = "#666"
        root.attributes('-transparentcolor', dicky['FramerBGColourPicker'], '-topmost', 1, '-fullscreen', True)
    root.config(bg=dicky['FramerBGColourPicker'])
    root.attributes("-alpha", dicky['alphie'])
    root.wm_attributes("-topmost", 1)
    bg = Canvas(root, width=width, height=height, bg=dicky['FramerBGColourPicker'])
    bg.grid(row=0, column=0)
    setClickthrough(bg.winfo_id())

    defFont = font.Font(family=dicky['fontFamily'], size=dicky['fontSize'], weight=dicky['fontWeight'])

    return root, bg, defFont, width, height

def main():

    initConfigFile()
    dicky = retrieveConfigVals()
    divRatioW = dicky['divRatioW']
    divRatioH = dicky['divRatioH']

    root, bg, defFont, width, height = initWindow(dicky)

    HiLiteRect = bg.create_rectangle(0, 100, 100, 300, fill=dicky['FramerColourPicker'])

    sideBtn = Button(root, text="", bg="red", highlightthickness=0, bd=0, borderwidth=0)
    sideBtn.bind("<Enter>", lambda x: popUp(Framer, width, dicky["divRatioW"]))
    sideBtn.grid(row=0, column=2)
    sideBtn.place(x=width - 5, y=(height - height * (1 - dicky['divRatioH'])) / 2,
                  bordermode='outside', height=height * (1 - dicky['divRatioH']), width=10)

    Framer = Frame(root, width=400, height=400)
    Framer.grid(row=0, column=1)
    Framer.place(x=width, y=(height - height * (1 - dicky['divRatioH'])) / 2,
                 width=width * (1 - dicky["divRatioW"]), height=height * (1 - dicky['divRatioH']))

    widther = DoubleVar()
    widther.set(dicky['widther'])
    Label(Framer, text="Width: ", font=defFont).grid(row=1, column=0)
    FramerWidthSlider = Scale(Framer, from_=10, to=width * 2, resolution=dicky['WHResolution'], orient=HORIZONTAL,
                            variable=widther, font=defFont, length=Framer.winfo_reqwidth() * 2 / 3)
    FramerWidthSlider.grid(row=1, column=1)

    heightr = DoubleVar()
    heightr.set(dicky['heightr'])
    Label(Framer, text="Height: ", font=defFont).grid(row=2, column=0)
    FramerHeightSlider = Scale(Framer, from_=10, to=height * 2, resolution=dicky['WHResolution'], orient=HORIZONTAL,
                            variable=heightr, font=defFont, length=Framer.winfo_reqwidth() * 2 / 3)
    FramerHeightSlider.grid(row=2, column=1)

    alphie = DoubleVar()
    alphie.set(dicky["alphie"])
    Label(Framer, text="Alpha: ", font=defFont).grid(row=3, column=0)
    FramerAlphaSlider = Scale(Framer, from_=0.1, to=.9, resolution=dicky['alphaResolution'], orient=HORIZONTAL,
                            variable=alphie, font=defFont, length=Framer.winfo_reqwidth() * 2 / 3)
    FramerAlphaSlider.grid(row=3, column=1)

    hiLiteColour = StringVar()
    hiLiteColour.set(dicky['FramerColourPicker'])
    Label(Framer, text="Highlight Colour (HEX): ", font=defFont).grid(row=4, column=0)
    FramerColourPicker = Entry(Framer, font=defFont)
    FramerColourPicker.insert(0, dicky['FramerColourPicker'])
    FramerColourPicker.grid(row=4, column=1)

    bgColour = StringVar()
    bgColour.set(dicky['FramerBGColourPicker'])
    Label(Framer, text="Background Colour (HEX): ", font=defFont).grid(row=5, column=0)
    FramerBGColourPicker = Entry(Framer, font=defFont)
    FramerBGColourPicker.insert(0, dicky['FramerBGColourPicker'])
    FramerBGColourPicker.grid(row=5, column=1)

    Button(Framer, text="Exit", command=lambda: preExit(root, widther.get(), heightr.get(), alphie.get(), FramerColourPicker.get(), FramerBGColourPicker.get()),
           font=defFont).grid(row=6, column=1, columnspan=2)

    updateThread = threading.Thread(target=movr, args=(bg, HiLiteRect, root, Framer, width, height, widther, heightr, alphie,
                                                       FramerColourPicker, FramerBGColourPicker, divRatioW, divRatioH), daemon=True)

    updateThread.start()
    root.mainloop()

    return

if __name__ == "__main__":
    main()

