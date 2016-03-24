Tequila
=======

What is Tequila?

- it's a collection of reusable Ansible roles
- it's a script providing a simplified interface for the ``ansible``
  command-line program


New Projects
------------

Creation of new projects would be done using django-project-template,
just as we currently do for margarita.  Installing tequila would make
available the ``tequila`` command, providing a simplified interface
for ``ansible-playbook`` (and friends) that will be mostly familiar to
current users of the django-project-template fabric scripts.  There
would also be some mild changes to the project structure, i.e. the
location of the project-specific variables and custom playbooks, since
these would be kept distinct from paths where they might conflict with
the equivalent Salt files.

Much of this work has already been started, and is currently on the
``use_tequila`` branch of django-project-template.


Installation
------------

We would like to have the ability to pin projects to particular
versions of tequila.  It is also desirable to have an easy command to
install or upgrade tequila, along the lines of ``pip install``.

If we intend to make a ``tequila`` command available, it is
uncontroversial to make the Tequila project pip installable (and, in
fact, this work has already been done).  However, the big question is
how we should make the roles themselves available in a way that they
can be used by the project.

- ansible-galaxy
  - one of the Ansible community conventions for re-usable roles
  - supports versioning
  - no extra effort needed for the roles path
  - Ansible Galaxy community and tools are still immature
  - need to break up the roles into their own repos to conform to
    the limited structure acceptable by ``ansible-galaxy``

- git checkout
  - the other convention for re-usable roles
  - automatically on the roles path if checked out into the top of the
    project dir, but would need to be gitignored
  - would allow devs to check it out elsewhere easily, with only a
    setting to update
  - version checkout needs to be manually managed by the developer;
    easy to screw up and deploy with the wrong version

- git submodule
  - effectively gets versioning back
  - no extra effort needed to fix roles path
  - no need for a gitignore
  - nobody likes these

- catch-all deployment project
  - since the roles are only ever used by one thing, which covers all
    Caktus projects, there is no issue with role path
  - need to have one massive repo that has everything, even though you
    rarely need most of it
  - effective role sharing, but poor versioning

- decouple deployment from the project
  - fairly typically thing in the Ansible community
  - extra repo to manage, but may be ok if only devops use it
  - but re-usability of roles is poor, unless you have roles in yet
    another repo, and then you have the same path problem

- pip install the roles
  - hides the roles
  - installation process that is not standard for the Ansible
    community
  - extra work needed to make the roles available on the path:
    - need a wrapper script around ``ansible`` to point to where the
      roles are, making use of the plain command extremely inconvenient
    - or, need to symlink or unpack the roles (``$ tequila roles``) to the
      top project directory
    - or, need to inject an environment variable when using this
      virtualenv


Proposal 1: ``$ tequila roles`` command puts the roles in the right place
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Under this proposal, no changes to the structure of the Tequila
repository need to happen.  Running the ``tequila roles`` command
would symlink or copy the ``tequila/roles`` directory up to the
current working directory (which under most scenarios would be the
project directory), and this would generally not need to be run more
than once per local setup.

For development of the roles themselves, one could ``pip install -e
<local_tequila_copy>``, and the in-progress versions of the roles
would easily be made available for the ansible commands.

The pros:

- no changes to our Tequila repo structure
- could still run plain versions of ``ansible-playbook``

The cons:

- our roles would not be easily usable by members of the Ansible
  community


Proposal 2: separate ``tequila-<rolename>`` repos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If we retain Tequila as an open-sourced project, we should conform to
the conventions of the Ansible community to the best of our ability.
Since the Ansible community uses Ansible Galaxy (think: PyPI) and the
``ansible-galaxy`` command (think: pip) for packaging and distribution
of roles, we should do so as well.

So, what do we need to do to make tequila installable using
``ansible-galaxy``?  Roles are limited to one per repo or package,
with all of the directory structure for the role exposed at the top
level, i.e.

::

    myrole-repo/
        defaults/
        files/
        handlers/
        meta/
        tasks/
        templates/
        tests/
        vars/


Tequila, as it currently stands, both fails to have the structure
necessary for the installation process to complete without errors, and
also has additional layers of directories, preventing roles from being
correctly included from within playbooks.

With this proposal, we would move each individual role out into its
own repo, with the naming scheme ``tequila-<rolename>``.  Each role
repo would get a tagged release number when changes land in master.

The pros:

- we would not need to commit to publishing to the Ansible Galaxy
  site, since roles can also be installed by pointing to a repo
- particular versions of roles can be pinned
- roles can be installed using a ``requirements.yml`` file similar to
  a pip requirements file
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
- management of versions of all of these repos

For ease of installation, projects will have to ship with an
ansible-galaxy requirements file, and an ``ansible.cfg`` file
specifying a ``roles_path`` within the project's directory structure
(e.g. ``roles/``).  Example versions of these will need to be included
in django-project-template.

What is the point of the tequila repo, then?

The tequila repo, then, would be a pip-installable central
clearinghouse for these roles.  It would also get one overall tagged
release number tying together the release numbers for all of the
individual roles.  It could also ship with an installation script (``$
tequila roles``) that would call ``ansible-galaxy`` for all of the
tequila sub-repo versions relevant for the current tequila release.

People would still be free, however, to install individual tequila
roles by directly using ``ansible-galaxy``.  We may even wish to do
this for infrequently used roles that are only relevant for some
projects.

The remaining question is how to deal with development of the tequila
roles themselves.  How can developers try them out before release?
For installing feature branches, it should be sufficient to use the
branch name as the version in the ``ansible-galaxy`` command.  For
iterative development, we can edit the project's ``ansible.cfg``
in-place to include the repo for the role at the head of the
``roles_path`` variable.


Proposal 3: all commands must be ``tequila ...`` commands
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is how the current version of Tequila works (though the command
isn't currently called ``tequila``).

The ``tequila`` command sets an environment variable for the roles
path, pointing to the ``tequila/roles`` directory wherever pip
installed it.

The pros:

- we wouldn't have a ``roles/`` directory that would potentially get
  accidentally committed inside our project directory

The cons:

- no longer easily able to use Ansible commands directly


Secrets
-------

"Infrastructure as Code".

You shouldn't commit secrets to the repo, but you need them in order
to provision servers.

To solve this problem, the Ansible community has settled upon the use
of Ansible Vault, a symmetric encryption scheme exposed through the
ansible command-line client.  But this just begs the question of how
to share the key to decrypt the Vault files amongst the developers who
need it.  We could share this key via "sneakernet" or on the private
intranet, but a more convenient and secure method may be to use a
shared password in LastPass.  The Ansible Vault password file can be
executable, so we could write code using of one of the LastPass API
libraries to fetch the key.

So, how should we make use of Ansible Vault-encrypted files?
It isn't possible to use Vault only on lines or sections, it has to be
whole files.  So it's recommended to split out only those variables
that need to be secret into their own files, to minimize the opaque
binary blobs that get checked into the repo.  The structure would look
something like this,

::

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


Also, in the playbook and role tasks, make sure to set ``no_log:
true`` so that the secrets don't get echoed to the console when the
verbosity is turned up.

.. code-block:: yaml

    - name: VPN Server | Load VPN secret keys
      include_vars: "vpn-secrets.yml"
      no_log: true


For ease of use, we could do away with the secret/non-secret file
split for the dev environment.

Other possible options for sharing the Vault key:

- keep on the intranet (either vault files or keys for files)
- HashiCorp's Vault
- consul
- KeePassX

Sources:

- http://www.slideshare.net/excellaco/using-ansible-vault-to-protect-your-secrets


Configuration and Customization
-------------------------------

Ansible will look relative to the playbook directory or the inventory
directory for variable files and other such files, as well as in the
appropriate directories inside roles.  So in order to configure a
project, it is sufficient to have a set of directories named according
to convention that will contain needed configuration variables.  A
likely possibility is

::

    django-project-template/
        inventory/
            group_vars/
            host_vars/


This has mostly been done already in the ``use_tequila`` branch,
though some adjustments should be made in order to follow the
recommended secrets-vs-non-secrets structure.

The ``ansible.cfg`` that ships with the project will need to define
the inventory location.

Since the relevant playbook(s) for a project will ship inside that
project, customized tasks can be added directly in that file.  If
there are sufficient numbers of these tasks for it to be desirable,
additional playbooks can be constructed and put in a conventional
location in the project (e.g. ``playbooks/``), and then brought into
the main playbook using the ``include`` directive.


Dynamic Inventory Management
----------------------------

As with the password file, Ansible will accept a script for its
inventory file.  This opens up the possibility of having a *dynamic*
inventory.  Ansible itself ships with a few working examples,
including scripts for AWS EC2 and OpenStack.


Conversion From Margarita
-------------------------

Needed:

- one-shot playbook to remove Salt from the servers
- create the directory structure used by the tequila-specific portions
  of django-project-template
- skeletons of project-specific Ansible variables files
- parse and inject pillar data (including secrets?) into the Ansible
  vars files
- convert Salt grain info into inventory files
- default playbooks
- removal of Salt-specific files (``fabfile.py``, ``install_salt.sh``)
- checklist for things that should be manually converted
  (project-specific Salt states, updating ``README.rst``, etc.)

Only with Installation Proposal 2:

- default ``ansible.cfg``
- default tequila roles ``requirements.yml`` file


The main tequila repo could ship with a command (``$ tequila
convert``) that may be able to make these changes for us.
