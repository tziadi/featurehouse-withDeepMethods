import wpath
import externalwirelessutils, configmanager
class WirelessNetworkProfile:
    def __init__(self, settings={}):
        if settings:
            for key, value in settings.iteritems():
                setattr(self, key, value)
class ProfiledWirelessInterface(externalwirelessutils.WirelessInterface):
    ''' Adds network profiles to the wireless interface. '''
    def __init__(self, interface_name):
        externalwirelessutils.WirelessInterface.__init__(self,
                                                         interface_name)
        self.config_manager = configmanager.ConfigManager(wpath.etc +
                                                          'wireless-%s-profiles.conf'
                                                          % interface_name)
    def scan(self):
        """ Updates the current wireless network list. """
        self.save_profiles()
        externalwirelessutils.WirelessInterface.scan(self)
        for network in self.networks:
            if self.config_manager.has_section(network.bssid):
                settings = self.config_manager.items(network.bssid)
                network.profile = WirelessNetworkProfile(dict(settings))
            else:
                network.profile = WirelessNetworkProfile()
    def save_profiles(self):
        """ Saves the profiles of all networks. """
        if not hasattr(self, 'networks'): return
        for network in self.networks:
            for item in dir(network.profile):
                if not item.startswith('_'):
                    self.config_manager.set_option(network.bssid,
                                                   item,
                                                   getattr(network.profile,
                                                           item)
                                                   )
        self.config_manager.write()
