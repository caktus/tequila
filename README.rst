Tequila
=======

This repository holds the documentation for a collection of `Ansible
<http://www.ansible.com/home>`_ roles for deployments of `Django
<https://docs.djangoproject.com/>`_ projects.  These exist primarily
to support the `Caktus Django project template
<https://github.com/caktus/django-project-template>`_.

`tequila-common <https://github.com/caktus/tequila-common>`_
    Install common system packages, set up server users and keys, add
    some basic security configuration, and create the standard project
    directory structure.

`tequila-nginx <https://github.com/caktus/tequila-nginx>`_
    Install and configure `nginx <https://nginx.org/en/docs/>`_ as a
    forwarding proxy for a Django project.

`tequila-django <https://github.com/caktus/tequila-django>`_
    Set up a Django project to run under `gunicorn
    <http://docs.gunicorn.org/en/stable/>`_ and/or `Celery
    <http://docs.celeryproject.org/en/latest/>`_.

`tequila-nodejs <https://github.com/caktus/tequila-nodejs>`_
    A thin wrapper around `geerlingguy/nodejs
    <https://github.com/geerlingguy/ansible-role-nodejs>`_,
    tequila-nodejs installs nodejs and npm, installs your project
    dependencies, and executes your front-end build script.

`tequila-postgresql <https://github.com/caktus/tequila-postgresql>`_
    Install a `PostgreSQL <https://www.postgresql.org/>`_ server and
    create a project database.

`tequila-rabbitmq <https://github.com/caktus/tequila-rabbitmq>`_
    Install and configure `RabbitMQ <https://www.rabbitmq.com/>`_ to
    use as a task queue for projects that use Celery.

Additionally, work is in progress on a couple more subprojects,

`tequila-cli <https://github.com/caktus/tequila-cli>`_
    A command-line Ansible wrapper that allows referencing inventories
    and playbooks in standard locations by more compact names, and
    allows for some actions that are difficult to do in a single
    command with standard Ansible.

`tequila-dokku <https://github.com/caktus/tequila-dokku>`_
    A role that sets up a Django project under `Dokku
    <http://dokku.viewdocs.io/dokku/>`_, a `Docker
    <https://docs.docker.com/>`_ -powered Platform-as-a-Service.


License
-------

The playbooks, roles, and code for this project are released under the
BSD License.  See the `LICENSE
<https://github.com/caktus/tequila/blob/master/LICENSE>`_ file for
more details.


Contributing
------------

If you think you've found a bug or are interested in contributing to this project
check out `tequila on Github <https://github.com/caktus/tequila>`_.

Development sponsored by `Caktus Consulting Group, LLC
<http://www.caktusgroup.com/services>`_.
