import yaml
import importlib
import simplejson
import os
import logging
from tools import MailNotificator, init_data_file

from datetime import datetime

project_root = os.path.dirname(__file__) + "/../"

with open('{0}/config.yml'.format(project_root)) as f:
    cfg = yaml.load(f)

log_cfg = cfg.get("System").get("logging")
log_mailer_cfg = log_cfg.get('mail_notification')
logger = logging.getLogger("spoofDog.collector")

if log_cfg.get('active'):
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(log_cfg.get('file'))
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    if log_mailer_cfg.get('active'):
        mail_handler = MailNotificator(log_mailer_cfg.get('mail_to'), log_mailer_cfg.get('from'))
        mail_handler.setFormatter(log_format)
        logger.addHandler(mail_handler)
    level = log_cfg.get('level').lower()
    if level == 'critical':
        logger.setLevel(logging.CRITICAL)
    elif level == 'error':
        logger.setLevel(logging.ERROR)
    elif level == 'warning':
        logger.setLevel(logging.WARNING)
    elif level == 'info':
        logger.setLevel(logging.INFO)
    elif level == 'debug':
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.DEBUG)
        logger.warning('Unknown value for option System:logging:level. defaulting to DEBUG')
else:
    logger.addHandler(logging.NullHandler())


def main():
    logger.info('SpoofDog collector initialized.')
    system_conf = cfg.get('System')

    data_dir = system_conf.get('data_dir')

    active_projects = {k: v for (k, v) in cfg.get('Projects').iteritems() if v.get('active')}
    logger.debug('Projects scheduled for scraping: {0}'.format(active_projects.keys()))
    today = datetime.today()
    timestamp = '{0}-{1}-{2}'.format(today.year, today.month, today.day)

    for project, details in active_projects.iteritems():
        project_module = importlib.import_module('estate_modules.{0}'.format(project))
        project_parser = getattr(project_module, details['class_name'])()

        project_parser.get_data()

        data_file_path = '{0}/{1}.json'.format(data_dir, project)

        try:
            if not os.path.isfile(data_file_path):
                init_data_file(data_file_path, project, project_parser.pretty_name)

            with open(data_file_path, 'r+') as f:
                data_json = simplejson.load(f)
                f.seek(0)
                data_json['data'].update({timestamp: project_parser.data})
                simplejson.dump(data_json, f)
                f.truncate()
            logger.info('{0} scraped successfully.'.format(project))
        except IOError:
            logger.critical('Writing data into {0} failed. Aborting all scheduled scrapings.'.format(data_file_path))
            break
        except ValueError as e:
            logger.error(
                'Failed to read JSON datafile {0}, skipping "{1}". Error: {2}'.format(data_file_path, project, e))

    mailers = [ml for ml in logger.handlers if isinstance(ml, MailNotificator)]
    for m in mailers:
        m.notify()


main()
