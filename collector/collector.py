import yaml
import importlib
import simplejson
import os
from datetime import datetime

project_root = os.path.dirname(__file__) + "/../"

with open('{0}/config.yml'.format(project_root)) as f:
    cfg = yaml.load(f)

data_dir = cfg.get('System').get('data_dir')

active_projects = {k:v for (k, v) in cfg.get('Projects').iteritems() if v.get('active') }

for project, details in active_projects.iteritems():
    project_module = importlib.import_module('estate_modules.{0}'.format(project))
    project_parser = getattr(project_module, details['class_name'])()

    project_parser.get_data()
    try:
        today = datetime.today()
        with open('{0}/{1}_{2}-{3}-{4}'.format(data_dir, project, today.year, today.month, today.day), 'w') as f:
            simplejson.dump(project_parser.data, f)
    except IOError:
        break
