import sys
from factcore.exceptions import cmdencode

class Logger(object):
    def msg(self, prefix, msg):
        if type(msg) is unicode:
            msg = msg.encode(cmdencode)
        sys.stdout.write('%s %s' % (prefix, msg))
        sys.stdout.write('\n')
        sys.stdout.flush()

    def raw(self, msg):
        sys.stdout.write('%s' % msg)
        sys.stdout.write('\n')
        sys.stdout.flush()

    def i(self, msg): self.msg('[I]', msg)
    def e(self, msg): self.msg('[E]', msg)
    def work(self, msg): self.msg('[W]', msg)
    def d(self, msg): self.msg('[D]', msg)

Log = Logger()
