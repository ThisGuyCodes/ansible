#!/usr/bin/python

DOCUMENTATION = ""

EXAMPLES = ""

RETURN = ""

from ansible.module_utils.basic import AnsibleModule

def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        gpg_url=dict(type='str', required=True),
        repo_url=dict(type='str', required=True),
        repo_name=dict(type='str', required=False, default='main'),
        distro=dict(type='str', required=True),
    )

    result = dict(
        changed=False,
        original_message='',
        message='',
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    if module.check_mode:
        pass



def main():
    run_module()

if __name__ == '__main__':
    main()