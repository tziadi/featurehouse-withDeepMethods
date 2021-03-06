import sys, os
import logging
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(
        os.path.realpath(__file__)
        ),
                 '../..')))
logging.debug(sys.path[0])
from gtkuibase import ShortInterfaceUiBase
sys.path.pop(0)
class WiredShortInterfaceUi(ShortInterfaceUiBase):
    def __init__(self, interface):
        ShortInterfaceUiBase.__init__(self, interface)
        self.image.set_from_icon_name('network-wired', 6)
