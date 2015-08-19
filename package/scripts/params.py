#!/usr/bin/env python
from resource_management.libraries.functions.version import format_hdp_stack_version, compare_versions
from resource_management import *

# server configurations
config = Script.get_config()


domain=config['configurations']['ambari-sssd-config']['domain.name']
bind_dn=config['configurations']['ambari-sssd-config']['bind.user']
bind_password=config['configurations']['ambari-sssd-config']['bind.password']
ldap_hostname=config['configurations']['ambari-sssd-config']['ldap.host']
ldap_protocol=config['configurations']['ambari-sssd-config']['ldap.protocol']
address=config['configurations']['ambari-sssd-config']['ldap.address']
address=address.strip()

sssd_template_config = config['configurations']['sssdconf-env']['content']

nsswitch_template_config = config['configurations']['nsswitch-env']['content']


