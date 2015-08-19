import sys, os, pwd, signal, time
from resource_management import *
from subprocess import call
import socket

class Master(Script):
  def install(self, env):
    # Install packages listed in metainfo.xml
    self.install_packages(env)
    import params

    self.configure(env)
    
    Execute('service sssd start')
    Execute('chkconfig sssd on')


  def configure(self, env):
    import params
    #import status_params    
    env.set_params(params)
    
    Execute('echo list of config dump: ' + str(', '.join(params.config['configurations'])))        

    switchcontent=InlineTemplate(params.nsswitch_template_config)
    File(format("/etc/nsswitch.conf"), content=switchcontent, owner='root',group='root', mode=0644)

    sssd_conf='/etc/sssd/sssd.conf'
    content=InlineTemplate(params.sssd_template_config)    
    File(format(sssd_conf), content=content, owner='root',group='root', mode=0600)
    #add new lines at end as Ambari removes trailing newlines and sssd requires this
    Execute('ed -s '+sssd_conf+' <<< w')    
    Execute('ed -s '+sssd_conf+' <<< w')    

    #only if user provided address...
    if (params.address):
      try:
        ip=socket.gethostbyname(params.ldap_hostname)
        Execute('echo Ldap IP detected to be '+ip+' . No need to write hosts entry')
      except socket.gaierror:
        Execute('echo Ldap IP could not be detected, writing hosts entry')        
        Execute('echo '+params.address+' '+params.ldap_hostname+' >> /etc/hosts')
        
  def stop(self, env):
    import params
    #import status_params
    self.configure(env)
    Execute('service sssd stop')
      
  def start(self, env):
    import params
    #import status_params
    self.configure(env)
    Execute('service sssd start')
	

  def status(self, env):
    #import status_params
    #env.set_params(status_params)  
    check_process_status('/var/run/sssd.pid')
    #Execute('service nslcd status')

if __name__ == "__main__":
  Master().execute()
