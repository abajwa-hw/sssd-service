#!/usr/bin/env python
from resource_management import *

config = Script.get_config()
sssd_template_config = config['configurations']['sssdconf-env']['content']

