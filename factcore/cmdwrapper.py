import os, sys

def getstatusoutput(cmd):
    """Return (status, output) of executing cmd in a shell."""
    if sys.platform == 'win32':
        pipe = os.popen(cmd + ' 2>&1', 'r')
    else:
        pipe = os.popen('{ ' + cmd + '; } 2>&1', 'r')
    text = pipe.read()
    try:
        sts = pipe.close()
    except:
        sts = -1
    if sts is None: sts = 0
    return sts, text

def runcmd(cmd):
    return getstatusoutput(cmd)
