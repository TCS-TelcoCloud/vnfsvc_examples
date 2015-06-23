============================ 
OpenVNFManager installation
============================

* Installation steps to be followed::

    $ Verify if vnfsvc_examples folder was cloned. Folder should exist in local machine with matching contents.

    $ Refer enterprise or Ims folder to deploy respective service.

    $ Refer the configuration files (under haproxy or Ims)to build the images.

    $ Update the nsd and vnfd templates(exists in vnfsvc_examples) path in /etc/vnfsvc/templates.json 

    $ Update the VNF descriptors(exists in respective usecase folders) with image paths or image uuid (if uploaded in glance) for flavor "Silver" as indicated in the templates.

    $ Update the userdata(exists in vnfsvc_examples) file path if any under deployment_artifact tag for "Silver" flavor in VNF descriptors

    $ Update the image(any desktop image) and flavor details under user_instance tag in heat.yaml

    $ Refer descriptor_inputs file under vnfsvc_examples if any field in VNF Descriptor has to be updated

    $ Upload the heat.yaml to HEAT.Enter the values given below for heat template attributes before uploading it.
         name - <service name> (Ims/webservice)
         flavor - Silver
         private - 192.168.1.0/24 (Any IPv4 CIDR)
         mgmt-if - 192.168.3.0.24 (Any IPv4 CIDR)
         user-nw - 192.168.4.0/24 (Any IPv4 CIDR)
         router - <Router name>

    $ According to the dependencies mentioned in the NSD templated the VNF's will be launched.

    $ After launching the non-dependent VNF/VNF's for a network service, VNFManager is created which takes care of configuring the VNF through managment network if required.

    $ Once the configuration of non-dependent VNF/VNF's are done, an acknowledgement will be sent to VNFSVC service. 
      After receiving the acknowledgement by VNFSVC service, it will resolve the next level of dependencies and then deploy those.
      This will be repeated until all the mentioned VNFS are deployed.

    $ Refer verification file in respective folders and follow the mentioned steps to verify the deployed Network Service.
