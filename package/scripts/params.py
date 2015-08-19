#!/usr/bin/env python
from resource_management.libraries.functions.version import format_hdp_stack_version, compare_versions
from resource_management import *

# server configurations
config = Script.get_config()


domain=config['configurations']['sssd-config']['domain.name']
bind_dn=config['configurations']['sssd-config']['bind.user']
bind_password=config['configurations']['sssd-config']['bind.password']
hostname=config['configurations']['sssd-config']['ldap.host']

sssd_template_config = config['configurations']['sssdconf-env']['content']

nsswitch_template_config = config['configurations']['nsswitch-env']['content']

