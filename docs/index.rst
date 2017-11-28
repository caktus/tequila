Tequila
=======

Tequila is a set of `Ansible <https://www.ansible.com/>`_ roles and
other tooling useful for deploying `Django
<https://www.djangoproject.com/>`_ projects.


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

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   build_documentation


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
