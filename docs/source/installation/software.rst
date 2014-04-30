Installing software
===================
Install python2, pip, and following pip packages: ...

Install the following debian packages:

.. code-block:: bash

  rsync
  python
  python-pip
  python-smbus
  git
  pip

with command:

.. code-block:: bash

  apt-get install rsync python python-pip python-smbus git 

And following pip packages:

.. code-block:: bash

  requests
  jsonschema
  configparser

with command:

.. code-block:: bash

  pip install requests jsonschema configparser

Go to a folder in your home folder where you want to install the datalogger software:

.. code-block:: bash

  cd ~

Download the datalogger:

.. code-block:: bash

  git clone https://github.com/jonathandb/datalogger.git
