import sys
class Logger(object):
    def msg(self, prefix, msg):
        sys.stdout.write('[%s] %s' % (prefix, msg))
        sys.stdout.write('\n')
        sys.stdout.flush()

    def i(self, msg): self.msg('[I]', msg)
    def e(self, msg): self.msg('[E]', msg)
    def w(self, msg): self.msg('[W]', msg)
    def d(self, msg): self.msg('[D]', msg)

Log = Logger()