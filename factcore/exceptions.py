from sys import platform
if platform == 'win32': cmdencode = 'gbk'
else: cmdencode = 'utf8'
cmdencode = 'utf8'

class FactRuntimeError(Exception):
    def __init__(self, message):
        if isinstance(message, unicode):
            self.message = message
        elif isinstance(message, str):
            self.message = message.decode('utf-8')
        # This shouldn't happen...
        else:
            raise TypeError
        super(FactRuntimeError, self).__init__(self.message.encode(cmdencode))

    def __unicode__(self):
        return self.message
