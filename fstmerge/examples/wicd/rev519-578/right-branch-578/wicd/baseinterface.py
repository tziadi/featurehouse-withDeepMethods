from misc import WicdError
import os, inspect
def needsidle(method):
    '''
    Can be used as a decorator to raise an
    error if the interface is not idle.
    '''
    def idlecheck(self, *args, **kwargs):
        if not (self._status == 'idle'):
            raise WicdError('Interface is not idle.')
        return method(self, *args, **kwargs)
    idlecheck.func_name = method.func_name
    return idlecheck
class BaseInterface(object):
    """ A basic Interface to subclass for Wicd's use. """
    class InterfaceException(WicdError):
        """ Defines the basic exception for use in interfaces. """
        pass
    class CannotCreateInterfaceException(WicdError):
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
    def get_name(self):
        return self.name
    def dump_settings_to_dictionary(self):
        return {
            'name' : self.name,
            'interface_name' : self.interface_name,
            'type' : self.get_type()
            }
    def do_save(self):
        '''
        Will save the interface configuration. Normally, you won't need this.
        Accepts:
        Nothing
        Returns:
        Nothing
        '''
        pass
    def __init__(self, interface_name, callback):
        self.status_change_callback = callback[0]
        self.state_change_callback = callback[1]
        self.status_change_hooks = []
        self.previous_status = 'none'
        self._status_change('initalizing')
        self.name = "Uninherited Interface"
        self.interface_name = interface_name
        self._status = 'none'
        self._connected_to_network = False
        self._connected_to_something = False
        self.can_create_network_connection = False
        self.requires_network_connection = False
        self._use_tray_icon = False
    def _status_change(self, value):
        '''
        Sets the current interface status (used internally)
        Accepts:
        String containing status.
        Returns:
        Nothing
        '''
        self._status = value
        ps = self.previous_status
        self.previous_status = value
        self.status_change_callback(ps, value)
        for item in self.status_change_hooks:
            if item[0] == value:
                if not item[1]():
                    self.status_change_hooks.remove(item)
    def _state_change(self, value):
        self._state = value
        self._connected_to_network = self._connected_to_something = value
    def add_status_change_hook(self, to_value, method):
        """
        Adds a method to the list of methods to be executed when the interface
        state changes to to_value. If method returns True, it will be kept in
        the queue to be called, otherwise it will be removed.
        Accepts:
        Nothing
        Returns:
        Nothing
        """
        self.status_change_hooks.append((to_value, method))
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
    def get_connected_to_something(self):
        """
        Returns a boolean indicating if the interface is connected to something.
        Accepts:
        Nothing
        Returns:
        True if this interface is connected to something, otherwise False.
        """
        return self._connected_to_something
    def get_status(self):
        """
        Returns a string containing a human readable description
        of the current status.
        Accepts:
        Nothing
        Returns:
        String containing current status.
        """
        if self.get_connected_to_something():
            return "Connected"
        else:
            return "Disconnected"
    def get_internal_status(self):
        return self._status
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
    @needsidle
    def do_disconnect(self):
        ''' Disconnects from the current network. '''
        self._status_change('disconnecting')
        self._state_change(False)
        self.interface.disconnect()
        self._status_change('idle')
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
    def get_module_path(self):
        return os.path.abspath(inspect.getmodule(self).__file__)
