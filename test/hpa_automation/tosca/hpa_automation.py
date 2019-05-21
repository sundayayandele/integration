#!/usr/bin/python

#Prerequisites for machine to run this
#Put in required parameters in hpa_automation_config.json
#Install python-pip (apt install python-pip)
#Install python mysql.connector (pip install mysql-connector-python)
#Install ONAP CLI
#Must have connectivity to the ONAP, a k8s vm already running is recommended
#Create Preload File, the script will modify the parameters required from serivce model, service instance
#and vnf instance
#Create policies for homing
#Put in CSAR file
#modify so-bpmn configmap and change version to v2

import json
import os
import time
import argparse
import sys
import requests

def get_parameters(file):
    parameters = json.load(file)
    return parameters

def get_out_helper(in_string):
    out_list = (((in_string.replace('-','')).replace('|', '')).replace('+', '')).split()
    return out_list

def get_out_helper_2(in_string):
    out_list = ((in_string.replace('|', '')).replace('+', '')).split()
    return out_list

def set_open_cli_env(parameters):
    os.environ["OPEN_CLI_PRODUCT_IN_USE"] = parameters["open_cli_product"]
    os.environ["OPEN_CLI_HOME"] = parameters["open_cli_home"]

def create_complex(parameters):
    complex_create_string = "oclip complex-create -j {} -r {} -x {} -y {} -lt {} -l {} -i {} -lo {} \
                         -S {} -la {} -g {} -w {} -z {} -k {} -o {} -q {} -m {} -u {} -p {}".format(parameters["street2"], \
                          parameters["physical_location"], parameters["complex_name"], \
                          parameters["data_center_code"], parameters["latitude"], parameters["region"], \
                          parameters["street1"], parameters["longitude"], parameters["state"], \
                          parameters["lata"], parameters["city"], parameters["postal-code"], \
                          parameters["complex_name"], parameters["country"], parameters["elevation"], \
                          parameters["identity_url"], parameters["aai_url"], parameters["aai_username"], \
                          parameters["aai_password"])

    os.system(complex_create_string)


def register_cloud_helper(cloud_region, values, parameters):
    #Create Cloud
    cloud_create_string = 'oclip cloud-create -e {} -b {} -I {{\\\\\\"openstack-region-id\\\\\\":\\\\\\"{}\\\\\\"}} \
    -x {} -y {} -j {} -w {} -l {} -url {} -n {} -q {} -r {} -Q {} -i {} -g {} -z {} -k {} -c {} -m {} -u {} -p {}'.format(
      values.get("esr-system-info-id"), values.get("user-name"), cloud_region, parameters["cloud-owner"], \
      cloud_region, values.get("password"), values.get("cloud-region-version"), values.get("default-tenant"), \
      values.get("service-url"), parameters["complex_name"], values.get("cloud-type"), parameters["owner-defined-type"], \
      values.get("system-type"), values.get("identity-url"), parameters["cloud-zone"], values.get("ssl-insecure"), \
      values.get("system-status"), values.get("cloud-domain"), parameters["aai_url"], parameters["aai_username"], \
      parameters["aai_password"])


    os.system(cloud_create_string)

    #Associate Cloud with complex
    complex_associate_string = "oclip complex-associate -x {} -y {} -z {} -m {} -u {} -p {}".format(parameters["complex_name"], \
      cloud_region, parameters["cloud-owner"], parameters["aai_url"], parameters["aai_username"], parameters["aai_password"])
    os.system(complex_associate_string)

    #Register Cloud with Multicloud
    multicloud_register_string = "oclip multicloud-register-cloud -y {} -x {} -m {}".format(parameters["cloud-owner"], \
      cloud_region, parameters["multicloud_url"])
    os.system(multicloud_register_string)

def register_all_clouds(parameters):
    cloud_dictionary = parameters["cloud_region_data"]
    for cloud_region, cloud_region_values in cloud_dictionary.iteritems():
        register_cloud_helper(cloud_region, cloud_region_values, parameters)

def register_vnfm_helper(vnfm_key, values, parameters):
    #Create vnfm
    vnfm_create_string = 'oclip vnfm-create -b {} -c {} -e {} -v {} -g {} -x {} -i {} -j {} -q {} \
    -m {} -u {} -p {}'.format(vnfm_key, values.get("type"), values.get("vendor"), \
      values.get("version"), values.get("url"), values.get("vim-id"), \
      values.get("user-name"), values.get("user-password"), values.get("vnfm-version"), \
      parameters["aai_url"], parameters["aai_username"], parameters["aai_password"])

    os.system(vnfm_create_string)

def register_vnfm(parameters):
    vnfm_params = parameters["vnfm_params"]
    for vnfm_key, vnfm_values in vnfm_params.iteritems():
        register_vnfm_helper(vnfm_key, vnfm_values, parameters)


#VNF Deployment Section
def add_policies(parameters):
    resource_string = (os.popen("oclip get-resource-module-name  -u {} -p {} -m {} |grep {}".format(\
      parameters["sdc_creator"], parameters["sdc_password"], parameters["sdc_catalog_url"], \
      parameters["service-model-name"] ))).read()
    resource_module_name =   (get_out_helper_2(resource_string))[1]

   #Put in the right resource module name in all policies located in parameters["policy_directory"]
    os.system("find {}/ -type f -exec sed -i 's/{}/{}/g' {{}} \;".format(
      parameters["policy_directory"], parameters["temp_resource_module_name"], resource_module_name))

   #Upload policy models
    for model in os.listdir(parameters["policy_models_directory"]):
      os.system("oclip policy-type-create -x {} -u {} -p {} -m {}".format(model, parameters["policy_username"], \
        parameters["policy_password"], parameters["policy_url"]))
      time.sleep(0.5)

    #print("Put in the resourceModuleName {} in your policy files in {}. ".format(resource_module_name, \
    #(parameters["policy_directory"])))
    #raw_input("Press Enter to continue...")


    #Loop through policy, put in resource_model_name and create policies
    for policy in os.listdir(parameters["policy_directory"]):
      policy_name = "{}.{}".format(parameters["policy_scope"], os.path.splitext(policy)[0])
      policy_file = (os.path.join(parameters["policy_directory"], policy))
      #Create policy
      os.system("oclip policy-create-outdated -m {} -u {} -p {} -x {} -S {} -T {} -o {} -b $(cat {})".format(parameters["policy_url"],\
      parameters["policy_username"], parameters["policy_password"], policy_name, parameters["policy_scope"], \
      parameters["policy_config_type"], parameters["policy_onapName"], policy_file))

      #Push policy
      os.system("oclip policy-push-outdated -m {} -u {} -p {} -x {} -b {} -c {}".format(parameters["policy_url"], \
        parameters["policy_username"], parameters["policy_password"], policy_name, parameters["policy_config_type"],\
        parameters["policy_pdp_group"]))

def onboard_vnf(parameters):
    vnfs = parameters["vnfs"]
    vnf_onboard_outputs = {}

    for key, value in vnfs.items():
        vnf_onboard_string = 'oclip vfc-catalog-onboard-vnf -c {}'.format(value.get("csar-id"))
        vnf_onboard_outs[key] = (os.popen(ns_onboard_string)).read()
    return vnf_onboard_outputs

def onboard_ns(parameters):
    ns_onboard_string = 'oclip vfc-catalog-onboard-ns -c {}'.format(parameters["ns-csar-id"])
    ns_onboard_out = (os.popen(ns_onboard_string)).read()
    return ns_onboard_out

def create_ns(parameters, csar_id):
    ns = parameters["ns"]
    ns_create_string = 'oclip vfc-nslcm-create -m {} -c {} -n {}'.format(parameters["vfc-url"], \
       csar_id, ns.get("name"))
    print ns_create_string
    ns_create_out = (os.popen(ns_create_string)).read()
    print ns_create_out
    ns_instance_id = (get_out_helper_2(ns_create_out))[3]
    return ns_instance_id

def instantiate_ns(parameters, ns_instance_id):
    ns_instantiate_string = 'oclip vfc-nslcm-instantiate -m {} -i {} -c {} -n {}'.format(parameters["vfc-url"], \
        ns_instance_id, parameters["location"], parameters["sdc-controller-id"])
    print ns_instantiate_string

    ns_instantiate_out = (os.popen(ns_instantiate_string)).read()
    return ns_instantiate_out

def create_ns_package(parameters):
    ns = parameters["ns"]
    create_ns_string = 'oclip vfc-catalog-create-ns -m {} -c {} -e {}'.format(parameters["vfc-url"], \
      ns.get("key"), ns.get("value"))
    cmd_out = (os.popen(create_ns_string)).read()
    out_list =  get_out_helper_2(cmd_out) 
    return out_list[4]

def create_vnf_package(parameters):
    vnfs = parameters["vnfs"]
    outputs = {}

    for vnf_key, vnf_values in vnfs.iteritems():
        create_vnf_string = 'oclip vfc-catalog-create-vnf -m {} -c {} -e {}'.format(parameters["vfc-url"], \
          vnf_values.get("key"), vnf_values.get("value"))
        cmd_out = (os.popen(create_vnf_string)).read()
        out_list =  get_out_helper_2(cmd_out) 
        outputs[vnf_key] = out_list[4]

    return outputs

def upload_ns_package(parameters, ns_package_output):
    ns = parameters["ns"]
    ns_upload_string = '{}/api/nsd/v1/ns_descriptors/{}/nsd_content'.format(parameters["vfc-url"], ns_package_output)
    print ns_upload_string
    print ns.get("path")
    resp = requests.put(ns_upload_string, files={'file': open(ns.get("path"), 'rb')})
    return resp

def upload_vnf_package(parameters, vnf_package_output):
    vnfs = parameters["vnfs"]
    for vnf_key, vnf_values in vnfs.iteritems():
        vnf_upload_str = '{}/api/vnfpkgm/v1/vnf_packages/{}/package_content'.format(parameters["vfc-url"], \
          vnf_package_output[vnf_key], vnf_package_output[vnf_key])
        resp = requests.put(vnf_upload_str, files={'file': open(vnf_values.get("path"), 'rb')})
    return resp


#Run Functions
parser = argparse.ArgumentParser()
parser.add_argument('-f', action='store', dest='config_file_path', help='Store config file path')
parser.add_argument('-t', action='store', dest='type', help='Store config file path')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

results = parser.parse_args()

config_file_path = results.config_file_path
if config_file_path is None:
    sys.exit(1)
config_file = open(config_file_path)
parameters = get_parameters(config_file)

# 1.Set cli command envionment
set_open_cli_env(parameters)

# 2.Create cloud complex
create_complex(parameters)

# 3.Register all clouds
register_all_clouds(parameters)

# 4.Register vnfm
register_vnfm(parameters)

# 5.create csar file
# 5.1 upload csar file to catalog
# 5.2 FIXME:Because SDC internal API will change without notice, so I will maually design VNF and Service.
# SDC output data model is not align with VFC, we use an workaround method
# We just do run time automation 
ns_package_output = ""

if type == "sdc":
    print "use csar file is distributed by sdc"
    # vnf_onboard_output = onboard_vnf(parameters)
    # print vnf_onboard_output
    # ns_onboard_out = onboard_ns(parameters)
    # print ns_onboard_out
else:
    print "use csar file is uploaded by local"
    vnf_package_output = create_vnf_package(parameters)
    print vnf_package_output
    ns_package_output = create_ns_package(parameters)
    print ns_package_output
    upload_vnf_out = upload_vnf_package(parameters, vnf_package_output)
    print upload_vnf_out
    upload_ns_out = upload_ns_package(parameters, ns_package_output)
    print upload_ns_out

# 6.add_policies function not currently working, using curl commands
# add_policies(parameters)

# 7. VFC part
ns_instance_id = create_ns(parameters, ns_package_output)
print ns_instance_id
instantiate_ns_output = instantiate_ns(parameters, ns_instance_id)
print instantiate_ns_output