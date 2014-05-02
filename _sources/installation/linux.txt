Setting up linux
================

Install a stable linux distribution. The following explained steps are meant to use for debian, but will normally work on the most other distributions. The following commands will set up the linux distribution to make it ready for using the datalogger.

.. seealso::

  In case you are using the cubieboard you can find read to use linux images on http://linux-sunxi.org/Bootable_OS_images

Setting kernel parameters
-------------------------
 Setting kernel parameters is only needed if you use the microcontroller as a proxy between the ARM board and the modbus slave. If this is the case, use a kernel with following kernel parameters.

.. code-block:: bash

  CONFIG_I2C=Y
  CONFIG_I2C_CHARDEV=Y


Setting up the linux environment
--------------------------------

Create a user and set up a password.

.. code-block:: bash

  useradd {user-name}
  passwd {user-name}

Create a group called iouser.

.. code-block:: bash

  groupadd iousers

Add the user to the iouser group.

.. code-block:: bash

  useradd -G iousers {user-name}

Add the following udev rules to give the iouser group access to the i2c and gpio pins:

.. code-block:: bash

  # /etc/udev/rules.d/10-i2c.rules
  KERNEL="i2c-[0-9]*", GROUP="iousers"

.. note::

  The i2c rule is only needed when using the microcontroller as a proxy between the ARM board and the modbus slave.

Create a log directory and give change the rights and the owner to our user. It’s possible to choose another directory to store log files in the local configuration.

.. code-block:: bash

  mkdir /var/log/datalogger
  chmod u+w /var/log/datalogger
  chown {user-name}

Optional: Set up gpio ports to enable led functionality.


