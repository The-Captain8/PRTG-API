import requests
import urllib3


class PRTGServer:
    def __init__(self, server_address: str, username: str, password: str = None, passhash: str = None,
                 verify: bool = False):
        """
        A PRTG server object

        :param server_address: The domain or IP address of the PRTG server
        :param username: Your user account name (account should be an administrator)
        :param password: Your user account password
        :param passhash: Your user account passhash (a password alternative, the hash is found in account settings)
        :param verify: Whether ssl is verified (See requests package documentation)
        """
        self.server_address = server_address
        self.username = username

        if passhash:
            self.password = passhash
            self.auth = f'&username={username}&passhash={passhash}'
        elif password:
            self.password = password
            self.auth = f'&username={username}&password={password}'
        else:
            raise ValueError('Either a password or passhash is required.')

        self.verify = verify
        urllib3.disable_warnings()

    def get_probe_list(self, count=500, root_id=0):
        """
        Gets a list of probes from the PRTG server.

        :param count: Determines the maximum of devices returned. Default is 500.
        :param root_id: The ID of the root group, where probes are typically under. Most common id is 0 (default) or 1.
        :return: A list of JSON objects is returned containing the object id and name of each probe.
        """
        response = requests.get(
            f"https://{self.server_address}/api/table.json?content=probes&columns=objid,name&filter_parentid={root_id}&count={count}{self.auth}",
            verify=self.verify)

        return response.json()['probes']

    def get_sensor_list(self, device_id, count=500):
        """
        Gets a list of all the sensors from a given device.

        :param count: Determines the maximum of sensors returned. Default is 500.
        :param device_id: Object ID of the device to retrieve sensors from
        :return: A list of the devices sensors in JSON format.
        """
        response = requests.get(
            f"https://{self.server_address}/api/table.json?content=sensors&columns=objid,device,sensor,status&id={device_id}&count={count}{self.auth}",
            verify=self.verify)

        return response.json()['sensors']

    def get_device_list(self, count=500):
        """
        Gets a list of all the devices.

        :param count: Determines the maximum of devices returned. Default is 500.
        :return: A list of the devices in JSON format.
        """
        response = requests.get(
            f"https://{self.server_address}/api/table.json?content=devices&columns=objid,probe,group,device,host,name,status&count={count}{self.auth}",
            verify=self.verify)

        return response.json()['devices']

    def get_object(self, object_id=None, object_name: str = None):
        """
        Gets a specific object (probe, device, sensor) from either its name or ID.

        :param object_id: Object ID of the object.
        :param object_name: The name of the object.
        :return: A list of the object attributes in JSON format.
        """
        if not object_id and not object_name:
            raise ValueError('Object ID or Object Name parameter is required.')

        if object_id:
            response = requests.get(
                f"https://{self.server_address}/api/table.json?output=json&columns=objid,probe,group,device,host,name,status&filter_objid={object_id}{self.auth}",
                verify=self.verify)

        else:
            response = requests.get(
                f"https://{self.server_address}/api/table.json?output=json&columns=objid,probe,group,device,host,name,status&filter_name=@sub({object_name}){self.auth}",
                verify=self.verify)

        try:
            response = response.json()[""][0]
        except IndexError:
            response = None
            print('Error finding object with that ID/name.')

        return response

    def remove_object(self, object_ID: str):
        """
        Removes an object in PRTG.

        :param object_ID: The ID of the object (sensor, device, probe, ect.).
        :return: The response from the server.
        """

        response = requests.get(
            f"https://{self.server_address}/api/deleteobject.htm?id={object_ID}&approve=1{self.auth}",
            verify=self.verify)

        return response

    def duplicate_device(self, template_device_id, device_name, device_ip, device_group_id):
        """
        Duplicates a device.

        :param template_device_id: Object ID of the device to be duplicated.
        :param device_name: Name of the device to be created.
        :param device_ip: IP address of the device to be created.
        :param device_group_id: Group for the new device to go into.
        :return: The response from the server.
        """
        response = requests.get(
            f"https://{self.server_address}/api/duplicateobject.htm?id={template_device_id}&name={device_name}&host={device_ip}&targetid={device_group_id}{self.auth}",
            verify=self.verify)

        return response

    def resume_object(self, object_ID):
        """
        Resumes an object in PRTG.

        :param object_ID: The ID of the object (sensor, device, probe, ect.).
        :return: The response from the server.
        """
        response = requests.get(
            f"https://{self.server_address}/api/pause.htm?id={object_ID}&action=1{self.auth}",
            verify=self.verify)

        return response

    def pause_object(self, object_ID):
        """
        Resumes an object in PRTG.

        :param object_ID: The ID of the object (sensor, device, probe, ect.).
        :return: The response from the server.
        """
        response = requests.get(
            f"https://{self.server_address}/api/pause.htm?id={object_ID}&action=0{self.auth}",
            verify=self.verify)

        return response
