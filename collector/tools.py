from logging import Handler, NOTSET
from email.mime.text import MIMEText
from subprocess import Popen, PIPE
import simplejson


class MailNotificator(Handler):
    """
    Log handler that collects all entries into single buffer. Upon calling notify() method, collected log entries are
    sent via mail and buffer is reset.

    Note: Mails sent from this handler are likely to end up in spam, make sure to set up your inbox to receive them
    correctly
    """

    def __init__(self, mail_to, from_, level=NOTSET):
        self.buffer = ''
        self.mail_to = mail_to
        self.from_ = from_
        super(MailNotificator, self).__init__(level)

    def emit(self, record):
        log_entry = self.format(record)
        self.buffer = '{0}\n{1}'.format(self.buffer, log_entry)

    def notify(self):
        body = MIMEText(self.buffer)
        body['From'] = self.from_
        body['to'] = self.mail_to
        body['Subject'] = "SpoofDog report"

        p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
        p.communicate(body.as_string())
        self.buffer = ''


def init_data_file(file_path, project, pretty_name):
    init_dict = {'project': project, 'pretty_name': pretty_name, 'data': {}}
    with open(file_path, 'w+') as file_:
        simplejson.dump(init_dict, file_)