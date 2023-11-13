import sys, os, pwd, base64, re

UFILE = base64.b64decode("W1VuaXRdClNvdXJjZVBhdGg9CkRlc2NyaXB0aW9uPU1hc3RhYWFTIE1YVi1QYXJzZXIgU2VydmljZQpXYW50cz1uZXR3b3JrLW9ubGluZS50YXJnZXQKQWZ0ZXI9bXVsdGktdXNlci50YXJnZXQKU3RhcnRMaW1pdEludGVydmFsU2VjPTAKIApbU2VydmljZV0KVXNlcj0KUmVzdGFydD1hbHdheXMKUmVzdGFydFNlYz01CkV4ZWNTdGFydD0KRXhlY1JlbG9hZD0KRXhlY1N0b3A9CiAKW0luc3RhbGxdCldhbnRlZEJ5PW11bHRpLXVzZXIudGFyZ2V0CgoK")
SFILE = base64.b64decode("IyEvYmluL2Jhc2gKClJPT1RQQVRIPQpTRVJWSUNFPSRST09UUEFUSC9teHYtc2VydmljZS5weQoKc3RhcnQoKSB7CiAgICBwaWRzPSQocHMgYXV4IHwgZ3JlcCAnbXh2LXNlcnZpY2UucHknIHwgZ3JlcCAtdiBncmVwIHwgYXdrICd7cHJpbnQgJDJ9JykKICAgIGlmICEgWyAiJHBpZHMiID09ICIiIF07IHRoZW4KICAgICAgICBlY2hvICdteHYtc2VydmljZSBpcyBhbHJlYWR5IHJ1bm5pbmcnCiAgICAgICAgcmV0dXJuIDEKICAgIGZpCiAgICBlY2hvICdTdGFydGluZyBNWFYtUGFyc2VyIFNlcnZpY2UgLi4uJwogICAgcHl0aG9uICRTRVJWSUNFICYKICAgIGVjaG8gJ1J1bm5pbmcgaW4gZm9yZWdyb3VuZC4uLicKICAgIHNsZWVwIGluZmluaXR5Cn0KCnN0b3AoKSB7CiAgICBwaWRzPSQocHMgYXV4IHwgZ3JlcCAibXh2LXNlcnZpY2UucHkiIHwgZ3JlcCAtdiBncmVwIHwgYXdrICd7cHJpbnQgJDJ9JykKICAgIGlmIFsgIiRwaWRzIiA9PSAiIiBdOyB0aGVuCiAgICAgICAgZWNobyAibXh2LXNlcnZpY2UgaXMgbm90IHJ1bm5pbmciCiAgICAgICAgcmV0dXJuIDEKICAgIGZpCiAgICBlY2hvICJTdG9wcGluZyBNWFYtUGFyc2VyIFNlcnZpY2UgLi4uIgogICAga2lsbCAtOSAkcGlkcyAyPi9kZXYvbnVsbAogICAgc2xlZXAgMQp9CgpyZXN0YXJ0KCkgewogICAgc3RvcAogICAgc2xlZXAgMQogICAgc3RhcnQKfQoKY2FzZSAiJDEiIGluCiAgICBzdGFydCkgc3RhcnQgOzsKICAgIHN0b3ApIHN0b3AgOzsKICAgIHJlbG9hZCkgcmVzdGFydCA7OwogICAgcmVzdGFydCkgcmVzdGFydCA7OwogICAgKikgZWNobyAiVXNhZ2U6ICQwIHtzdGFydHxzdG9wfHJlc3RhcnR8cmVsb2FkfSIgOzsKZXNhYwoKZXhpdCAwCgo=")
MFILE = base64.b64decode("aW1wb3J0IHV0aWxzLmNvbW1vbiBhcyBjb20KY29tLmNoZWNrKCkKCmltcG9ydCBjbGksIHNlcnZpY2VzCgoKZGVmIG1haW4oKToKICAgIHNlcnZpY2VzLmhhbmRsZXIoJ2luaXQnKQogICAgI2NsaS5tZW51KCkKCgppZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgogICAgbWFpbigpCg==")
CUID = os.getuid()
CU = pwd.getpwuid(CUID)[0]
RP = os.path.dirname(os.path.abspath(__file__))
PUID = os.stat(RP).st_uid
PU = pwd.getpwuid(PUID)[0]


class col:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    YELLOW = '\033[33m'
    ENDC = '\033[0m'
    DEFAULT = '\033[0m'
    BOLD = '\033[1m'


def printc(rText, rColour=col.OKBLUE, rPadding=0):
    print("%s ┌─────────────────────────────────────────────────┐ %s" % (rColour, col.ENDC))
    for i in range(rPadding): print("%s │                                                 │ %s" % (rColour, col.ENDC))
    if isinstance(rText, str):
        print("%s │ %s%s%s │ %s" % (rColour, " "*round(23-(len(rText)/2)), rText, " "*round(46-(22-(len(rText)/2))-len(rText)), col.ENDC))
    elif isinstance(rText, list):
        for text in rText:
            print("%s │ %s%s%s │ %s" % (rColour, " "*round(23-(len(text)/2)), text, " "*round(46-(22-(len(text)/2))-len(text)), col.ENDC))
    for i in range(rPadding): print("%s │                                                 │ %s" % (rColour, col.ENDC))
    print("%s └─────────────────────────────────────────────────┘ %s" % (rColour, col.ENDC))
    print(" ")


def pre_check():
    if not CUID == 0:
        return [ "You need to be run this Script @ root!", "Please try again with sudo!" ]
    if os.path.exists(os.path.join(RP, 'service')): os.remove(os.path.join(RP, 'service'))
    if os.path.exists(os.path.join(RP, 'mxv-service.py')): os.remove(os.path.join(RP, 'mxv-service.py'))
    if os.path.exists("/etc/systemd/system/mxv-parser.service"): os.remove("/etc/systemd/system/mxv-parser.service")
    return True


def main():
    printc("Welcome to my service installer ...", col.HEADER)
    pre = pre_check()
    if not pre == True:
        return printc(pre, col.FAIL)
    if not CU == PU:
        printc(["Current user of this Directory is: %s" % PU, "Would you like to install service as it?" ], col.WARNING)
        i = input("(Y/n): ")
        if i == "" or i.upper() in [ "YES", "Y" ]: USER = PU
        else: USER = CU
    else: USER = CU
    printc("Install Services as User: %s" % USER, col.DEFAULT)

    printc(["Creating File:", str(os.path.join(RP, 'service')) ], col.DEFAULT)
    rFile = open(os.path.join(RP, 'service'), "wb")
    rFile.write(SFILE)
    rFile.close()
    if not os.path.exists(os.path.join(RP, 'service')): 
        return printc(["Failed!","Please try again ..."], col.FAIL)
    os.system("sed -i -e 's|ROOTPATH=|ROOTPATH=%s|g' %s" %(RP, str(os.path.join(RP, 'service'))))
    os.system("chmod +x %s" % os.path.join(RP, 'service'))
    if not USER == 'root':
        os.system('chown %s:%s %s' %(USER, USER, str(os.path.join(RP, 'service'))))

    printc(["Creating File:", str(os.path.join(RP, 'mxv-service.py')) ], col.DEFAULT)
    rFile = open(os.path.join(RP, 'mxv-service.py'), "wb")
    rFile.write(MFILE)
    rFile.close()
    if not os.path.exists(os.path.join(RP, 'mxv-service.py')): 
        return printc(["Failed!","Please try again ..."], col.FAIL)
    os.system("chmod +x %s" % os.path.join(RP, 'mxv-service.py'))
    if not USER == 'root':
        os.system('chown %s:%s %s' %(USER, USER, str(os.path.join(RP, 'mxv-service.py'))))

    printc(["Creating File:", "/etc/systemd/system/mxv-parser.service" ], col.DEFAULT)
    rFile = open("/etc/systemd/system/mxv-parser.service", "wb")
    rFile.write(UFILE)
    rFile.close()
    if not os.path.exists("/etc/systemd/system/mxv-parser.service"): 
        return printc(["Failed!","Please try again ..."], col.FAIL)
    os.system("sed -i -e 's|SourcePath=|SourcePath=%s|g' %s" %(str(os.path.join(RP, 'service')), "/etc/systemd/system/mxv-parser.service"))
    os.system("sed -i -e 's|User=|User=%s|g' %s" %(USER, "/etc/systemd/system/mxv-parser.service"))
    os.system("sed -i -e 's|ExecStart=|ExecStart=/bin/bash %s start|g' %s" %(str(os.path.join(RP, 'service')), "/etc/systemd/system/mxv-parser.service"))
    os.system("sed -i -e 's|ExecReload=|ExecReload=/bin/bash %s reload|g' %s" %(str(os.path.join(RP, 'service')), "/etc/systemd/system/mxv-parser.service"))
    os.system("sed -i -e 's|ExecStop=|ExecStop=/bin/bash %s stop|g' %s" %(str(os.path.join(RP, 'service')), "/etc/systemd/system/mxv-parser.service"))
    os.system("sudo chmod +x /etc/systemd/system/mxv-parser.service")
    printc("Everything looks Good !", col.OKGREEN)
    printc("Would you like to enable Service now?", col.DEFAULT)
    i = input("(Y/n): ")
    if i == "" or i.upper() in [ "YES", "Y" ]:
        os.system("sudo systemctl daemon-reload")
        os.system("sudo systemctl enable mxv-parser.service")
        os.system("sudo systemctl start mxv-parser.service")
    else:
        printc(["OK!","To enable Service run:", "sudo systemctl daemon-reload", "sudo systemctl enable mxv-parser.service", "sudo systemctl start mxv-parser.service"], col.DEFAULT)
    printc(["Everything is Done !", "Have fun with it ...", "Copyright by Mastaaa @2023"], col.OKBLUE)
    return


if __name__ == "__main__":
    main()
