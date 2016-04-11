Tequila
=======

This repository provides a command-line interface to simplify the use
of `Ansible <http://www.ansible.com/home>`_ for deployments, primarily
to support the `Caktus Django project template
<https://github.com/caktus/django-project-template>`_ and the
associated Tequila Ansible roles:

- `tequila-common <https://github.com/caktus/tequila-common>`_
- `tequila-postgresql <https://github.com/caktus/tequila-postgresql>`_
- `tequila-nginx <https://github.com/caktus/tequila-nginx>`_
- `tequila-django <https://github.com/caktus/tequila-django>`_
- `tequila-rabbitmq <https://github.com/caktus/tequila-rabbitmq>`_


License
-------

This code is released under the BSD License.  See the `LICENSE
<https://github.com/caktus/tequila/blob/master/LICENSE>`_ file for
more details.


Contributing
------------

If you think you've found a bug or are interested in contributing to this project
check out `tequila on Github <https://github.com/caktus/tequila>`_.

Development sponsored by `Caktus Consulting Group, LLC
<http://www.caktusgroup.com/services>`_.


Installation
------------

* Create & activate a virtualenv for your project.
* Add tequila to your project requirements, e.g.  in
  ``requirements.txt``::

    git+https://github.com/caktus/tequila.git@0.0.1

* Install the tequila package into your virtualenv, e.g.::

    pip install -r requirements.txt


Project Structure
-----------------

* In your project's top-level directory (which will be the current
  directory when you run deploys), create a ``deployment/`` directory.

* Inside of the ``deployment/`` directory, create directories called
  ``environments/`` and ``playbooks/``.

* For each environment (e.g. `staging`, `production`), create an
  `Ansible inventory file
  <http://docs.ansible.com/ansible/intro_inventory.html>`_ named
  ``$(PWD)/deployment/environments/<envname>/inventory``.  The
  inventory file is an ``ini``-format file.

  The purpose of the inventory file is to specify which hosts are
  serving which roles in the deploy, *and* how to connect to them. To
  do this, servers should be added to the groups "db", "web", "queue",
  and "worker" as appropriate, and variables such as
  ``ansible_ssh_host`` and ``ansible_ssh_user`` can be set on
  individual hosts.

  Example::

    # file: deployment/environments/staging/inventory

    # We can give the servers convenient "names" here, and then use
    # ansible_ssh_host and other variables to tell Ansible how
    # to connect to them.

    server1 ansible_ssh_host=ec2-gibberish.more.long.domain
    server2 ansible_ssh_host=ec2-gibberish2.more.long.domain

    [web]
    server1

    [db]
    server2

    [queue]
    # no queue yet for this project

    [worker]
    # no workers yet for this project

* In the ``$(PWD)/deployment/playbooks/`` directory, create a playbook
  called ``site.yml``.  This will be the playbook that deploys the
  entire site, and should merely include a set of more finely-grained
  playbooks for each service type, e.g.::

    ---
    # file: deployment/playbooks/site.yml
    #
    # This playbook will deploy an entire environment
    #
    - include: db.yml
    - include: web.yml
    - include: queue.yml
    - include: worker.yml

  Each of these sub-playbooks should specify the hosts affected and
  the roles to be used, e.g.::

    ---
    # file: deployment/playbooks/db.yml
    #
    # This playbook will deploy a database server using postgresql
    #
    - hosts: db
      roles:
        - tequila-common
        - tequila-postgresql

* At the top of the ``deployment/`` directory, create a
  ``requirements.yml`` file.  This file is the Ansible equivalent of a
  pip ``requirements.txt`` file, specifying which Ansible roles and
  what versions are to be used with this project, e.g.::

    ---
    # file: deployment/requirements.yml
    #
    - src: https://github.com/caktus/tequila-common
      version: master

    - src: https://github.com/caktus/tequila-nginx
      version: master

    - src: https://github.com/caktus/tequila-django
      version: master

    - src: https://github.com/caktus/tequila-postgresql
      version: master

    - src: https://github.com/caktus/tequila-rabbitmq
      version: master

  If you need to install specific branches of the roles (for Ansible
  >= 2.1.0),::

    ---
    - src: https://github.com/caktus/tequila-common
      version: branchname

    - src: https://github.com/caktus/tequila-nginx
      version: branchname

    - src: https://github.com/caktus/tequila-django
      version: branchname

    - src: https://github.com/caktus/tequila-postgresql
      version: branchname

    - src: https://github.com/caktus/tequila-rabbitmq
      version: branchname

  This doesn't work properly for Ansible < 2.1.0, but can be worked around,::

    ---
    - src: https://github.com/caktus/tequila-common/archive/branchname.tar.gz
      name: tequila-common

    - src: https://github.com/caktus/tequila-nginx/archive/branchname.tar.gz
      name: tequila-nginx

    - src: https://github.com/caktus/tequila-django/archive/branchname.tar.gz
      name: tequila-django

    - src: https://github.com/caktus/tequila-postgresql/archive/branchname.tar.gz
      name: tequila-postgresql

    - src: https://github.com/caktus/tequila-rabbitmq/archive/branchname.tar.gz
      name: tequila-rabbitmq


Where to set variables
----------------------

Ansible supports setting variables in many places.  Here are some
recommended conventions:

* Variables telling Ansible how to connect to a particular host go into
  the inventory file, on the same line as the first mention of that
  host.

* Each environment directory and the playbooks directory may have
  either a ``group_vars/`` subdirectory or a ``host_vars/``
  subdirectory, or both.  These directories can then contain files or
  directories named for the group (in ``group_vars/``) or the host (in
  ``host_vars/``), which will then have their contents automatically
  included when that environment is deployed or playbook is executed.

  The special group name ``all`` will match all groups.

* Variables that are global to the project go in
  ``deployment/playbooks/group_vars/all.yml``, or if more modularity
  is needed, ``deployment/playbooks/group_vars/all/<filename>.yml``::

    ---
    # file: deployment/playbooks/group_vars/all.yml
    project_name: our_project
    python_version: 3.4
    less_version: 2.1.0
    postgres_version: 9.3

* Variables that apply to all servers in a particular environment go
  in ``deployment/environments/<envname>/group_vars/all.yml`` or
  ``deployment/environments/<envname>/group_vars/all/<filename>.yml``::

    ---
    # file: deployment/environments/staging/group_vars/all/vars.yml
    domain: project-staging.example.com
    repo:
      url: git@github.com:caktus/caktus-website.git
      branch: develop

* Variables whose values should be secret (such as passwords and API
  keys) should be kept in separate variable files, named by convention
  ``secrets.yml``, that get encrypted using ``ansible-vault``.  Only
  secret values should be kept in encrypted files.  Since such secrets
  will probably be specific to the environment, we recommend that they
  be placed in
  ``$(PWD)/deployment/environments/<envname>/all/secrets.yml``.  All
  variables defined in such encrypted files should then be exposed in
  a corresponding non-encrypted file ::

    ---
    # file: deployment/environments/staging/group_vars/all/secrets.yml
    SECRET_DB_PASSWORD: "value of password"

    ---
    # file: deployment/playbooks/group_vars/all.yml
    db_password: {{ SECRET_DB_PASSWORD }}

  By convention, names of variables placed in encrypted files should
  have the prefix ``SECRET_``.  (This two-step approach to secret
  variables is recommended as an `Ansible best practice
  <http://docs.ansible.com/ansible/playbooks_best_practices.html#variables-and-vaults>`_).

* Put the passwords for the Ansible vault in files named ``.vaultpassword-<envname>``.
  Be *sure* that (1) they do not get added to version control, and (2) they
  are not public (e.g. set permissions to 0600).  E.g.::

      echo ".vaultpassword*" >>.gitignore
      echo "password" >.vaultpassword-staging
      chmod 600 .vaultpassword-staging


Deployment
----------

* Run ``tequila deploy <envname>`` to update servers.  E.g.::

    tequila deploy staging

  or::

    tequila deploy production


TODO for this README
--------------------

TODO: Add full documentation for the ``tequila`` script.

TODO: Create more detailed documentation, including which groups to use and
what variables need to be set, and lots of examples of the whole process
