
#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: install_galaxy_collection
short_description: a module to instll collections by ansible-galaxy command
version_added: 0.1.0
description:
    this module is used for install ansible collections by ansible-galaxy command
options:
    name:
        description: the identity to verify each installed result
        required: true
        type: str
    src:
        description: the ansible collection source name, may be a collection name or url to find collection
        required: true
        type: str
    src_type:
        description: the src type of collection, different type may use different command to install
        required: true
        type: str
        choices: [ "git-ssh"]
    version:
        description: the version of this collection
        requritd: true
        type: str
    fource:
        description: to decide if need to add --force flag
        type: bool
        default: true
    installed_root_path
        description: where to install the collection
        type: str
        default: ./.ansible
    skip_versions
        description: version in skip_versions will no install
        type: list
        elements: str
        default: []
'''

EXAMPLES = r'''
- name: run library/install_galaxy
    install_galaxy_collection:
    name: <a_name_for_install_result>
    src: <ssh_git_url_of_this_collection>
    src_type: git-ssh
    version: <git_branch_for_this_collection>
    fource: yes
    installed_root_path: "./.ansible"
    skip_versions:
        - "develop"
        - ""
'''

RETURN = r'''
install_command:
    description: ansible-galaxy command to install collections
    type: str
rc:
    description: the return code after run ansible-galaxy command
    rype: int
stdout_lines:
    description: the stdout after run ansible-galaxy command
    rype: list
    elements: str
stderr_lines
    description: the stderr after run ansible-galaxy command
    rype: list
    elements: str
'''


from ansible.module_utils.basic import AnsibleModule
import os
import shlex

class SrcTypeNotSupportException(BaseException):
    pass

support_src_type = {
    "ssh-git": 'ssh-git'
}

def main():
    arguments = dict(
        name = dict(type="str", required=True),
        src = dict(type="str", required=True),
        src_type = dict(type="str", required=True, choices= ["git-ssh"]),
        version = dict(type='str', default=''),
        fource = dict(type='bool', default=True),
        installed_root_path = dict(type='str', default='./.ansible'),
        skip_versions = dict(type='list', elements='str')
    )

    module = AnsibleModule(
        argument_spec = arguments,
        supports_check_mode = True
    )

    if version_need_to_skip(module.params["version"], module.params["skip_versions"]):
        module_skip_when_version_need_to_skip(module)
    else:
        module_run_to_install_ansible_collection(module)


def module_skip_when_version_need_to_skip(ansible_module):
    result = {}
    result['skipped'] = True
    result['stdout_lines'] = "{} in skip version list, skip this".format(ansible_module.params["version"])

    if ansible_module.check_mode:
        ansible_module.exit_json(**result)
    ansible_module.exit_json(**result)

def module_run_to_install_ansible_collection(ansible_module):
    result = {}
    ansible_galaxy_command = ansible_galaxy_command_factory(ansible_module)

    result['install_command'] = ansible_galaxy_command

    if ansible_module.check_mode:
        ansible_module.exit_json(**result)

    result['rc'], stdout, stderr = ansible_module.run_command(args=shlex.split(ansible_galaxy_command))
    result['stdout_lines'] = stdout.split('\n')
    result['stderr_lines'] = stderr.split('\n')
    result['changed'] = True

    ansible_module.exit_json(**result)

def ansible_galaxy_command_factory(ansible_module):

    collection_installed_dest = os.path.join(ansible_module.params['installed_root_path'],
                                             ansible_module.params['name'])
    ansible_galaxy_command = ""

    if ansible_module.params['src_type'] == "git-ssh":
        ansible_galaxy_command = "ansible-galaxy collection install {collection_source},{collection_version} -p {collections_path} {if_force_flag}".format(
                                collection_source=ansible_module.params['src'],
                                collection_version=ansible_module.params['version'],
                                collections_path=collection_installed_dest,
                                if_force_flag='--force' if ansible_module.params['fource'] else ''
                              )
    else:
        raise SrcTypeNotSupportException("ansible_galaxy_command_factory not support src_type: {}".format(ansible_module.params['src_type']))
    return ansible_galaxy_command

def version_need_to_skip(version, skip_versions_list):
    if version in skip_versions_list:
        return True
    else:
        return False

if __name__ == '__main__':
    main()
