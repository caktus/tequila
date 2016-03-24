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

The Ansible community seems to have coalesced around two main schemes
for reusing roles across multiple deployment projects: installation
using ``ansible-galaxy``, or checking out the roles repo to some
conventional location.

Proposal 1: installation using ``ansible-galaxy``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the intended method provided by the Ansible project to allow
the publishing and reuse of roles across the entire Ansible community.
The Ansible Galaxy site (think: PyPI) is used to publish packaged
roles, and the ``ansible-galaxy`` command (think: pip) is used to
install those roles.

So, what do we need to do to make Tequila's roles installable using
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
We would not need to immediately commit to publishing to the Ansible
Galaxy site, since roles can also be installed by pointing to a repo

The pros:

- particular versions of roles can be pinned for each project
- no further effort would be needed to place installed roles on the roles path
- the standard ``ansible`` commands would work without any additional effort
- roles can be installed using a ``requirements.yml`` file similar to a pip requirements file
- use of the ``ansible-galaxy`` command would allow installed tequila roles to live side-by-side with installed roles from the community
- conforming to community standards would allow our roles to be used in contexts outside of the django-project-template by other members of the community, using Ansible's standard tools

The cons:

- ``ansible-galaxy`` is very particular about the directory structure of roles that it can install
- due to that structure, there is a limit of one role per repo or "package"
- management of all of these repos, and the versions thereof

For ease of installation, projects will have to ship with an
ansible-galaxy requirements file, and an ``ansible.cfg`` file
specifying a ``roles_path`` within the project's directory structure
(e.g. ``roles/``).  Example versions of these will need to be included
in django-project-template.

Under this proposal, the Tequila repo itself would be reduced to only
providing the simplified Ansible CLI, and the minimal files necessary
for conversions of existing django-project-template projects to use
Tequila.

Proposal 2: conventional location
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The roles would remain in a single centralized repository, which would
then need to be checked out in a standard location by the developer in
order to be available to the ``ansible`` command, typically in the top
level directory or ``deployment/`` sub-directory of the codebase to be
deployed.  This option easily allows checkout of the roles repo
elsewhere on the developer's system, however, with only the minor
extra effort of setting the ``roles_path`` Ansible configuration
setting.  The advantage here is we have a single repo to manage
instead of multiple, and versioning can be kept consistent over the
entire set of roles.  However, which version actually gets used to
deploy a given project will be up to the developer to manage, making
this choice fragile if we do wind up pinning a bunch of different
versions of Tequila to different projects.  This problem may be
mitigated by using git submodules, but that brings in its own
problems.


Other options in use, either by the community or by the existing
version of Tequila, include,

Catch-all deployment project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One repo would contain not only all roles used by Caktus projects, but
also each separate project's deployment configuration and inventory
files.  Since the roles are only ever used in this one repo, there is
no issue with role path, and the roles themselves are properly reused.
The downside is that developers would need to checkout and use this
one massive repo that has everything, even though you rarely need most
of it.  Also, management of the versioning would be awkward if the
different projects need different versions of the deployment project
pinned.

Decouple deployment from the project entirely
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each project would have its own separate deployment repo, which would
contain the configuration and inventory for that project.  This is a
fairly typical practice in the Ansible community.  However, the
problem with this is that the re-usability of roles is poor unless you
have the shared roles in yet another repo, and then you still have the
roles path problem.

Install the roles using pip
~~~~~~~~~~~~~~~~~~~~~~~~~~~

As far as I can tell, this option is not used by the wider Ansible
community.  It hides the roles, making it extremely inconvenient to
use the standard Ansible tools, and necessitates extra work to make
the roles available on the path:

- need a wrapper script around ``ansible`` to point to where the roles are, making use of the plain command extremely inconvenient
- or, need to symlink or unpack the roles (``$ tequila roles``) to the top project directory
- or, need to inject an environment variable when the virtualenv is active


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
- default ``ansible.cfg`` (if needed)
- default tequila roles ``requirements.yml`` file (if needed)


The main tequila repo could ship with a command (``$ tequila
convert``) that may be able to make these changes for us.
