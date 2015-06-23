import yaml
import time
from vnfmanager.agent.linux import utils
import paramiko
from vnfmanager.drivers import ellis_netconf as templates
from ncclient import manager

from vnfmanager.openstack.common import log as logging
from vnfmanager.openstack.common.gettextutils import _
LOG = logging.getLogger(__name__)

class ellis:

    def __init__(self, conf):
        LOG.debug(_(conf))
        self.__ncport = "830"
        self.homerip = "0.0.0.0"
        self.hsip = "0.0.0.0"
        self.retries = 10

        self.parse(conf)
        try:
            self.__uname = "user="+self.username
            self.__pswd = "password="+self.password
        except KeyError:
            raise

    def parse(self,cfg):
        for vdu in range(0,len(cfg['Ims'])):
            if(cfg['Ims'][vdu]['name']=="vEllis"):
                self.username=cfg['Ims'][vdu]['vm_details']['image_details']['username']
                self.password=cfg['Ims'][vdu]['vm_details']['image_details']['password']
                self.localip=cfg['Ims'][vdu]['vm_details']['network_interfaces']['pkt-in']['ips']['ims-vellis']
                self.publicip=cfg['Ims'][vdu]['vm_details']['network_interfaces']['pkt-in']['ips']['ims-vellis']
                self.mgmtip=cfg['Ims'][vdu]['vm_details']['network_interfaces']['management-interface']['ips']['ims-vellis']
         
                     
            if(cfg['Ims'][vdu]['name']=="vHomer"):
                self.homerip=cfg['Ims'][vdu]['vm_details']['network_interfaces']['pkt-in']['ips']['ims-vhomer']
            if(cfg['Ims'][vdu]['name']=="vHS"):
                self.hsip=cfg['Ims'][vdu]['vm_details']['network_interfaces']['pkt-in']['ips']['ims-vhs']

    def configure_service(self, *args, **kwargs):
         """configure the service """
         LOG.debug(_("Ellis configure service"))
         LOG.debug(_(self.hsip))
         LOG.debug(_(self.homerip))

         conf_dict = {"private_ip": self.localip ,
                      "public_ip": self.publicip , "chronos_ip": self.localip,"homer_ip": self.homerip, "homestead_ip": self.hsip , "service_name": "ellis"}
         confstr = templates.ellis_settings.format(**conf_dict)

         configuration_done = False
         while not configuration_done:
             try:
                 with manager.connect(host=self.mgmtip, username=self.username, password=self.password, port=830, hostkey_verify=False) as m:
                     print "VM is UP"
                     LOG.debug(_("VM is UP"))
                     configuration_done = True
                     conf_data = m.get_config(source='running').data_xml
                     LOG.debug(_("config %s"), conf_data)
                     c2 = m.edit_config(target='candidate', config=confstr)
                     m.commit(confirmed=False, timeout=300)
             except Exception as e:
                 LOG.debug(_("VM is DOWN %s"), e)
                 LOG.debug(_("VM is DOWN"))
                 print e
                 print "VM is down"
                 time.sleep(5)
