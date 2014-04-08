.. _installation-guide:

Installation guide
==================

*What follows is a guide which  describes how you can install the datalogger on various systems*

 * :ref:`setup`
 * :ref:`software`
 * :ref:`configure`

.. _setup:

Setting up linux
----------------

Install a stable linux distribution. The following explained steps are meant to use for debian, but will normally work on the most other distributions.
The following commands will set up the linux distribution to make it ready for using the datalogger. 

Use a kernel with following kernel parameters. This is only needed if you use the microcontroller.

.. code-block:: bash

  CONFIG_I2C=Y
  CONFIG_I2C_CHARDEV=Y

Create a user and set up a password.

.. code-block:: bash

  useradd {user-name}
  passwd {user-name}

Create a group called iouser.

.. code-block:: bash

  groupadd iouser 

Add the user to the iouser group.

.. code-block:: bash

  useradd -G iouser {user-name}

Add the following udev rules to give the iouser group access to the i2c and gpio pins:

.. code-block:: bash

  /etc/udev/rules.d/10-i2c.rules

  KERNEL="i2c-[0-9]*", GROUP="i2c"

Create a log directory and give change the rights and the owner to our user. It's possible to choose another directory to store log files in the :ref:`local configuration <configure>`.

.. code-block:: bash

  mkdir /var/log/datalogger
  chmod u+w /var/log/datalogger
  chown adekus

Optional: Set up gpio ports to have led functionality.

.. _software:

Installing software
-------------------

Install python2, pip, and following pip packages: ...


Install the following packages:

.. code-block:: bash

  rsync
  python
  python-pip
  python-smbus
  i2c-tools

And following pip packages:

.. code-block:: bash

  pip
  requests
  jsonschema
  configparser

.. _configure:

Configure datalogger
--------------------


Set local configuration parameters:



