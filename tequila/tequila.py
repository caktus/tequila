import argparse
import os
from subprocess import check_call

# TODO: Provide a way to pass additional arguments to ansible-playbook


def convert(args):
    print(args)


def install(args):
    print(args)


def new(args):
    print(args)


def deploy(args):
    command = ['ansible-playbook']

    inventory_file = os.path.join(
        'deployment', 'environments', args.envname, 'inventory')
    if not os.path.exists(inventory_file):
        print("ERROR: No inventory file found at {!r},"
              " is {!r} a valid environment?".format(inventory_file, envname))
        return

    if args.playbook == 'site.yml':
        playbook_file = os.path.join('deployment', 'site.yml')
    else:
        playbook_file = os.path.join(
            'deployment', 'playbooks', args.playbook)
    if not os.path.exists(playbook_file):
        print("ERROR: No playbook file found at {!r}.".format(playbook_file))
        return

    command.extend([
        '--become',
        '-i', inventory_file,
        playbook_file,
    ])

    print("Invoking ansible: {}".format(command))
    check_call(command)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="sub-command help")

    parser_convert = subparsers.add_parser('convert', help="convert help")
    parser_convert.set_defaults(func=convert)

    parser_install = subparsers.add_parser('install', help="install help")
    parser_install.set_defaults(func=install)

    parser_new = subparsers.add_parser('new', help="new help")
    parser_new.set_defaults(func=new)
    parser_new.add_argument(
        'envname',
        help=("Required: name of the new environment to create an inventory"
              " and vars files for.")
    )

    parser_deploy = subparsers.add_parser('deploy', help="deploy help")
    parser_deploy.set_defaults(func=deploy)
    parser_deploy.add_argument(
        'envname',
        help=("Required: name of the environment to deploy to, e.g. 'staging'"
              " or 'production'.")
    )
    parser_deploy.add_argument(
        'playbook', nargs='?', default='site.yml',
        help=("Optional: name of the Ansible playbook to execute.")
    )

    args = parser.parse_args()
    args.func(args)
