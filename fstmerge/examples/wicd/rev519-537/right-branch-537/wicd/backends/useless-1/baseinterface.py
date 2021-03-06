class BaseInterface(object):
    """ A basic Interface to subclass for Wicd's use. """
    class XmlUiEventHandler(object):
        """ A class to handle the UI events. """
        pass
    class InterfaceException(Exception):
        """ Defines the basic exception for use in interfaces. """
        pass
    class CannotCreateInterfaceException(InterfaceException):
        """ Defines an exception for use in
        cases when an interface cannot be created. """
        pass
    @staticmethod
    def find_available_interfaces():
        """
        Static method. Returns a list of the interfaces of this type.
        Accepts:
        Nothing
        Returns:
        A list with zero or more strings of the names of interfaces.
        These names can be passed to __init__ to instantiate an object.
        """
        return []
    @staticmethod
    def get_type():
        return 'uninherited-interface'
    def dump_settings_to_dictionary(self):
        return {
            'name' : self.name,
            'interface_name' : self.interface_name,
            'type' : self.get_type()
            }
    def __init__(self, interface_name, status_change_callback):
        status_change_callback('initalizing')
        self.name = "Uninherited Interface"
        self.interface_name = interface_name
        self.status = "Uninherited"
        self._connected_to_network = False
        self.connected = False
        self.can_create_network_connection = False
        self.requires_network_connection = False
        self._use_tray_icon = False
        self.status_change_callback = status_change_callback
    def get_connected_to_network(self):
        """
        Returns a boolean indicating if the interface is connected to
        a network.
        Accepts:
        Nothing
        Returns:
        True if this interface has an IP address on a network,
        otherwise False.
        """
        return self._connected_to_network
    def get_status(self):
        """
        Returns a string containing a human readable description
        of the current status.
        Accepts:
        Nothing
        Returns:
        String containing current status.
        """
        return "Uninherited. Connected %s" % self.get_connected_to_network()
    def get_use_tray_icon(self):
        """
        Returns a boolean telling whether the current interface supports
        a tray icon.
        Accepts:
        Nothing
        Returns:
        True if the interface supports a tray icon, otherwise False
        """
        return self._use_tray_icon
    def do_update(self):
        """
        Calculates the current state.
        Accepts:
        Nothing
        Returns:
        Nothing
        """
        pass
    def do_update_icon(self):
        """
        Returns a list of image paths that can be merged (in order given)
        to create an icon that represents the interface status at the last
        call to do_update().
        Accepts:
        Nothing
        Returns:
        A list of image paths.
        """
        pass
    def connect(self):
        """
        Connects to a network.
        Accepts:
        TODO: figure what accepts
        Returns:
        TODO: figure out what is returned
        """
        pass
    def valid_new_interface_name(self, name):
        """
        Validates an interface name. A valid interface name is one that
        can be used to create a new interface using this class.
        Accepts:
        Name -- string containing interface name
        Returns:
        True if the name is valid, otherwise False.
        """
        return True
