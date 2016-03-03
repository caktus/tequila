import argparse
import os
import os.path
from subprocess import check_call

import tequila

# TODO: Provide a way to pass additional arguments to ansible-playbook

# NOTE: To put literal "{" or "}" in these templates, we have to
# double them to "{{" or "}}".

INVENTORY_FILE_TEMPLATE = """# Inventory file for environment {envname}

# Put ALL hosts for THIS enviornment in the {envname} group, and also in
# any other groups corresponding to their roles.
[{envname}]
dbserver1 ansible_ssh_host="1.2.3.4"
generalpurpose1 ansible_ssh_host="1.2.3.5" ansible_user="user2"
generalpurpose2 ansible_ssh_host="1.2.3.6"

[db-master]
dbserver1

[worker]
generalpurpose1
generalpurpose2

[web]
generalpurpose1
generalpurpose2

# [queue]
# [cache]
"""

ALL_VARS_TEMPLATE = """---
# These variables will apply to all environments, roles, hosts, etc.
project_name: our_neat_project
python_version: 3.5
postgres_version: 9.4
ansible_sudo: true
users:
  - name: 'vagrant'
    public_keys:
      - 'ssh-rsa .........'
  - name: 'devuser1'
    public_keys:
      - 'ssh-rsa longkeystring== devuser1@example.com'
      - 'ssh-rsa anotherlongkeystring...  '
"""

ENV_VARS_TEMPLATE = """---
# These variables will apply to everything in the environment {envname}
domain: project-staging.example.com

repo:
  branch: develop
  url: git@github.com:caktus/caktus-website.git

# Actual secrets are in {env_secrets_file} with password in {password_file}.
# Edit secrets using
#  ansible-vault edit --vault-password-file={password_file} {env_secrets_file}
DB_PASSWORD: {{ secret_DB_PASSWORD }}
"""

SECRETS_FILE_TEMPLATE = """---
# Secrets file for environment {envname}
# Put password in {password_file} then encrypt this file using:
#  ansible-vault encrypt --vault-password-file={password_file} {env_secrets_file}
# and edit using
#  ansible-vault edit --vault-password-file={password_file} {env_secrets_file}
secret_DB_PASSWORD: noway
"""


def touch(filename, content, mode=None):
    """
    Create a file at `filename` containing `content`, but only if it
    doesn't already exist. Also creates any necessary intermediate directories.
    """
    if not os.path.exists(filename):
        print("Creating %s" % filename)
        fullpath = os.path.abspath(filename)
        directory = os.path.dirname(fullpath)
        if not os.path.isdir(directory):
            os.makedirs(directory)
        f = open(filename, "w")
        f.write(content)
        f.close()
        if mode:
            os.chmod(filename, mode)


def main():
    tequila_dir = os.path.dirname(tequila.__file__)

    tequila_roles_dir = os.path.join(tequila_dir, 'roles')
    if not os.path.exists(tequila_roles_dir):
        raise Exception("Something is wrong, tequila roles were expected to be at "
                        "%s but they're not" % tequila_roles_dir)

    roles_dirs = ['roles', tequila_roles_dir] + os.environ.get('ANSIBLE_ROLES_PATH', '').split(':')
    os.environ['ANSIBLE_ROLES_PATH'] = ':'.join(roles_dirs)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "envname",
        help="Required: name of the environment to deploy, e.g. 'staging' or 'production'",
    )
    parser.add_argument(
        "--newenv",
        action='store_true',
        help="Create the files for the environment specified as `envname` if they "
             "don't already exist, then exit.",
    )
    parser.add_argument(
        "--inventory",
        "-i",
        action='store',
        help="Use a different inventory file than the default."
    )
    args = parser.parse_args()
    envname = args.envname

    inventory_file = args.inventory or 'inventory/{}'.format(envname)
    global_vars_file = 'inventory/group_vars/all/vars.yml'
    env_vars_file = 'inventory/group_vars/{}/vars.yml'.format(envname)
    env_secrets_file = 'inventory/group_vars/{}/secrets.yml'.format(envname)
    password_file = '.vaultpassword-{envname}'.format(envname=envname)

    if args.newenv:
        print("Creating new environment {!r}".format(envname))
        context = dict(
            envname=envname,
            env_secrets_file=env_secrets_file,
            password_file=password_file,
        )
        touch(global_vars_file, ALL_VARS_TEMPLATE.format(**context))
        touch(inventory_file, INVENTORY_FILE_TEMPLATE.format(**context))
        touch(env_vars_file, ENV_VARS_TEMPLATE.format(**context))
        touch(env_secrets_file, SECRETS_FILE_TEMPLATE.format(**context))

        touch('.gitignore', '', mode=int('0600', base=8))
        if "%s\n" % password_file not in open('.gitignore').read():
            print("Updating .gitignore")
            with open('.gitignore', "a") as f:
                f.write("%s\n" % password_file)

        return

    if not os.path.exists(inventory_file):
        print("ERROR: No inventory file found at {!r}, is {!r} a valid environment?".format(inventory_file, envname))
        return
    if not os.path.exists(env_vars_file):
        print("ERROR: No vars file found at {!r}, is {!r} a valid environment?".format(env_vars_file, envname))
        return

    playbook_options = [
        '--become',
        '-i', inventory_file,
        #'-e', 'tequila_dir=%s' % tequila_dir,   # Do we need this?
        '-e', 'env_name=%s' % envname,
        '-e', 'local_project_dir=%s' % os.getcwd(),
    ]

    if os.path.exists(password_file):
        playbook_options.extend(['--vault-password-file', password_file])
    else:
        print("WARNING: No {} file found.  If Ansible vault complains, that\'s why.".format(password_file))

    command = ['ansible-playbook'] + playbook_options + ['%s/deploy.yml' % tequila_dir]

    print("Invoking ansible: {}".format(command))

    check_call(command)
