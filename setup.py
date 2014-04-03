from distutils.core import setup

setup(
    name='Datalogger',
    version='0.1.0',
    author='Jonathan De Beir',
    author_email='jonathan.de.beir@gmail.com',
    packages=['datalogger'],
    install_requires=['requests',
                      'jsonschema',
                      'apscheduler',
                      'configparser'],
    scripts=['bin/datalogger'],
    description='Logs data from modbus slaves or your own data source.',
)
