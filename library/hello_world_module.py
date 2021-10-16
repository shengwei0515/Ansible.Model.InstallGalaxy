#!/usr/bin/python3
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: hello_word_module

short_description: a poc for ansible module

version_added: "1.0.0"

description: just a poc

options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str

author:
    - Small Seal
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test_info:
    name: hello world
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
my_useful_info:
    description: The dictionary containing information about your system.
    type: dict
    returned: always
    sample: {
        'foo': 'bar',
        'answer': 42,
    }
'''
from ansible.module_utils.basic import AnsibleModule
import shutil

def main():

    module_args = dict(
        name=dict(type='str', required=True)
    )


    result = dict(
        changed=False,
        original_message = '',
        message='',
        my_useful_info={}
    )


    module = AnsibleModule(
        argument_spec = module_args,
        supports_check_mode = True
    )

    # if you use --ckeck flag when run playbook, return the current variable status
    if module.check_mode:
        module.exit_json(**result)

    result['original_message'] = module.params['name']
    result['message'] = 'goodbye'
    result['my_useful_info'] = {
        'foo': 'bar',
        'answer': 42,
    }

    module.exit_json(**result)
    
if __name__ == '__main__':
    main()
