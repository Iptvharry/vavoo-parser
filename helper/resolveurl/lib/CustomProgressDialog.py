import six
from resolveurl.lib import log_utils

logger = log_utils.Logger.get_logger(__name__)
DIALOG_XML = 'ProgressDialog.xml' if six.PY2 else 'ProgressDialog2.xml'


class ProgressDialog(object):
    dialog = None

    def get_path(self):
        return '/home/masta/bin/lib/python3/resolveurl/'

    def create(self, heading, line1='', line2='', line3=''):
        return

    def update(self, percent, line1='', line2='', line3=''):
        if self.dialog is not None:
            self.dialog.setProgress(percent)
            if line1:
                self.dialog.setLine1(line1)
            if line2:
                self.dialog.setLine2(line2)
            if line3:
                self.dialog.setLine3(line3)

    def iscanceled(self):
        if self.dialog is not None:
            return self.dialog.cancel
        else:
            return False

    def close(self):
        if self.dialog is not None:
            self.dialog.close()
            del self.dialog

