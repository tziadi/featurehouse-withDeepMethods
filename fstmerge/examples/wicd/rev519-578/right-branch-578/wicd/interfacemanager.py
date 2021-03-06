""" Interface manager for wicd.
Manages and loads the interfaces for wicd.
"""
from configmanager import ConfigManager
from backend import BackendManager
import wpath
import baseinterface
import logging
class InterfaceManager(object):
    def __init__(self, status_change_callback, state_change_callback):
        ''' Creates a new InterfaceManager object. '''
        self._interfaces = {}
        path = wpath.etc + "interfaces.conf"
        self.config_manager = ConfigManager(path)
        self.backend_manager = BackendManager()
        self.backend_manager.load_all_available_backends()
        self.status_change_callback = status_change_callback
        self.state_change_callback = state_change_callback
    def add(self, interface):
        ''' Adds interface to the dictionary of interfaces. '''
        self._interfaces[interface.interface_name] = interface
    def remove(self, interface_name):
        del self._interfaces[interface_name]
    def create(self, type, interface_name):
        ''' Creates the interface, if possible. If interface exists, returns. '''
        if not self.exists(interface_name):
            type_class = self.backend_manager.get_backend_by_type(type)
            def customized_status_callback(*args):
                return self.status_change_callback(interface_name, *args)
            def customized_state_callback(*args):
                return self.state_change_callback(interface_name, *args)
            new_interface = type_class(interface_name,
                                       (customized_status_callback,
                                        customized_state_callback))
            self.add(new_interface)
            logging.info( 'new interface: %s', new_interface.interface_name)
        else:
            logging.error('interface already exists: %s', interface_name)
    def delete(self, interface_name):
        if self.exists(interface_name):
            self.remove(interface_name)
    def get(self, interface_name):
        ''' Gets a single interface object. '''
        return self._interfaces.get(interface_name)
    def exists(self, interface_name):
        ''' Returns True if the specified interface exists, otherwise False. '''
        return bool(self._interfaces.get(interface_name))
    def load(self):
        """ Loads the saved interface configuration. """
        sections = self.config_manager.sections()
        for section in sections:
            interface_name = section
            type = self.config_manager.get_option(section, 'type')
            try:
                self.create(type, interface_name)
            except baseinterface.BaseInterface.CannotCreateInterfaceException:
                logging.error( 'error creating interface %s' % interface_name)
                logging.info( 'skipping interface %s' % interface_name)
            else:
                interface = self.get(interface_name)
                for k, v in self.config_manager.items(section):
                    setattr(interface, k, v)
    def save(self):
        """ Saves the current interface configuration. """
        self.config_manager.clear_all()
        for interface_name in self.get_all():
            interface = self.get(interface_name)
            interface.do_save()
            settings = interface.dump_settings_to_dictionary()
            for k, v in settings.iteritems():
                self.config_manager.set_option(interface_name, k, v)
        self.config_manager.write()
    def get_all(self):
        ''' Returns the interface dictionary. '''
        return self._interfaces
    def get_all_by_type(self, the_type):
        ''' Get all interfaces of the specified type. '''
        return [ interface
                 for name, interface in self.get_all().iteritems()
                 if interface.get_type() == the_type ]
    def get_all_names(self):
        ''' Returns the names of all the interfaces. '''
        interfaces = self.get_all()
        names = [ value.interface_name for key, value in interfaces.iteritems() ]
        return names
