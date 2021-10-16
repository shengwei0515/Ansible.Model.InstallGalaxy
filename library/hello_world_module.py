#!/usr/bin/python3
import shutil
from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec = dict(
            source=dict(required=True, type='str'),
            dest=dict(required=True, type='str')
        )
    )

    # action to do
    shutil.copy(module.params['source'], module.params['dest'])

    # setfact
    remote_facts = {
        'rc_source': module.params['source'],
        'rc_dest': module.params['dest']
    }

    module.exit_json(changed=True, ansible_facts=remote_facts)
    
if __name__ == '__main__':
    main()
