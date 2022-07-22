from setuptools import setup

long = """
PRTG API SIMPLIFIED
===================

This python package helps simplify the PRTG API (v1) by making the experience more pythonic.

The current methods are:

    * get_probe_list
    * get_sensor_list
    * get_device_list
    * get_object
    * remove_object
    * duplicate_device
    * resume_object
    * pause_object

To use these methods you must first create a PRTGServer object.
The parameters are:

    * server_address: The domain or IP address of the PRTG server
    * username: Your user account name (account should be an administrator)
    * password: Your user account password
    * passhash: Your user account passhash (a password alternative, the hash is found in account settings)
    * verify: Whether ssl is verified (See requests package documentation)

"""


setup(
    name='PRTGAPI',
    version='1.03',
    packages=['PRTGAPI'],
    url='https://github.com/The-Captain8/PRTG-API',
    license='https://github.com/The-Captain8/PRTG-API/blob/main/LICENSE',
    author='The-Captain8',
    author_email='',
    description='A package meant to make interfacing with the PRTG API more simple.',
    long_description_content_type='text/x-rst',
    long_description=long
)
