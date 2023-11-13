import json
import six

LOGDEBUG = LOGERROR = LOGWARNING = LOGINFO = None

def execute_jsonrpc(command):
    if not isinstance(command, six.string_types):
        command = json.dumps(command)
    response = xbmc.executeJSONRPC(command)
    return json.loads(response)


def _is_debugging():

    return False


class Logger(object):
    __loggers = {}
    __name = "ResolveURL"
    __addon_debug = False
    __debug_on = _is_debugging()
    __disabled = set()

    @staticmethod
    def get_logger(name=None):
        if name not in Logger.__loggers:
            Logger.__loggers[name] = Logger()

        return Logger.__loggers[name]

    def disable(self):
        if self not in Logger.__disabled:
            Logger.__disabled.add(self)

    def enable(self):
        if self in Logger.__disabled:
            Logger.__disabled.remove(self)

    def log(self, msg, level=LOGDEBUG):
        return

    def log_debug(self, msg):
        self.log(msg, level=LOGDEBUG)

    def log_notice(self, msg):
        self.log(msg, level=LOGINFO)

    def log_warning(self, msg):
        self.log(msg, level=LOGWARNING)

    def log_error(self, msg):
        self.log(msg, level=LOGERROR)
