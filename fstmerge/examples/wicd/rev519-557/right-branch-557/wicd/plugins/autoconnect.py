from baseplugin import BasePlugin
from misc import WicdError
from logfile import log
class AutoconnectPlugin(BasePlugin):
    ''' A plugin that will autoconnect to networks. '''
    PRIORITY = 100
    def do_start(self):
        log( 'autoconnect plugin started...')
    def do_got_link(self, interface):
        self._run_autoconnect('onlink', interface.interface_name)
    def do_autoconnect(self, interface_name=None):
        self._run_autoconnect('secondary', interface_name)
    def _run_autoconnect(self, value, interface_name):
        log( 'running _run_autoconnect...', value)
        if interface_name is None:
            for interface_name in self.daemon.ListInterfaces():
                self._autoconnect_interface(value, interface_name)
        else:
            self._autoconnect_interface(value, interface_name)
    def _autoconnect_interface(self, value, interface_name):
        interface = self.daemon.interface_manager.get(interface_name)
        log( 'autoconnecting', interface.interface_name,)
        if not interface.get_connected_to_something():
            if hasattr(interface, 'do_autoconnect'):
                try:
                    log( 'ok'                    )
                    getattr(interface, 'do_autoconnect')(value)                    
                except WicdError, e:
                    log( 'error autoconnecting interface %s: %s' % \
                          (interface_name, e))
        else:
            log( 'already connected')
