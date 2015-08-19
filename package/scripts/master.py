import sys, os, pwd, signal, time
from resource_management import *
from subprocess import call


class Master(Script):
  def install(self, env):
    # Install packages listed in metainfo.xml
    self.install_packages(env)

    import params

    service_packagedir = os.path.realpath(__file__).split('/scripts')[0]     


    self.configure(env)
    
    #Execute('sed -i "s/passwd:.*files/passwd: files  ldap/g" /etc/nsswitch.conf')
    #Execute('sed -i "s/group:.*files/group: files  ldap/g" /etc/nsswitch.conf')

    #Execute('sed -i "s/gid nslcd/gid root/g" /etc/nslcd.conf')
    #Execute('sed -i "s/base dc=example,dc=com/base '+params.dist_name+'/g" /etc/nslcd.conf') 
    #Execute('sed -i "s#uri ldap://127.0.0.1/#uri ldap://'+params.ldap_url+'/#g" /etc/nslcd.conf')


    #Execute('sed -i "s/#base.*group.*ou=Groups,dc=example,dc=com/base   group '+params.groups_name+'/g" /etc/nslcd.conf')
    #Execute('sed -i "s/#base   passwd ou=People,dc=example,dc=com/base   passwd '+params.users_name+'/g" /etc/nslcd.conf')
    #Execute('sed -i "s/#filter passwd (objectClass=aixAccount)/filter passwd (objectClass=posixaccount)/g" /etc/nslcd.conf')

    #Execute('sed -i "s/#map.*passwd uidNumber.*uid/map    passwd uidNumber         uidNumber/g" /etc/nslcd.conf')
    #Execute('sed -i "s/#map.*passwd gidNumber.*gid/map    passwd gidNumber         gidNumber/g" /etc/nslcd.conf')
    #Execute('sed -i "s/#filter group  (objectClass=aixAccessGroup)/filter group  (objectClass=posixgroup)/g" /etc/nslcd.conf')

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
