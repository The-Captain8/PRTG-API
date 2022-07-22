PRTG API SIMPLIFIED
===================

https://pypi.org/project/PRTGAPI/1.0/

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

