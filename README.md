#### An Ambari Service for SSSD
Ambari service for easily installing and managing SSSD on HDP cluster

This can be used in conjunction with [other security related Ambari services](https://github.com/abajwa-hw/ambari-workshops#security-related-sample-services) to setup security on a cluster
  - [Steps](https://github.com/abajwa-hw/security-workshops/blob/master/Setup-kerberos-Ambari-services.md) on how to use Ambari services to automate the install of OpenLDAP, KDC, NSLCD/SSSD on existing cluster, and then running Ambari kerberos wizard
  - [Steps](https://github.com/abajwa-hw/ambari-workshops/blob/master/blueprints-demo-security.md) on how to use blueprints to deploy a cluster with OpenLDAP, KDC, SSSD/SSSD, and then run Ambari kerberos wizard


Author: [Ali Bajwa](https://www.linkedin.com/in/aliabajwa)

#### Setup

- Download HDP 2.2 sandbox VM image (Sandbox_HDP_2.2_VMware.ova) from [Hortonworks website](http://hortonworks.com/products/hortonworks-sandbox/)
- Import Sandbox_HDP_2.2_VMware.ova into VMWare and set the VM memory size to 8GB
- Now start the VM
- After it boots up, find the IP address of the VM and add an entry into your machines hosts file e.g.
```
192.168.191.241 sandbox.hortonworks.com sandbox    
```
- Connect to the VM via SSH (password hadoop) and start Ambari server
```
ssh root@sandbox.hortonworks.com
/root/start_ambari.sh
```

- To deploy the SSSD service, run below
```
cd /var/lib/ambari-server/resources/stacks/HDP/2.2/services
git clone https://github.com/abajwa-hw/sssd-service.git   
sudo service ambari restart
```
- Then you can click on 'Add Service' from the 'Actions' dropdown menu in the bottom left of the Ambari dashboard:

On bottom left -> Actions -> Add service -> check SSSD server -> Next -> Next -> Enter password -> Next -> Deploy
![Image](../master/screenshots/screenshot-vnc-config.png?raw=true)

- On successful deployment you will see the SSSD service as part of Ambari stack and will be able to start/stop the service from here:
![Image](../master/screenshots/screenshot-vnc-stack.png?raw=true)

- When you've completed the install process, SSSD server will appear in Ambari 
![Image](../master/screenshots/screenshot-freeipa-stack.png?raw=true)

- You can see the parameters you configured under 'Configs' tab
![Image](../master/screenshots/screenshot-freeipa-stack-config.png?raw=true)

- To remove the SSSD service: 
  - Stop the service via Ambari
  - Delete the service
  
    ```
    curl -u admin:admin -i -H 'X-Requested-By: ambari' -X DELETE http://sandbox.hortonworks.com:8080/api/v1/clusters/Sandbox/services/SSSD
    ```
  - Remove SSSD rpm and config files 
  
    ```
	rpm -e nss-pam-ldapd-0.8.12-rhel6.13.1.x86_64
	rm -f /etc/nslcd.conf
	rm -f /etc/nsswitch.conf    
    ```

- One benefit to wrapping the component in Ambari service is that you can now monitor/manage this service remotely via REST API
```
export SERVICE=SSSD
export PASSWORD=admin
export AMBARI_HOST=sandbox.hortonworks.com
export CLUSTER=Sandbox

#get service status
curl -u admin:$PASSWORD -i -H 'X-Requested-By: ambari' -X GET http://$AMBARI_HOST:8080/api/v1/clusters/$CLUSTER/services/$SERVICE

#start service
curl -u admin:$PASSWORD -i -H 'X-Requested-By: ambari' -X PUT -d '{"RequestInfo": {"context" :"Start $SERVICE via REST"}, "Body": {"ServiceInfo": {"state": "STARTED"}}}' http://$AMBARI_HOST:8080/api/v1/clusters/$CLUSTER/services/$SERVICE

#stop service
curl -u admin:$PASSWORD -i -H 'X-Requested-By: ambari' -X PUT -d '{"RequestInfo": {"context" :"Stop $SERVICE via REST"}, "Body": {"ServiceInfo": {"state": "INSTALLED"}}}' http://$AMBARI_HOST:8080/api/v1/clusters/$CLUSTER/services/$SERVICE
```

#### Browse LDAP users from Hadoop cluster

- Your operating system can now recognize your LDAP users (e.g. in OpenLDAP) 
```
# groups ali
ali : sales marketing hr legal finance
# id ali
uid=75000010(ali) gid=75000005(sales) groups=75000005(sales),75000001(marketing),75000002(hr),75000003(legal),75000004(finance)
``` 


