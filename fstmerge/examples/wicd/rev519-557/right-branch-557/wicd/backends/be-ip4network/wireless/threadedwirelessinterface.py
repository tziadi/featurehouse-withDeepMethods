from misc import WicdError
from encryptablewirelessinterface import EncryptableWirelessInterface
from asyncrunner import AsyncManager, AsyncError
from logfile import log
class ThreadedWirelessInterface(EncryptableWirelessInterface):
    def __init__(self, interface_name):
        EncryptableWirelessInterface.__init__(self, interface_name)
        self.__async_manager = AsyncManager()
    def scan(self, finished_callback):
        ''' Performs a scan. Scanning is done asynchronously. '''
        def _do_scan(abort_if_needed, self):
            return EncryptableWirelessInterface.scan(self)
        def finish_up(result):
            log('scan finished', result)
            self.networks = result
            finished_callback()
        self.__async_manager.run(_do_scan, finish_up, self)
    def connect(self, finished_callback):
        ''' Attempts to connect. Connecting is done asynchronously.'''
        def _do_connect(abort_if_needed, interface, network):
            log('connecting to network', network.bssid)
            interface.reset()
            interface.up()
            interface.set_up_encryption(network)
            got_ip = interface.do_ip_address(network.profile)
	    log('%s: interface got IP: %s' % (interface.interface_name, got_ip))
        def _finish_up(result):
            finished_callback()
        self.__async_manager.run(_do_connect, _finish_up, self,
                                                     self.current_network,
                                                     name='connect')
    def cancel_connection_attempt(self):
        ''' Cancel the current attempt to connect to the network. '''
        self.dhcp_manager.stop()        
        self.__async_manager.stop('connect')
