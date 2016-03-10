Tequila
=======

New Projects
------------

Creation of new projects would be done using django-project-template,
just as we currently do for margarita.  Versions of the project
template which use tequila would have tequila-specific fabric scripts,
providing simplified wrappers with an interface mostly familiar to
current users around the necessary ansible-playbook commands.  There
would also be some mild changes to the project structure, i.e. the
location of the project-specific variables and custom playbooks, since
these would be kept distinct from paths where they might conflict with
the equivalent Salt files.

Much of this work has already been started, and is currently on the
use_tequila branch.


Installation
------------

We need to have the ability to pin projects to particular versions of
tequila.  It is also desirable to have an easy command to install or
upgrade tequila, along the lines of ``pip install``.

If we retain Tequila as an open-sourced project, we should conform to
the conventions of the Ansible community to the best of our ability.
Since the Ansible community uses Ansible Galaxy (think: PyPI) and the
``ansible-galaxy`` command (think: pip) for packaging and distribution
of roles, we should do so as well.

The pros:

- roles can be installed by pointing to a repo, instead of publishing
  to the Ansible Galaxy site
- particular versions of roles can be pinned
- roles can be installed using a file similar to a pip requirements
  file
- use of the ``ansible-galaxy`` command would allow installed tequila
  roles to live side-by-side with installed roles from the community
- conforming to community standards would allow our roles to be used
  in contexts outside of the django-project-template by other members
  of the community, using Ansible's standard tools

The cons:

- ``ansible-galaxy`` is very particular about the directory structure
  of roles that it can install
- due to that structure, there is a limit of one role per repo or
  "package"


For ease of installation, projects will have to ship with an
ansible-galaxy requirements file, and an ``ansible.cfg`` file
specifying a ``roles_path`` within the project's directory structure
(e.g. ``roles/``).  Example versions of these will need to be included
in django-project-template.

So, what do we need to do to make tequila installable using
``ansible-galaxy``?  Roles are limited to one per repo or package,
with all of the directory structure for the role exposed at the top
level, i.e.

..

    myrole-repo/
        defaults/
        files/
        handlers/
        meta/
        tasks/
        templates/
        tests/
        vars/


Tequila both fails to have the structure necessary for the
installation process to complete without errors, and also has
additional layers of directories, preventing roles from being
correctly included from within playbooks.

My recommendation is to move each individual role out into its own
repo, with the naming scheme ``tequila-<rolename>``.  Each role repo
would get a tagged release number when changes land in master.

.. FIXME

What is the point of the tequila repo, then?

People would still be free, however, to directly install individual
tequila roles using ``ansible-galaxy``.  We may even wish to do this
for infrequently used roles that are only relevant for some projects.

.. FIXME

How can we try out new versions of tequila roles before they are
released?

- branch name as the version in the ``ansible-galaxy`` command
- edit ``ansible.cfg`` in-place to include the repo for the role



.. FIXME

The caktus/tequila repo, then, would be a pip-installable central
clearinghouse for these roles.  It would also get a tagged release
number, and would have an installation script that would call
``ansible-galaxy`` for all of the tequila sub-repo versions relevant
for the current tequila release.


Secrets
-------

.. FIXME

Use Ansible Vault.  But how to share the secret to decrypt the Vault
files?

..

    group_vars/
        prod/
            secrets.yml
            non-secrets.yml
        staging/
            secrets.yml
            non-secrets.yml
        dev/
            secrets.yml
            non-secrets.yml


and then the ``non-secrets.yml`` files make use of variables defined
in ``secrets.yml``:

.. code-block:: yaml

    postgres_host: localhost
    postgres_database: pg_database
    postgres_user: pg_user
    postgres_password: {{ VAULT_POSTGRES_PASSWORD }}
    postgres_port: 5432


The Ansible Vault password file can be executable.

Checked-in files, even encrypted ones, can still be compromised.  Do
we *really* want to use Ansible Vault?

- shared password in LastPass
- keep on the intranet (either vault files or keys for files)
- consul
- KeePassX

- http://www.slideshare.net/excellaco/using-ansible-vault-to-protect-your-secrets


Configuration and Customization
-------------------------------

Ansible will look relative to the playbook directory or the inventory
directory for variable files and other such files, as well as in the
appropriate directories inside roles.  So in order to configure a
project, it is sufficient to have a set of directories named according
to convention that will contain needed configuration variables.  A
likely possibility is

..

    django-project-template/
        inventory/
            group_vars/
            host_vars/


This has mostly been done already in the ``use_tequila`` branch,
though some adjustments should be made in order to follow the
recommended secrets-vs-non-secrets structure.

The ``ansible.cfg`` that ships with the project will need to define
the inventory location.

Since the relevant playbook for a project will ship inside that
project, customized tasks can be added directly in that file.  If
there are sufficient numbers of these tasks for it to be desirable,
additional playbooks can be constructed and put in a conventional
location in the project (e.g. ``playbooks/``), and then brought into
the main playbook using the ``include`` directive.


Dynamic Inventory Management
----------------------------


Conversion From Margarita
-------------------------

Needed:

- one-shot playbook to remove Salt from the servers
- create the directory structure used by the tequila-specific portions
  of django-project-template
- skeletons of project-specific Ansible variables files
- convert existing knowledge about servers into inventory files?
- tequila-specific commands
- default ``ansible.cfg``
- default tequila roles ``requirements.yml`` file
- default playbooks
- updates to README.rst?
- checklist for things that should be manually converted
  (project-specific Salt states, removal of fabfiles, etc.)


The main tequila repo could ship with a script that could make these
changes.
