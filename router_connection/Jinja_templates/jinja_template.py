# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
import yaml
import sys


def generate_cfg_from_template(templates, data_files):
    env = Environment(loader=FileSystemLoader('template'), trim_blocks=True)
    template = env.get_template(templates)
    vars_dict = yaml.load( open( data_files ) )
    result = template.render( vars_dict )
    return result


temp='fix_cust_template.txt'
vars_file='add_vlan_to_switch.yml'
test = generate_cfg_from_template(temp, vars_file)
print(test.split('\n'))