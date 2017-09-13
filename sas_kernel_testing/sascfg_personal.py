SAS_config_names = ['default', 'ssh']

SAS_config_options = {'lock_down': True}

SAS_output_options = {'output' : 'html5'}


default  = {
    'saspath': '/opt/sas9.4/install/SASHome/SASFoundation/9.4/bin/sas_u8',
    'options' : ["-fullstimer"]
}

ssh = {
    'saspath' : '/opt/sas9.4/install/SASHome/SASFoundation/9.4/bin/sas_u8',
    'ssh'     : '/usr/bin/ssh',
    'host'    : 'ec2-user@54.205.61.195',
    'options' : ["-fullstimer"]
}
