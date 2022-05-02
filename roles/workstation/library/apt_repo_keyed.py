#!/usr/bin/python

DOCUMENTATION = ""

EXAMPLES = ""

RETURN = ""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url
from hashlib import sha256

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

    gpg_key_location = '/usr/share/keyrings/'+module.params['name']+'.gpg'
    apt_list_location = '/etc/apt/sources.list.d/'+module.params['name']+'.list'

    gpg_response, gpg_info = fetch_url(module, module.params['gpg_url'], method='GET')
    if gpg_info['status'] >= 400:
        module.fail_json('Error retrieving gpg key from provided URL')

    gpg_raw = gpg_response.read().decode('utf8')
    rc, gpg_converted, _ = module.run_command('gpg --yes --dearmor', data=gpg_raw)
    if rc != 0:
        module.fail_json(**result)
    
    gpg_converted = gpg_converted.encode('utf-8')
    
    gpg_sha_expected = sha256(gpg_converted)
    gpg_sha_actual = module.sha256(gpg_key_location)

    if gpg_sha_expected.hexdigest() != gpg_sha_actual:
        result['changed'] = True
        if not module.check_mode:
            with open(gpg_key_location, 'wb') as gpg_key_file:
                gpg_key_file.write(gpg_converted)
    
    apt_line = "deb [signed-by={gpg}] {url} {distro} {name}\n".format(
        gpg=gpg_key_location,
        url=module.params['repo_url'],
        distro=module.params['distro'],
        name=module.params['repo_name'],
    ).encode('utf8')
    apt_sha_expected = sha256(apt_line)
    apt_sha_actual = module.sha256(apt_list_location)
    if apt_sha_expected.hexdigest() != apt_sha_actual:
        result['changed'] = True
        if not module.check_mode:
            with open(apt_list_location, 'wb') as apt_list_file:
                apt_list_file.write(apt_line)
    
    module.exit_json(**result)







def main():
    run_module()

if __name__ == '__main__':
    main()