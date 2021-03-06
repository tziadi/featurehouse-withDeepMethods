""" Wicd GUI module.
Module containg all the code (other than the tray icon) related to the 
Wicd user interface.
"""
import os
import sys
import time
import gobject
import dbus
import dbus.service
import pango
import gtk
import gtk.glade
import wicd.wpath as wpath
import wicd.misc as misc
if __name__ == '__main__':
    wpath.chdir(__file__)
try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
if getattr(dbus, 'version', (0, 0, 0)) < (0, 80, 0):
    import dbus.glib
else:
    from dbus.mainloop.glib import DBusGMainLoop
    DBusGMainLoop(set_as_default=True)
bus = dbus.SystemBus()
proxy_obj = daemon = wireless = wired = dbus_ifaces = config = None
_ = misc.get_gettext()
language = {}
language['connect'] = _("Connect")
language['ip'] = _("IP")
language['netmask'] = _("Netmask")
language['gateway'] = _('Gateway')
language['dns'] = _('DNS')
language['use_static_ip'] = _('Use Static IPs')
language['use_static_dns'] = _('Use Static DNS')
language['use_encryption'] = _('Use Encryption')
language['advanced_settings'] = _('Advanced Settings')
language['wired_network'] = _('Wired Network')
language['wired_network_instructions'] = _('To connect to a wired network, you'
' must create a network profile. To create a network profile, type a name that'
' describes this network, and press Add.')
language['automatic_connect'] = _('Automatically connect to this network')
language['secured'] = _('Secured')
language['unsecured'] = _('Unsecured')
language['channel'] = _('Channel')
language['preferences'] = _('Preferences')
language['wpa_supplicant_driver'] = _('WPA Supplicant Driver')
language['wireless_interface'] = _('Wireless Interface')
language['wired_interface'] = _('Wired Interface')
language['hidden_network'] = _('Hidden Network')
language['hidden_network_essid'] = _('Hidden Network ESSID')
language['connected_to_wireless'] = _('Connected to $A at $B (IP: $C)')
language['connected_to_wired'] = _('Connected to wired network (IP: $A)')
language['not_connected'] = _('Not connected')
language['no_wireless_networks_found'] = _('No wireless networks found.')
language['killswitch_enabled'] = _('Wireless Kill Switch Enabled')
language['key'] = _('Key')
language['username'] = _('Username')
language['password'] = _('Password')
language['anonymous_identity'] = _('Anonymous Identity')
language['identity'] = _('Identity')
language['authentication'] = _('Authentication')
language['path_to_pac_file'] = _('Path to PAC File')
language['select_a_network'] = _('Choose from the networks below:')
language['connecting'] = _('Connecting...')
language['wired_always_on'] = _('Always show wired interface')
language['auto_reconnect'] = _('Automatically reconnect on connection loss')
language['create_adhoc_network'] = _('Create an Ad-Hoc Network')
language['essid'] = _('ESSID')
language['use_wep_encryption'] = _('Use Encryption (WEP only)')
language['before_script'] = _('Run script before connect')
language['after_script'] = _('Run script after connect')
language['disconnect_script'] = _('Run disconnect script')
language['script_settings'] = _('Scripts')
language['use_ics'] = _('Activate Internet Connection Sharing')
language['madwifi_for_adhoc'] = _('Check if using madwifi/atheros drivers')
language['default_wired'] = _('Use as default profile (overwrites any previous default)')
language['use_debug_mode'] = _('Enable debug mode')
language['use_global_dns'] = _('Use global DNS servers')
language['use_default_profile'] = _('Use default profile on wired autoconnect')
language['show_wired_list'] = _('Prompt for profile on wired autoconnect')
language['use_last_used_profile'] = _('Use last used profile on wired autoconnect')
language['choose_wired_profile'] = _('Select or create a wired profile to connect with')
language['wired_network_found'] = _('Wired connection detected')
language['stop_showing_chooser'] = _('Stop Showing Autoconnect pop-up temporarily')
language['display_type_dialog'] = _('Use dBm to measure signal strength')
language['scripts'] = _('Scripts')
language['invalid_address'] = _('Invalid address in $A entry.')
language['global_settings'] = _('Use these settings for all networks sharing this essid')
language['encrypt_info_missing'] = _('Required encryption information is missing.')
language['enable_encryption'] = _('This network requires encryption to be enabled.')
language['wicd_auto_config'] = _('Automatic (recommended)')
language["gen_settings"] = _("General Settings")
language["ext_programs"] = _("External Programs")
language["dhcp_client"] = _("DHCP Client")
language["wired_detect"] = _("Wired Link Detection")
language["route_flush"] = _("Route Table Flushing")
language["no_global_dns"] = _("Global DNS is not enabled in preferences, so it can't be used for this network")
language['scripts_need_root'] = _('You must enter your password to configure scripts')
language['0'] = _('0')
language['1'] = _('1')
language['2'] = _('2')
language['3'] = _('3')
language['4'] = _('4')
language['5'] = _('5')
language['6'] = _('6')
language['7'] = _('7')
language['8'] = _('8')
language['9'] = _('9')
language['interface_down'] = _('Putting interface down...')
language['resetting_ip_address'] = _('Resetting IP address...')
language['interface_up'] = _('Putting interface up...')
language['setting_encryption_info'] = _('Setting encryption info')
language['removing_old_connection'] = _('Removing old connection...')
language['generating_psk'] = _('Generating PSK...')
language['generating_wpa_config'] = _('Generating WPA configuration file...')
language['flushing_routing_table'] = _('Flushing the routing table...')
language['configuring_interface'] = _('Configuring wireless interface...')
language['validating_authentication'] = _('Validating authentication...')
language['setting_broadcast_address'] = _('Setting broadcast address...')
language['setting_static_dns'] = _('Setting static DNS servers...')
language['setting_static_ip'] = _('Setting static IP addresses...')
language['running_dhcp'] = _('Obtaining IP address...')
language['dhcp_failed'] = _('Connection Failed: Unable to Get IP Address')
language['aborted'] = _('Connection Cancelled')
language['bad_pass'] = _('Connection Failed: Bad password')
language['done'] = _('Done connecting...')
def setup_dbus():
    global proxy_obj, daemon, wireless, wired, config, dbus_ifaces
    proxy_obj = bus.get_object("org.wicd.daemon", '/org/wicd/daemon')
    daemon = dbus.Interface(proxy_obj, 'org.wicd.daemon')
    wireless = dbus.Interface(proxy_obj, 'org.wicd.daemon.wireless')
    wired = dbus.Interface(proxy_obj, 'org.wicd.daemon.wired')
    config = dbus.Interface(proxy_obj, 'org.wicd.daemon.config')
    dbus_ifaces = {"daemon" : daemon, "wireless" : wireless, "wired" : wired, 
                   "config" : config}
class LinkButton(gtk.EventBox):
    label = None
    def __init__(self, txt):
        gtk.EventBox.__init__(self)
        self.connect("realize", self.__setHandCursor) 
        label = gtk.Label()
        label.set_markup("[ <span color=\"blue\">" + txt + "</span> ]")
        label.set_alignment(0,.5)
        label.show()
        self.add(label)
        self.show_all()
    def __setHandCursor(self, widget):
        hand = gtk.gdk.Cursor(gtk.gdk.HAND1)
        widget.window.set_cursor(hand)
class SmallLabel(gtk.Label):
    def __init__(self, text=''):
        gtk.Label.__init__(self, text)
        self.set_size_request(50, -1)
class LabelEntry(gtk.HBox):
    """ A label on the left with a textbox on the right and an optional checkbox for hiding the contents. """
    def __init__(self, text):
        gtk.HBox.__init__(self)
        self.show_contents_checkbox = gtk.CheckButton()
        self.show_contents_checkbox.set_active(True)
        self.show_contents_checkbox.set_no_show_all(True)
        self.entry = gtk.Entry()
        self.entry.set_size_request(200, -1)
        self.label = SmallLabel()
        self.label.set_text(text)
        self.label.set_size_request(170, -1)
        self.pack_start(self.label, fill=False, expand=False)
        self.pack_start(self.entry, fill=False, expand=False)
        self.pack_start(self.show_contents_checkbox,
                        fill=False, expand=False)
        self.label.show()
        self.entry.show()
        self.show_contents_checkbox.connect('toggled', self.toggle_visibility_checkbox)
        self.show()
        self.set_auto_hidden(False)
    def set_text(self, text):
        self.entry.set_text(text)
    def get_text(self):
        return self.entry.get_text()
    def set_auto_hidden(self, value):
        self.auto_hide_text = value
        if value:
            self.hide_characters()
            self.entry.set_visibility(False)
            self.show_contents_checkbox.set_active(False)
            self.show_contents_checkbox.show()
        else:
            self.show_characters()
            self.entry.set_visibility(True)
            self.show_contents_checkbox.set_active(True)
            self.show_contents_checkbox.hide()
    def toggle_visibility_checkbox(self, widget=None, event=None):
        if self.show_contents_checkbox.get_active():
            self.show_characters()
        else:
            self.hide_characters()
    def show_characters(self, widget=None, event=None):
        if self.auto_hide_text:
            self.entry.set_visibility(True)
    def hide_characters(self, widget=None, event=None):
        if self.auto_hide_text:
            self.entry.set_visibility(False)
    def set_sensitive(self, value):
        gtk.HBox.set_sensitive(self, value)
        self.entry.set_sensitive(value)
        self.label.set_sensitive(value)
class GreyLabel(gtk.Label):
    """ Creates a grey gtk.Label. """
    def __init__(self):
        gtk.Label.__init__(self)
    def set_label(self, text):
        self.set_markup("<span color=\"#666666\"><i>" + text + "</i></span>")
        self.set_alignment(0, 0)
def noneToString(text):
    """ Converts a blank string to "None". """
    if text == "":
        return "None"
    else:
        return str(text)
def noneToBlankString(text):
    """ Converts NoneType or "None" to a blank string. """
    if text in (None, "None"):
        return ""
    else:
        return str(text)
def stringToNone(text):
    """ Performs opposite function of noneToString. """
    if text in ("", None, "None"):
        return None
    else:
        return str(text)
def stringToBoolean(text):
    """ Turns a string representation of a bool to a boolean if needed. """
    if text in ("True", "1"):
        return True
    if text in ("False", "0"):
        return False
    return text
def checkboxTextboxToggle(checkbox, textboxes):
    for textbox in textboxes:
        textbox.set_sensitive(checkbox.get_active())
def error(parent, message): 
    """ Shows an error dialog """
    dialog = gtk.MessageDialog(parent, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR,
                               gtk.BUTTONS_OK)
    dialog.set_markup(message)
    dialog.run()
    dialog.destroy()
class AdvancedSettingsDialog(gtk.Dialog):
    def __init__(self):
        """ Build the base advanced settings dialog.
        This class isn't used by itself, instead it is used as a parent for
        the WiredSettingsDialog and WirelessSettingsDialog.
        """
        gtk.Dialog.__init__(self, title=language['advanced_settings'],
                            flags=gtk.DIALOG_MODAL, buttons=(gtk.STOCK_CANCEL,
                                                             gtk.RESPONSE_REJECT,
                                                             gtk.STOCK_OK,
                                                             gtk.RESPONSE_ACCEPT))
        self.txt_ip = LabelEntry(language['ip'])
        self.txt_ip.entry.connect('focus-out-event', self.set_defaults)
        self.txt_netmask = LabelEntry(language['netmask'])
        self.txt_gateway = LabelEntry(language['gateway'])
        self.txt_dns_1 = LabelEntry(language['dns'] + ' ' + language['1'])
        self.txt_dns_2 = LabelEntry(language['dns'] + ' ' + language['2'])
        self.txt_dns_3 = LabelEntry(language['dns'] + ' ' + language['3'])
        self.chkbox_static_ip = gtk.CheckButton(language['use_static_ip'])
        self.chkbox_static_dns = gtk.CheckButton(language['use_static_dns'])
        self.chkbox_global_dns = gtk.CheckButton(language['use_global_dns'])
        self.hbox_dns = gtk.HBox(False, 0)
        self.hbox_dns.pack_start(self.chkbox_static_dns)
        self.hbox_dns.pack_start(self.chkbox_global_dns)
        self.vbox.pack_start(self.chkbox_static_ip, fill=False, expand=False)
        self.vbox.pack_start(self.txt_ip, fill=False, expand=False)
        self.vbox.pack_start(self.txt_netmask, fill=False, expand=False)
        self.vbox.pack_start(self.txt_gateway, fill=False, expand=False)
        self.vbox.pack_start(self.hbox_dns, fill=False, expand=False)
        self.vbox.pack_start(self.txt_dns_1, fill=False, expand=False)
        self.vbox.pack_start(self.txt_dns_2, fill=False, expand=False)
        self.vbox.pack_start(self.txt_dns_3, fill=False, expand=False)
        self.chkbox_static_ip.connect("toggled", self.toggle_ip_checkbox)
        self.chkbox_static_dns.connect("toggled", self.toggle_dns_checkbox)
        self.chkbox_global_dns.connect("toggled", self.toggle_global_dns_checkbox)
        self.chkbox_static_ip.set_active(False)
        self.chkbox_static_dns.set_active(False)
    def set_defaults(self, widget=None, event=None):
        """ Put some default values into entries to help the user out. """
        ipAddress = self.txt_ip.get_text()  
        netmask = self.txt_netmask
        gateway = self.txt_gateway
        ip_parts = misc.IsValidIP(ipAddress)
        if ip_parts:
            if stringToNone(gateway.get_text()) is None:  
                gateway.set_text('.'.join(ip_parts[0:3]) + '.1')
            if stringToNone(netmask.get_text()) is None:  
                netmask.set_text('255.255.255.0')  
        elif ipAddress != "":
            error(None, "Invalid IP Address Entered.")
    def reset_static_checkboxes(self):
        if stringToNone(self.txt_ip.get_text()):
            self.chkbox_static_ip.set_active(True)
            self.chkbox_static_dns.set_active(True)
            self.chkbox_static_dns.set_sensitive(False)
        else:
            self.chkbox_static_ip.set_active(False)
            self.chkbox_static_dns.set_sensitive(True)
        if stringToNone(self.txt_dns_1.get_text()) or \
           self.chkbox_global_dns.get_active():
            self.chkbox_static_dns.set_active(True)
        else:
            self.chkbox_static_dns.set_active(False)
        self.toggle_ip_checkbox()
        self.toggle_dns_checkbox()
        self.toggle_global_dns_checkbox()
    def toggle_ip_checkbox(self, widget=None):
        """Toggle entries/checkboxes based on the static IP checkbox. """
        if self.chkbox_static_ip.get_active():
            self.chkbox_static_dns.set_active(True)
            self.chkbox_static_dns.set_sensitive(False)
        else:
            self.chkbox_static_dns.set_sensitive(True)
        self.txt_ip.set_sensitive(self.chkbox_static_ip.get_active())
        self.txt_netmask.set_sensitive(self.chkbox_static_ip.get_active())
        self.txt_gateway.set_sensitive(self.chkbox_static_ip.get_active())
    def toggle_dns_checkbox(self, widget=None):
        """ Toggle entries and checkboxes based on the static dns checkbox. """
        if self.chkbox_static_ip.get_active():
            self.chkbox_static_dns.set_active(True)
            self.chkbox_static_dns.set_sensitive(False)
        self.chkbox_global_dns.set_sensitive(self.chkbox_static_dns.
                                             get_active())
        if self.chkbox_static_dns.get_active():
            self.txt_dns_1.set_sensitive(not self.chkbox_global_dns.get_active())
            self.txt_dns_2.set_sensitive(not self.chkbox_global_dns.get_active())
            self.txt_dns_3.set_sensitive(not self.chkbox_global_dns.get_active())
        else:
            self.txt_dns_1.set_sensitive(False)
            self.txt_dns_2.set_sensitive(False)
            self.txt_dns_3.set_sensitive(False)
            self.chkbox_global_dns.set_active(False)
    def toggle_global_dns_checkbox(self, widget=None):
        """ Set the DNS entries' sensitivity based on the Global checkbox. """
        if daemon.GetUseGlobalDNS() and self.chkbox_static_dns.get_active():
            self.txt_dns_1.set_sensitive(not self.chkbox_global_dns.get_active())
            self.txt_dns_2.set_sensitive(not self.chkbox_global_dns.get_active())
            self.txt_dns_3.set_sensitive(not self.chkbox_global_dns.get_active())
        elif self.chkbox_global_dns.get_active():
            self.chkbox_global_dns.set_active(False)
            error(None, language['no_global_dns'])
    def destroy_called(self):
        """ Clean up everything. """
        super(AdvancedSettingsDialog, self).destroy()
        self.destroy()
        del self
class WiredSettingsDialog(AdvancedSettingsDialog):
    def __init__(self, name):
        """ Build the wired settings dialog. """
        AdvancedSettingsDialog.__init__(self)
        self.des = self.connect("destroy", self.destroy_called)
        self.prof_name = name
    def set_net_prop(self, option, value):
        """ Sets the given option to the given value for this network. """
        wired.SetWiredProperty(option, value)
    def set_values(self):
        """ Fill in the Gtk.Entry objects with the correct values. """
        self.txt_ip.set_text(self.format_entry("ip"))
        self.txt_netmask.set_text(self.format_entry("netmask"))
        self.txt_gateway.set_text(self.format_entry("gateway"))
        self.txt_dns_1.set_text(self.format_entry("dns1"))
        self.txt_dns_2.set_text(self.format_entry("dns2"))
        self.txt_dns_3.set_text(self.format_entry("dns3"))
        self.chkbox_global_dns.set_active(bool(wired.GetWiredProperty("use_global_dns")))
        self.reset_static_checkboxes()
        if bool(wired.GetWiredProperty('use_global_dns')):
            self.chkbox_global_dns.set_active(True)
            self.chkbox_static_dns.set_active(True)
        self.toggle_dns_checkbox()
        self.toggle_ip_checkbox()
    def format_entry(self, label):
        """ Helper method to fetch and format wired properties. """
        return noneToBlankString(wired.GetWiredProperty(label))
    def destroy_called(self):
        """ Clean up everything. """
        self.disconnect(self.des)
        super(WiredSettingsDialog, self).destroy_called()
        self.destroy()
        del self
class WirelessSettingsDialog(AdvancedSettingsDialog):
    def __init__(self, networkID):
        """ Build the wireless settings dialog. """
        AdvancedSettingsDialog.__init__(self)
        self.networkID = networkID
        self.combo_encryption = gtk.combo_box_new_text()
        self.chkbox_encryption = gtk.CheckButton(language['use_encryption'])
        self.chkbox_global_settings = gtk.CheckButton(language['global_settings'])
        self.vbox_encrypt_info = gtk.VBox(False, 0)        
        self.toggle_encryption()
        self.chkbox_encryption.set_active(False)
        self.combo_encryption.set_sensitive(False)
        self.encrypt_types = misc.LoadEncryptionMethods()
        activeID = -1  
        for x, enc_type in enumerate(self.encrypt_types):
            self.combo_encryption.append_text(enc_type[0])
            if enc_type[1] == wireless.GetWirelessProperty(networkID,
                                                           "enctype"):
                activeID = x
        self.combo_encryption.set_active(activeID)
        if activeID != -1:
            self.chkbox_encryption.set_active(True)
            self.combo_encryption.set_sensitive(True)
            self.vbox_encrypt_info.set_sensitive(True)
        else:
            self.combo_encryption.set_active(0)
        self.change_encrypt_method()
        self.vbox.pack_start(self.chkbox_global_settings, False, False)
        self.vbox.pack_start(self.chkbox_encryption, False, False)
        self.vbox.pack_start(self.combo_encryption, False, False)
        self.vbox.pack_start(self.vbox_encrypt_info, False, False)
        self.chkbox_encryption.connect("toggled", self.toggle_encryption)
        self.combo_encryption.connect("changed", self.change_encrypt_method)
        self.des = self.connect("destroy", self.destroy_called)
    def destroy_called(self):
        """ Clean up everything. """
        self.disconnect(self.des)
        super(WirelessSettingsDialog, self).destroy_called()
        self.destroy()
        del self
    def set_net_prop(self, option, value):
        """ Sets the given option to the given value for this network. """
        wireless.SetWirelessProperty(self.networkID, option, value)
    def set_values(self):
        """ Set the various network settings to the right values. """
        networkID = self.networkID
        self.txt_ip.set_text(self.format_entry(networkID,"ip"))
        self.txt_netmask.set_text(self.format_entry(networkID,"netmask"))
        self.txt_gateway.set_text(self.format_entry(networkID,"gateway"))
        self.txt_dns_1.set_text(self.format_entry(networkID, "dns1"))
        self.txt_dns_2.set_text(self.format_entry(networkID, "dns2"))
        self.txt_dns_3.set_text(self.format_entry(networkID, "dns3"))
        self.reset_static_checkboxes()
        self.chkbox_encryption.set_active(bool(wireless.GetWirelessProperty(networkID,
                                                                            'encryption')))
        self.chkbox_global_settings.set_active(bool(wireless.GetWirelessProperty(networkID,
                                                                                 'use_settings_globally')))
        activeID = -1  
        user_enctype = wireless.GetWirelessProperty(networkID, "enctype")
        for x, enc_type in enumerate(self.encrypt_types):
            if enc_type[1] == user_enctype:
                activeID = x
        self.combo_encryption.set_active(activeID)
        if activeID != -1:
            self.chkbox_encryption.set_active(True)
            self.combo_encryption.set_sensitive(True)
            self.vbox_encrypt_info.set_sensitive(True)
        else:
            self.combo_encryption.set_active(0)
        self.change_encrypt_method()
        if bool(wireless.GetWirelessProperty(networkID, 'use_global_dns')):
            self.chkbox_global_dns.set_active(True)
            self.chkbox_static_dns.set_active(True)
        self.toggle_encryption()
        self.toggle_dns_checkbox()
        self.toggle_ip_checkbox()
    def format_entry(self, networkid, label):
        """ Helper method for fetching/formatting wireless properties. """
        return noneToBlankString(wireless.GetWirelessProperty(networkid, label))
    def toggle_encryption(self, widget=None):
        """ Toggle the encryption combobox based on the encryption checkbox. """
        active = self.chkbox_encryption.get_active()
        self.vbox_encrypt_info.set_sensitive(active)
        self.combo_encryption.set_sensitive(active)
    def change_encrypt_method(self, widget=None):
        """ Load all the entries for a given encryption method. """
        for z in self.vbox_encrypt_info:
            z.destroy()  
        ID = self.combo_encryption.get_active()
        methods = misc.LoadEncryptionMethods()
        self.encryption_info = {}
        if ID == -1:
            self.combo_encryption.set_active(0)
            ID = 0
        opts = methods[ID][2]
        for x in opts:
            box = None
            if language.has_key(opts[x][0]):
                box = LabelEntry(language[opts[x][0].lower().replace(' ','_')])
            else:
                box = LabelEntry(opts[x][0].replace('_',' '))
            box.set_auto_hidden(True)
            self.vbox_encrypt_info.pack_start(box)
            self.encryption_info[opts[x][1]] = box.entry
            box.entry.set_text(noneToBlankString(
                wireless.GetWirelessProperty(self.networkID, opts[x][1])))
        self.vbox_encrypt_info.show_all() 
class NetworkEntry(gtk.HBox):
    def __init__(self):
        """ Base network entry class.
        Provides gtk objects used by both the WiredNetworkEntry and
        WirelessNetworkEntry classes.
        """
        gtk.HBox.__init__(self, False, 2)
        self.expander = gtk.Expander()
        self.image = gtk.Image()
        self.pack_start(self.image, False, False)
        self.connect_button = gtk.Button(stock=gtk.STOCK_CONNECT)
        self.connect_hbox = gtk.HBox(False, 2)
        self.connect_hbox.pack_start(self.connect_button, False, False)
        self.connect_hbox.show()
        self.disconnect_button = gtk.Button(stock=gtk.STOCK_DISCONNECT)
        self.connect_hbox.pack_start(self.disconnect_button, False, False)
        self.expander_vbox = gtk.VBox(False, 1)
        self.expander_vbox.show()
        self.expander_vbox.pack_start(self.expander)
        self.expander_vbox.pack_start(self.connect_hbox, False, False)
        self.pack_end(self.expander_vbox)
        self.advanced_button = gtk.Button()
        self.advanced_image = gtk.Image()
        self.advanced_image.set_from_stock(gtk.STOCK_EDIT, 4)
        self.advanced_image.set_padding(4, 0)
        self.advanced_button.set_alignment(.5, .5)
        self.advanced_button.set_label(language['advanced_settings'])
        self.advanced_button.set_image(self.advanced_image)
        self.script_button = gtk.Button()
        self.script_image = gtk.Image()
        self.script_image.set_from_stock(gtk.STOCK_EXECUTE, 4)
        self.script_image.set_padding(4, 0)
        self.script_button.set_alignment(.5, .5)
        self.script_button.set_image(self.script_image)
        self.script_button.set_label(language['scripts'])
        self.settings_hbox = gtk.HBox(False, 3)
        self.settings_hbox.set_border_width(5)
        self.settings_hbox.pack_start(self.script_button, False, False)
        self.settings_hbox.pack_start(self.advanced_button, False, False)
        self.vbox_top = gtk.VBox(False, 0)
        self.vbox_top.pack_end(self.settings_hbox, False, False)
        aligner = gtk.Alignment(xscale=1.0)
        aligner.add(self.vbox_top)
        aligner.set_padding(0, 0, 15, 0)
        self.expander.add(aligner)
    def destroy_called(self, *args):
        """ Clean up everything. """
        super(NetworkEntry, self).destroy()
        self.destroy()
        del self
class WiredNetworkEntry(NetworkEntry):
    def __init__(self):
        """ Load the wired network entry. """
        NetworkEntry.__init__(self)
        self.image.set_alignment(.5, 0)
        self.image.set_size_request(60, -1)
        self.image.set_from_file(wpath.images + 'wired.png')
        self.image.show()
        self.expander.show()
        self.connect_button.show()
        self.expander.set_label(language['wired_network'])
        self.is_full_gui = True
        self.button_add = gtk.Button(stock=gtk.STOCK_ADD)
        self.button_delete = gtk.Button(stock=gtk.STOCK_DELETE)
        self.profile_help = gtk.Label(language['wired_network_instructions'])
        self.chkbox_default_profile = gtk.CheckButton(language['default_wired'])
        self.combo_profile_names = gtk.combo_box_entry_new_text()
        self.profile_list = config.GetWiredProfileList()
        if self.profile_list:
            for x in self.profile_list:
                self.combo_profile_names.append_text(x)
        self.profile_help.set_justify(gtk.JUSTIFY_LEFT)
        self.profile_help.set_line_wrap(True)
        self.hbox_temp = gtk.HBox(False, 0)
        self.hbox_def = gtk.HBox(False, 0)
        self.vbox_top.pack_start(self.profile_help, True, True)
        self.vbox_top.pack_start(self.hbox_def)
        self.vbox_top.pack_start(self.hbox_temp)
        self.hbox_temp.pack_start(self.combo_profile_names, True, True)
        self.hbox_temp.pack_start(self.button_add, False, False)
        self.hbox_temp.pack_start(self.button_delete, False, False)
        self.hbox_def.pack_start(self.chkbox_default_profile, False, False)
        self.button_add.connect("clicked", self.add_profile)
        self.button_delete.connect("clicked", self.remove_profile)
        self.chkbox_default_profile.connect("toggled",
                                            self.toggle_default_profile)
        self.combo_profile_names.connect("changed", self.change_profile)
        self.script_button.connect("button-press-event", self.edit_scripts)
        if stringToBoolean(wired.GetWiredProperty("default")):
            self.chkbox_default_profile.set_active(True)
        else:
            self.chkbox_default_profile.set_active(False)
        self.show_all()
        self.profile_help.hide()
        self.advanced_dialog = WiredSettingsDialog(self.combo_profile_names.get_active_text())
        if self.profile_list is not None:
            prof = config.GetDefaultWiredNetwork()
            if prof != None:  
                i = 0
                while self.combo_profile_names.get_active_text() != prof:
                    self.combo_profile_names.set_active(i)
                    i += 1
            else:
                self.combo_profile_names.set_active(0)
            print "wired profiles found"
            self.expander.set_expanded(False)
        else:
            print "no wired profiles found"
            if not wired.GetAlwaysShowWiredInterface():
                self.expander.set_expanded(True)
            self.profile_help.show()        
        self.check_enable()
        self.wireddis = self.connect("destroy", self.destroy_called)
    def destroy_called(self, *args):
        """ Clean up everything. """
        self.disconnect(self.wireddis)
        self.advanced_dialog.destroy_called()
        del self.advanced_dialog
        super(WiredNetworkEntry, self).destroy_called()
        self.destroy()
        del self
    def edit_scripts(self, widget=None, event=None):
        """ Launch the script editting dialog. """
        profile = self.combo_profile_names.get_active_text()
        try:
            sudo_prog = misc.choose_sudo_prog()
            msg = "'%s.'" % language['scripts_need_root']
            if sudo_prog.endswith("gksudo") or sudo_prog.endswith("ktsuss"):
                msg_flag = "--message"
            else:
                msg_flag = "--caption"
            misc.LaunchAndWait(' '.join([sudo_prog, msg_flag, msg, 
                                         os.path.join(wpath.lib, "configscript.py"),
                                         profile, "wired"]))
        except misc.WicdError:
            error("Could not find a graphical sudo program." + \
                  "  Script editor could not be launched.")
    def check_enable(self):
        """ Disable objects if the profile list is empty. """
        profile_list = config.GetWiredProfileList()
        if profile_list == None:
            self.button_delete.set_sensitive(False)
            self.connect_button.set_sensitive(False)
            self.advanced_button.set_sensitive(False)
            self.script_button.set_sensitive(False)
    def update_connect_button(self, state, apbssid=None):
        """ Update the connection/disconnect button for this entry. """
        if state == misc.WIRED:
            self.disconnect_button.show()
            self.connect_button.hide()
        else:
            self.disconnect_button.hide()
            self.connect_button.show()
    def add_profile(self, widget):
        """ Add a profile to the profile list. """
        print "adding profile"
        profile_name = self.combo_profile_names.get_active_text()
        profile_list = config.GetWiredProfileList()
        if profile_list:
            if profile_name in profile_list:
                return False
        if profile_name != "":
            self.profile_help.hide()
            config.CreateWiredNetworkProfile(profile_name, False)
            self.combo_profile_names.prepend_text(profile_name)
            self.combo_profile_names.set_active(0)
            self.advanced_dialog.prof_name = profile_name
            if self.is_full_gui:
                self.button_delete.set_sensitive(True)
                self.connect_button.set_sensitive(True)
                self.advanced_button.set_sensitive(True)
                self.script_button.set_sensitive(True)
    def remove_profile(self, widget):
        """ Remove a profile from the profile list. """
        print "removing profile"
        profile_name = self.combo_profile_names.get_active_text()
        config.DeleteWiredNetworkProfile(profile_name)
        self.combo_profile_names.remove_text(self.combo_profile_names.
                                             get_active())
        self.combo_profile_names.set_active(0)
        self.advanced_dialog.prof_name = self.combo_profile_names.get_active_text()
        if not config.GetWiredProfileList():
            self.profile_help.show()
            entry = self.combo_profile_names.child
            entry.set_text("")
            if self.is_full_gui:
                self.button_delete.set_sensitive(False)
                self.advanced_button.set_sensitive(False)
                self.script_button.set_sensitive(False)
                self.connect_button.set_sensitive(False)
        else:
            self.profile_help.hide()
    def toggle_default_profile(self, widget):
        """ Change the default profile. """
        if self.chkbox_default_profile.get_active():
            config.UnsetWiredDefault()
        wired.SetWiredProperty("default",
                               self.chkbox_default_profile.get_active())
        config.SaveWiredNetworkProfile(self.combo_profile_names.get_active_text())
    def change_profile(self, widget):
        """ Called when a new profile is chosen from the list. """
        if self.combo_profile_names.get_active() > -1:
            if not self.is_full_gui:
                return
            profile_name = self.combo_profile_names.get_active_text()
            config.ReadWiredNetworkProfile(profile_name)
            self.advanced_dialog.txt_ip.set_text(self.format_entry("ip"))
            self.advanced_dialog.txt_netmask.set_text(self.format_entry("netmask"))
            self.advanced_dialog.txt_gateway.set_text(self.format_entry("gateway"))
            self.advanced_dialog.txt_dns_1.set_text(self.format_entry("dns1"))
            self.advanced_dialog.txt_dns_2.set_text(self.format_entry("dns2"))
            self.advanced_dialog.txt_dns_3.set_text(self.format_entry("dns3"))
            self.advanced_dialog.prof_name = profile_name
            is_default = wired.GetWiredProperty("default")
            self.chkbox_default_profile.set_active(stringToBoolean(is_default))
    def format_entry(self, label):
        """ Help method for fetching/formatting wired properties. """
        return noneToBlankString(wired.GetWiredProperty(label))
class WirelessNetworkEntry(NetworkEntry):
    def __init__(self, networkID, iwconfig=""):
        """ Build the wireless network entry. """
        NetworkEntry.__init__(self)
        self.networkID = networkID
        self.image.set_padding(0, 0)
        self.image.set_alignment(.5, 0)
        self.image.set_size_request(60, -1)
        self.image.set_from_icon_name("network-wired", 6)
        self.essid = noneToBlankString(wireless.GetWirelessProperty(networkID, 
                                                                    "essid"))
        self.lbl_strength = GreyLabel()
        self.lbl_encryption = GreyLabel()
        self.lbl_mac = GreyLabel()
        self.lbl_channel = GreyLabel()
        self.lbl_mode = GreyLabel()
        self.hbox_status = gtk.HBox(False, 5)
        self.chkbox_autoconnect = gtk.CheckButton(language['automatic_connect'])
        self.set_signal_strength(wireless.GetWirelessProperty(networkID, 
                                                              'quality'),
                                 wireless.GetWirelessProperty(networkID, 
                                                              'strength'))
        self.set_mac_address(wireless.GetWirelessProperty(networkID, 'bssid'))
        self.set_mode(wireless.GetWirelessProperty(networkID, 'mode'))
        self.set_channel(wireless.GetWirelessProperty(networkID, 'channel'))
        self.set_encryption(wireless.GetWirelessProperty(networkID,
                                                         'encryption'),
                            wireless.GetWirelessProperty(networkID, 
                                                         'encryption_method'))
        self.expander.set_use_markup(True)
        self.expander.set_label(self._escape(self.essid) + "   " + 
                                self.lbl_strength.get_label() + "   " +
                                self.lbl_encryption.get_label() + "   " +
                                self.lbl_mac.get_label())
        self.hbox_status.pack_start(self.lbl_strength, True, True)
        self.hbox_status.pack_start(self.lbl_encryption, True, True)
        self.hbox_status.pack_start(self.lbl_mac, True, True)
        self.hbox_status.pack_start(self.lbl_mode, True, True)
        self.hbox_status.pack_start(self.lbl_channel, True, True)
        self.vbox_top.pack_start(self.chkbox_autoconnect, False, False)
        self.vbox_top.pack_start(self.hbox_status, True, True)
        if stringToBoolean(self.format_entry(networkID, "automatic")):
            self.chkbox_autoconnect.set_active(True)
        else:
            self.chkbox_autoconnect.set_active(False)
        self.chkbox_autoconnect.connect("toggled", self.update_autoconnect)
        self.script_button.connect("button-press-event", self.edit_scripts)       
        self.show_all()
        self.advanced_dialog = WirelessSettingsDialog(networkID)
        self.wifides = self.connect("destroy", self.destroy_called)
    def _escape(self, val):
        return val.replace("&", "&amp;").replace("<", "&lt;").\
               replace(">","&gt;").replace("'", "&apos;").replace('"', "&quot;")
    def destroy_called(self, *args):
        """ Clean up everything. """
        self.disconnect(self.wifides)
        self.advanced_dialog.destroy_called()
        del self.advanced_dialog
        super(WirelessNetworkEntry, self).destroy_called()
        self.destroy()
        del self
    def set_signal_strength(self, strength, dbm_strength):
        """ Set the signal strength displayed in the WirelessNetworkEntry. """
        if strength is not None:
            strength = int(strength)
        else:
            strength = -1
        if dbm_strength is not None:
            dbm_strength = int(dbm_strength)
        else:
            dbm_strength = -100
        display_type = daemon.GetSignalDisplayType()
        if daemon.GetWPADriver() == 'ralink legacy' or display_type == 1:
            if dbm_strength >= -60:
                signal_img = 'signal-100.png'
            elif dbm_strength >= -70:
                signal_img = 'signal-75.png'
            elif dbm_strength >= -80:
                signal_img = 'signal-50.png'
            else:
                signal_img = 'signal-25.png'
            ending = "dBm"
            disp_strength = str(dbm_strength)
        else:
            if strength > 75:
                signal_img = 'signal-100.png'
            elif strength > 50:
                signal_img = 'signal-75.png'
            elif strength > 25:
                signal_img = 'signal-50.png'
            else:
                signal_img = 'signal-25.png'
            ending = "%"
            disp_strength = str(strength)
        self.image.set_from_file(wpath.images + signal_img)
        self.lbl_strength.set_label(disp_strength + ending)
    def update_connect_button(self, state, apbssid):
        """ Update the connection/disconnect button for this entry. """
        if not apbssid:
            apbssid = wireless.GetApBssid()
        if state == misc.WIRELESS and \
           apbssid == wireless.GetWirelessProperty(self.networkID, "bssid"):
            self.disconnect_button.show()
            self.connect_button.hide()
        else:
            self.disconnect_button.hide()
            self.connect_button.show()
    def set_mac_address(self, address):
        """ Set the MAC address for the WirelessNetworkEntry. """
        self.lbl_mac.set_label(str(address))
    def set_encryption(self, on, ttype):
        """ Set the encryption value for the WirelessNetworkEntry. """
        if on and ttype:
            self.lbl_encryption.set_label(str(ttype))
        if on and not ttype: 
            self.lbl_encryption.set_label(language['secured'])
        if not on:
            self.lbl_encryption.set_label(language['unsecured'])
    def set_channel(self, channel):
        """ Set the channel value for the WirelessNetworkEntry. """
        self.lbl_channel.set_label(language['channel'] + ' ' + str(channel))
    def set_mode(self, mode):
        """ Set the mode value for the WirelessNetworkEntry. """
        self.lbl_mode.set_label(str(mode))
    def format_entry(self, networkid, label):
        """ Helper method for fetching/formatting wireless properties. """
        return noneToBlankString(wireless.GetWirelessProperty(networkid, label))
    def edit_scripts(self, widget=None, event=None):
        """ Launch the script editting dialog. """
        try:
            sudo_prog = misc.choose_sudo_prog()
            msg = "'%s.'" % language['scripts_need_root']
            if sudo_prog.endswith("gksudo") or sudo_prog.endswith("ktsuss"):
                msg_flag = "-m"
            else:
                msg_flag = "--caption"
            misc.LaunchAndWait(' '.join([sudo_prog, msg_flag, msg, 
                                         os.path.join(wpath.lib, "configscript.py"), 
                                         str(self.networkID), "wireless"]))
        except misc.WicdError:
            error(None, "Could not find a graphical sudo program." + \
                  "  Script editor could no be launched.")
    def update_autoconnect(self, widget=None):
        """ Called when the autoconnect checkbox is toggled. """
        wireless.SetWirelessProperty(self.networkID, "automatic",
                                     noneToString(self.chkbox_autoconnect.
                                                  get_active()))
        config.SaveWirelessNetworkProperty(self.networkID, "automatic")
class WiredProfileChooser:
    """ Class for displaying the wired profile chooser. """
    def __init__(self):
        """ Initializes and runs the wired profile chooser. """
        wired_net_entry = WiredNetworkEntry()
        dialog = gtk.Dialog(title = language['wired_network_found'],
                            flags = gtk.DIALOG_MODAL,
                            buttons = (gtk.STOCK_CONNECT, 1,
                                       gtk.STOCK_CANCEL, 2))
        dialog.set_has_separator(False)
        dialog.set_size_request(400, 150)
        instruct_label = gtk.Label(language['choose_wired_profile'] + ':\n')
        stoppopcheckbox = gtk.CheckButton(language['stop_showing_chooser'])
        wired_net_entry.is_full_gui = False
        instruct_label.set_alignment(0, 0)
        stoppopcheckbox.set_active(False)
        wired_net_entry.vbox_top.remove(wired_net_entry.hbox_temp)
        wired_net_entry.vbox_top.remove(wired_net_entry.profile_help)
        dialog.vbox.pack_start(instruct_label, fill=False, expand=False)
        dialog.vbox.pack_start(wired_net_entry.profile_help, False, False)
        dialog.vbox.pack_start(wired_net_entry.hbox_temp, False, False)
        dialog.vbox.pack_start(stoppopcheckbox, False, False)
        dialog.show_all()
        wired_profiles = wired_net_entry.combo_profile_names
        wired_net_entry.profile_help.hide()
        if wired_net_entry.profile_list != None:
            wired_profiles.set_active(0)
            print "wired profiles found"
        else:
            print "no wired profiles found"
            wired_net_entry.profile_help.show()
        response = dialog.run()
        if response == 1:
            print 'reading profile ', wired_profiles.get_active_text()
            config.ReadWiredNetworkProfile(wired_profiles.get_active_text())
            wired.ConnectWired()
        else:
            if stoppopcheckbox.get_active():
                daemon.SetForcedDisconnect(True)
        dialog.destroy()
class appGui:
    """ The main wicd GUI class. """
    def __init__(self, standalone=False):
        """ Initializes everything needed for the GUI. """
        gladefile = wpath.share + "wicd.glade"
        self.windowname = "gtkbench"
        self.wTree = gtk.glade.XML(gladefile)
        dic = { "refresh_clicked" : self.refresh_networks, 
                "quit_clicked" : self.exit, 
                "disconnect_clicked" : self.disconnect_all,
                "main_exit" : self.exit, 
                "cancel_clicked" : self.cancel_connect,
                "connect_clicked" : self.connect_hidden,
                "preferences_clicked" : self.settings_dialog,
                "about_clicked" : self.about_dialog,
                "create_adhoc_network_button_button" : self.create_adhoc_network}
        self.wTree.signal_autoconnect(dic)
        label_instruct = self.wTree.get_widget("label_instructions")
        label_instruct.set_label(language['select_a_network'])
        probar = self.wTree.get_widget("progressbar")
        probar.set_text(language['connecting'])
        self.window = self.wTree.get_widget("window1")
        self.network_list = self.wTree.get_widget("network_list_vbox")
        self.status_area = self.wTree.get_widget("connecting_hbox")
        self.status_bar = self.wTree.get_widget("statusbar")
        self.status_area.hide_all()
        if os.path.exists(wpath.images + "wicd-client.png"):
            self.window.set_icon_from_file(wpath.images + "wicd-client.png")
        self.statusID = None
        self.first_dialog_load = True
        self.vpn_connection_pipe = None
        self.is_visible = True
        self.pulse_active = False
        self.standalone = standalone
        self.wpadrivercombo = None
        self.connecting = False
        self.prev_state = False
        self.refresh_networks(fresh=False)
        self.window.connect('delete_event', self.exit)
        self.window.connect('key-release-event', self.key_event)
        size = config.ReadWindowSize("main")
        width = size[0]
        height = size[1]
        if width > -1 and height > -1:
            self.window.resize(int(width), int(height))
        try:
            gobject.timeout_add_seconds(1, self.update_statusbar)
        except:
            gobject.timeout_add(1000, self.update_statusbar)
    def create_adhoc_network(self, widget=None):
        """ Shows a dialog that creates a new adhoc network. """
        print "Starting the Ad-Hoc Network Creation Process..."
        dialog = gtk.Dialog(title = language['create_adhoc_network'],
                            flags = gtk.DIALOG_MODAL,
                            buttons=(gtk.STOCK_OK, 1, gtk.STOCK_CANCEL, 2))
        dialog.set_has_separator(False)
        dialog.set_size_request(400, -1)
        self.chkbox_use_encryption = gtk.CheckButton(language['use_wep_encryption'])
        self.chkbox_use_encryption.set_active(False)
        ip_entry = LabelEntry(language['ip'] + ':')
        essid_entry = LabelEntry(language['essid'] + ':')
        channel_entry = LabelEntry(language['channel'] + ':')
        self.key_entry = LabelEntry(language['key'] + ':')
        self.key_entry.set_auto_hidden(True)
        self.key_entry.set_sensitive(False)
        chkbox_use_ics = gtk.CheckButton(language['use_ics'])
        self.chkbox_use_encryption.connect("toggled",
                                           self.toggle_encrypt_check)
        channel_entry.entry.set_text('3')
        essid_entry.entry.set_text('My_Adhoc_Network')
        ip_entry.entry.set_text('169.254.12.10')  
        vbox_ah = gtk.VBox(False, 0)
        vbox_ah.pack_start(self.chkbox_use_encryption, False, False)
        vbox_ah.pack_start(self.key_entry, False, False)
        vbox_ah.show()
        dialog.vbox.pack_start(essid_entry)
        dialog.vbox.pack_start(ip_entry)
        dialog.vbox.pack_start(channel_entry)
        dialog.vbox.pack_start(chkbox_use_ics)
        dialog.vbox.pack_start(vbox_ah)
        dialog.vbox.set_spacing(5)
        dialog.show_all()
        response = dialog.run()
        if response == 1:
            wireless.CreateAdHocNetwork(essid_entry.entry.get_text(),
                                        channel_entry.entry.get_text(),
                                        ip_entry.entry.get_text(), "WEP",
                                        self.key_entry.entry.get_text(),
                                        self.chkbox_use_encryption.get_active(),
                                        False) 
        dialog.destroy()
    def toggle_encrypt_check(self, widget=None):
        """ Toggles the encryption key entry box for the ad-hoc dialog. """
        self.key_entry.set_sensitive(self.chkbox_use_encryption.get_active())
    def disconnect_all(self, widget=None):
        """ Disconnects from any active network. """
        daemon.Disconnect()
    def about_dialog(self, widget, event=None):
        """ Displays an about dialog. """
        dialog = gtk.AboutDialog()
        dialog.set_name("Wicd")
        dialog.set_version(daemon.Hello())
        dialog.set_authors([ "Adam Blackburn", "Dan O'Reilly" ])
        dialog.set_website("http://wicd.sourceforge.net")
        dialog.run()
        dialog.destroy()
    def key_event (self, widget, event=None):
        """ Handle key-release-events. """
        if event.state & gtk.gdk.CONTROL_MASK and \
           gtk.gdk.keyval_name(event.keyval) in ["w", "q"]:
            self.exit()
    def settings_dialog(self, widget, event=None):
        """ Displays a general settings dialog. """
        dialog = self.wTree.get_widget("pref_dialog")
        dialog.set_title(language['preferences'])
        size = config.ReadWindowSize("pref")
        width = size[0]
        height = size[1]
        if width > -1 and height > -1:
            dialog.resize(int(width), int(height))
        wiredcheckbox = self.wTree.get_widget("pref_always_check")
        wiredcheckbox.set_label(language['wired_always_on'])
        wiredcheckbox.set_active(wired.GetAlwaysShowWiredInterface())
        reconnectcheckbox = self.wTree.get_widget("pref_auto_check")
        reconnectcheckbox.set_label(language['auto_reconnect'])
        reconnectcheckbox.set_active(daemon.GetAutoReconnect())
        debugmodecheckbox = self.wTree.get_widget("pref_debug_check")
        debugmodecheckbox.set_label(language['use_debug_mode'])
        debugmodecheckbox.set_active(daemon.GetDebugMode())
        displaytypecheckbox = self.wTree.get_widget("pref_dbm_check")
        displaytypecheckbox.set_label(language['display_type_dialog'])
        displaytypecheckbox.set_active(daemon.GetSignalDisplayType())
        entryWiredAutoMethod = self.wTree.get_widget("pref_wired_auto_label")
        entryWiredAutoMethod.set_label('Wired Autoconnect Setting:')
        usedefaultradiobutton = self.wTree.get_widget("pref_use_def_radio")
        usedefaultradiobutton.set_label(language['use_default_profile'])
        showlistradiobutton = self.wTree.get_widget("pref_prompt_radio")
        showlistradiobutton.set_label(language['show_wired_list'])
        lastusedradiobutton = self.wTree.get_widget("pref_use_last_radio")
        lastusedradiobutton.set_label(language['use_last_used_profile'])
        self.wTree.get_widget("gen_settings_label").set_label(language["gen_settings"])
        self.wTree.get_widget("ext_prog_label").set_label(language["ext_programs"])
        self.wTree.get_widget("dhcp_client_label").set_label(language["dhcp_client"])
        self.wTree.get_widget("wired_detect_label").set_label(language["wired_detect"])
        self.wTree.get_widget("route_flush_label").set_label(language["route_flush"])
        dhcpautoradio = self.wTree.get_widget("dhcp_auto_radio")
        dhcpautoradio.set_label(language["wicd_auto_config"])
        dhclientradio = self.wTree.get_widget("dhclient_radio")
        pumpradio = self.wTree.get_widget("pump_radio")
        dhcpcdradio = self.wTree.get_widget("dhcpcd_radio")
        dhcp_list = [dhcpautoradio, dhclientradio, dhcpcdradio, pumpradio]
        dhcp_method = daemon.GetDHCPClient()
        dhcp_list[dhcp_method].set_active(True)
        linkautoradio = self.wTree.get_widget("link_auto_radio")
        linkautoradio.set_label(language['wicd_auto_config'])
        linkautoradio = self.wTree.get_widget("link_auto_radio")
        ethtoolradio = self.wTree.get_widget("ethtool_radio")
        miitoolradio = self.wTree.get_widget("miitool_radio")
        wired_link_list = [linkautoradio, ethtoolradio, miitoolradio]
        wired_link_method = daemon.GetLinkDetectionTool()
        wired_link_list[wired_link_method].set_active(True)
        flushautoradio = self.wTree.get_widget("flush_auto_radio")
        flushautoradio.set_label(language['wicd_auto_config'])
        ipflushradio = self.wTree.get_widget("ip_flush_radio")
        routeflushradio = self.wTree.get_widget("route_flush_radio")
        flush_list = [flushautoradio, ipflushradio, routeflushradio]
        flush_method = daemon.GetFlushTool()
        flush_list[flush_method].set_active(True)
        if wired.GetWiredAutoConnectMethod() == 1:
            usedefaultradiobutton.set_active(True)
        elif wired.GetWiredAutoConnectMethod() == 2:
            showlistradiobutton.set_active(True)
        elif wired.GetWiredAutoConnectMethod() == 3:
            lastusedradiobutton.set_active(True)
        self.set_label("pref_driver_label", language['wpa_supplicant_driver'] +
                       ':')
        wpa_hbox = self.wTree.get_widget("hbox_wpa")
        if not self.first_dialog_load:
            wpa_hbox.remove(self.wpadrivercombo)
        else:
            self.first_dialog_load = False
        self.wpadrivercombo = gtk.combo_box_new_text()
        wpadrivercombo = self.wpadrivercombo  
        wpa_hbox.pack_end(wpadrivercombo)
        wpadrivers = ["wext", "hostap", "madwifi", "atmel", "ndiswrapper", 
                      "ipw", "ralink legacy"]
        found = False
        def_driver = daemon.GetWPADriver()
        for i, x in enumerate(wpadrivers):
            if x == def_driver: 
                found = True
                user_driver_index = i
            wpadrivercombo.append_text(x)
        if found:
            wpadrivercombo.set_active(user_driver_index)
        else:
            wpadrivercombo.set_active(0)
        self.set_label("pref_wifi_label", language['wireless_interface'] + ':')
        self.set_label("pref_wired_label", language['wired_interface'] + ':')
        entryWirelessInterface = self.wTree.get_widget("pref_wifi_entry")
        entryWirelessInterface.set_text(daemon.GetWirelessInterface())
        entryWiredInterface = self.wTree.get_widget("pref_wired_entry")
        entryWiredInterface.set_text(daemon.GetWiredInterface())
        useGlobalDNSCheckbox = self.wTree.get_widget("pref_global_check")
        useGlobalDNSCheckbox.set_label(language['use_global_dns'])
        dns1Entry = self.wTree.get_widget("pref_dns1_entry")
        dns2Entry = self.wTree.get_widget("pref_dns2_entry")
        dns3Entry = self.wTree.get_widget("pref_dns3_entry")
        self.set_label("pref_dns1_label", language['dns'] + ' ' + language['1'])
        self.set_label("pref_dns2_label", language['dns'] + ' ' + language['2'])
        self.set_label("pref_dns3_label", language['dns'] + ' ' + language['3'])
        useGlobalDNSCheckbox.connect("toggled", checkboxTextboxToggle,
                                     (dns1Entry, dns2Entry, dns3Entry))
        dns_addresses = daemon.GetGlobalDNSAddresses()
        useGlobalDNSCheckbox.set_active(daemon.GetUseGlobalDNS())
        dns1Entry.set_text(noneToBlankString(dns_addresses[0]))
        dns2Entry.set_text(noneToBlankString(dns_addresses[1]))
        dns3Entry.set_text(noneToBlankString(dns_addresses[2]))
        if not daemon.GetUseGlobalDNS():
            dns1Entry.set_sensitive(False)
            dns2Entry.set_sensitive(False)
            dns3Entry.set_sensitive(False)
        entryWiredAutoMethod.set_alignment(0, 0)
        atrlist = pango.AttrList()
        atrlist.insert(pango.AttrWeight(pango.WEIGHT_BOLD, 0, 50))
        entryWiredAutoMethod.set_attributes(atrlist)
        self.wTree.get_widget("notebook2").set_current_page(0)
        dialog.show_all()
        invalid = True
        response = -1
        while invalid:
            response = dialog.run()
            invalid = False
            if response == 1:
                if useGlobalDNSCheckbox.get_active():
                    if not misc.IsValidIP(dns1Entry.get_text()):
                        invalid = True
                    if dns3Entry.get_text() and \
                       not misc.IsValidIP(dns2Entry.get_text()):
                        invalid = True
                    if dns3Entry.get_text() and \
                       not misc.IsValidIP(dns3Entry.get_text()):
                        invalid = True
                else:
                    for ent in [dns1Entry, dns2Entry, dns3Entry]:
                        ent.set_text("")
                if invalid: error(dialog, "One or more of your global DNS servers are invalid.")
        if response == 1:
            daemon.SetUseGlobalDNS(useGlobalDNSCheckbox.get_active())
            daemon.SetGlobalDNS(dns1Entry.get_text(), dns2Entry.get_text(),
                                dns3Entry.get_text())
            daemon.SetWirelessInterface(entryWirelessInterface.get_text())
            daemon.SetWiredInterface(entryWiredInterface.get_text())
            daemon.SetWPADriver(wpadrivers[wpadrivercombo.get_active()])
            wired.SetAlwaysShowWiredInterface(wiredcheckbox.get_active())
            daemon.SetAutoReconnect(reconnectcheckbox.get_active())
            daemon.SetDebugMode(debugmodecheckbox.get_active())
            daemon.SetSignalDisplayType(displaytypecheckbox.get_active())
            if showlistradiobutton.get_active():
                wired.SetWiredAutoConnectMethod(2)
            elif lastusedradiobutton.get_active():
                wired.SetWiredAutoConnectMethod(3)
            else:
                wired.SetWiredAutoConnectMethod(1)
            if dhcpautoradio.get_active():
                dhcp_client = misc.AUTO
            elif dhclientradio.get_active():
                dhcp_client = misc.DHCLIENT
            elif dhcpcdradio.get_active():
                dhcp_client = misc.DHCPCD
            else:
                dhcp_client = misc.PUMP
            daemon.SetDHCPClient(dhcp_client)
            if linkautoradio.get_active():
                link_tool = misc.AUTO
            elif ethtoolradio.get_active():
                link_tool = misc.ETHTOOL
            else:
                link_tool = misc.MIITOOL
            daemon.SetLinkDetectionTool(link_tool)
            if flushautoradio.get_active():
                flush_tool = misc.AUTO
            elif ipflushradio.get_active():
                flush_tool = misc.IP
            else:
                flush_tool = misc.ROUTE
            daemon.SetFlushTool(flush_tool)
        dialog.hide()
        [width, height] = dialog.get_size()
        config.WriteWindowSize(width, height, "pref")
    def set_label(self, glade_str, label):
        """ Sets the label for the given widget in wicd.glade. """
        self.wTree.get_widget(glade_str).set_label(label)
    def connect_hidden(self, widget):
        """ Prompts the user for a hidden network, then scans for it. """
        dialog = gtk.Dialog(title=language['hidden_network'],
                            flags=gtk.DIALOG_MODAL,
                            buttons=(gtk.STOCK_ADD, 1, gtk.STOCK_CANCEL, 2))
        dialog.set_has_separator(False)
        lbl = gtk.Label(language['hidden_network_essid'])
        textbox = gtk.Entry()
        dialog.vbox.pack_start(lbl)
        dialog.vbox.pack_start(textbox)
        dialog.show_all()
        button = dialog.run()
        if button == 1:
            answer = textbox.get_text()
            dialog.destroy()
            self.refresh_networks(None, True, answer)
        else:
            dialog.destroy()
    def cancel_connect(self, widget):
        """ Alerts the daemon to cancel the connection process. """
        cancel_button = self.wTree.get_widget("cancel_button")
        cancel_button.set_sensitive(False)
        daemon.CancelConnect()
        daemon.SetForcedDisconnect(True)
    def pulse_progress_bar(self):
        """ Pulses the progress bar while connecting to a network. """
        if not self.pulse_active:
            return False
        if not self.is_visible:
            return True
        try:
            self.wTree.get_widget("progressbar").pulse()
        except:
            pass
        return True
    def update_statusbar(self):
        """ Updates the status bar. """
        if not self.is_visible:
            return True
        wired_connecting = wired.CheckIfWiredConnecting()
        wireless_connecting = wireless.CheckIfWirelessConnecting()
        self.connecting = wired_connecting or wireless_connecting
        if self.connecting:
            if not self.pulse_active:
                self.pulse_active = True
                gobject.timeout_add(100, self.pulse_progress_bar)
                self.network_list.set_sensitive(False)
                self.status_area.show_all()
            if self.statusID:
                self.status_bar.remove(1, self.statusID)
            if wireless_connecting:
                iwconfig = wireless.GetIwconfig()
                self.set_status(wireless.GetCurrentNetwork(iwconfig) + ': ' +
                                language[str(wireless.CheckWirelessConnectingMessage())])
            if wired_connecting:
                self.set_status(language['wired_network'] + ': ' + 
                                language[str(wired.CheckWiredConnectingMessage())])
            return True
        else:
            if self.pulse_active:
                self.pulse_progress_bar()
                self.pulse_active = False
                self.network_list.set_sensitive(True)
                self.status_area.hide_all()
            if self.statusID:
                self.status_bar.remove(1, self.statusID)
            if self.check_for_wired(wired.GetWiredIP()):
                return True
            if self.check_for_wireless(wireless.GetIwconfig(),
                                       wireless.GetWirelessIP()):
                return True
            self.set_status(language['not_connected'])
            return True
    def update_connect_buttons(self, state=None, x=None, force_check=False):
        """ Updates the connect/disconnect buttons for each network entry. """
        if not state:
            state, x = daemon.GetConnectionStatus()
        if self.prev_state != state or force_check:
            apbssid = wireless.GetApBssid()
            for entry in self.network_list:
                if hasattr(entry, "update_connect_button"):
                    entry.update_connect_button(state, apbssid)
        self.prev_state = state
    def check_for_wired(self, wired_ip):
        """ Determine if wired is active, and if yes, set the status. """
        if wired_ip and wired.CheckPluggedIn():
            self.set_status(language['connected_to_wired'].replace('$A',
                                                                   wired_ip))
            return True
        else:
            return False
    def check_for_wireless(self, iwconfig, wireless_ip):
        """ Determine if wireless is active, and if yes, set the status. """
        if not wireless_ip:
            return False
        network = wireless.GetCurrentNetwork(iwconfig)
        if not network:
            return False
        network = str(network)
        if daemon.GetSignalDisplayType() == 0:
            strength = wireless.GetCurrentSignalStrength(iwconfig)
        else:
            strength = wireless.GetCurrentDBMStrength(iwconfig)
        if strength is None:
            return False
        strength = str(strength)            
        ip = str(wireless_ip)
        self.set_status(language['connected_to_wireless'].replace
                        ('$A', network).replace
                        ('$B', daemon.FormatSignalForPrinting(strength)).replace
                        ('$C', wireless_ip))
        return True
    def set_status(self, msg):
        """ Sets the status bar message for the GUI. """
        self.statusID = self.status_bar.push(1, msg)
    def dbus_scan_finished(self):
        """ Calls for a non-fresh update of the gui window.
        This method is called after the daemon runs an automatic
        rescan.
        """
        if not self.connecting:
            self.refresh_networks(fresh=False)
    def dbus_scan_started(self):
        self.network_list.set_sensitive(False)
    def refresh_networks(self, widget=None, fresh=True, hidden=None):
        """ Refreshes the network list.
        If fresh=True, scans for wireless networks and displays the results.
        If a ethernet connection is available, or the user has chosen to,
        displays a Wired Network entry as well.
        If hidden isn't None, will scan for networks after running
        iwconfig <wireless interface> essid <hidden>.
        """
        print "refreshing..."
        self.network_list.set_sensitive(False)
        self.wait_for_events()
        printLine = False  
        for z in self.network_list:
            self.network_list.remove(z)
            z.destroy()
            del z
        if wired.CheckPluggedIn() or wired.GetAlwaysShowWiredInterface():
            printLine = True  
            wirednet = WiredNetworkEntry()
            self.network_list.pack_start(wirednet, False, False)
            wirednet.connect_button.connect("button-press-event", self.connect,
                                            "wired", 0, wirednet)
            wirednet.disconnect_button.connect("button-press-event", self.disconnect,
                                               "wired", 0, wirednet)
            wirednet.advanced_button.connect("button-press-event",
                                             self.edit_advanced, "wired", 0, 
                                             wirednet)
        if fresh:
            wireless.SetHiddenNetworkESSID(noneToString(hidden))
            wireless.Scan()
        num_networks = wireless.GetNumberOfNetworks()
        instruct_label = self.wTree.get_widget("label_instructions")
        if num_networks > 0:
            instruct_label.show()
            for x in range(0, num_networks):
                if printLine:
                    sep = gtk.HSeparator()
                    self.network_list.pack_start(sep, padding=10, fill=False,
                                                 expand=False)
                    sep.show()
                else:
                    printLine = True
                tempnet = WirelessNetworkEntry(x)
                print "=======",wireless.GetWirelessProperty(x, 'essid'),"========"
                tempnet.show_all()
                self.network_list.pack_start(tempnet, False, False)
                tempnet.connect_button.connect("button-press-event",
                                               self.connect, "wireless", x,
                                               tempnet)
                tempnet.disconnect_button.connect("button-press-event",
                                                  self.disconnect, "wireless",
                                                  x, tempnet)
                tempnet.advanced_button.connect("button-press-event",
                                                self.edit_advanced, "wireless",
                                                x, tempnet)
        else:
            instruct_label.hide()
            if wireless.GetKillSwitchEnabled():
                label = gtk.Label(language['killswitch_enabled'] + ".")
            else:
                label = gtk.Label(language['no_wireless_networks_found'])
            self.network_list.pack_start(label)
            label.show()
        self.update_connect_buttons(force_check=True)
        self.network_list.set_sensitive(True)
    def save_settings(self, nettype, networkid, networkentry):
        """ Verifies and saves the settings for the network entry. """
        entry = networkentry.advanced_dialog
        entlist = []
        if entry.chkbox_static_ip.get_active():
            entlist = [ent for ent in [entry.txt_ip, entry.txt_netmask,
                                       entry.txt_gateway]]
        if entry.chkbox_static_dns.get_active() and \
           not entry.chkbox_global_dns.get_active():
            entlist.append(entry.txt_dns_1)
            for ent in [entry.txt_dns_2, entry.txt_dns_3]:
                if ent.get_text() != "":
                    entlist.append(ent)
        for lblent in entlist:
            if not misc.IsValidIP(lblent.get_text()):
                error(self.window, language['invalid_address'].
                      replace('$A', lblent.label.get_label()))
                return False
        if entry.chkbox_global_dns.get_active() and \
           not daemon.GetUseGlobalDNS():
            error(self.window, language['no_global_dns'])
            return False
        if nettype == "wireless":
            if not self.save_wireless_settings(networkid, entry, networkentry):
                return False
        elif nettype == "wired":
            if not self.save_wired_settings(entry):
                return False
        return True
    def save_wired_settings(self, entry):
        """ Saved wired network settings. """
        if entry.chkbox_static_ip.get_active():
            entry.set_net_prop("ip", noneToString(entry.txt_ip.get_text()))
            entry.set_net_prop("netmask", noneToString(entry.txt_netmask.get_text()))
            entry.set_net_prop("gateway", noneToString(entry.txt_gateway.get_text()))
        else:
            entry.set_net_prop("ip", '')
            entry.set_net_prop("netmask", '')
            entry.set_net_prop("gateway", '')
        if entry.chkbox_static_dns.get_active() and \
           not entry.chkbox_global_dns.get_active():
            entry.set_net_prop('use_static_dns', True)
            entry.set_net_prop('use_global_dns', False)
            entry.set_net_prop("dns1", noneToString(entry.txt_dns_1.get_text()))
            entry.set_net_prop("dns2", noneToString(entry.txt_dns_2.get_text()))
            entry.set_net_prop("dns3", noneToString(entry.txt_dns_3.get_text()))
        elif entry.chkbox_static_dns.get_active() and \
             entry.chkbox_global_dns.get_active():
            entry.set_net_prop('use_static_dns', True)
            entry.set_net_prop('use_global_dns', True)
        else:
            entry.set_net_prop('use_static_dns', False)
            entry.set_net_prop('use_global_dns', False)
            entry.set_net_prop("dns1", '')
            entry.set_net_prop("dns2", '')
            entry.set_net_prop("dns3", '')
        config.SaveWiredNetworkProfile(entry.prof_name)
        return True
    def save_wireless_settings(self, networkid, entry, netent):
        """ Save wireless network settings. """
        if entry.chkbox_encryption.get_active():
            print "setting encryption info..."
            encryption_info = entry.encryption_info
            encrypt_methods = misc.LoadEncryptionMethods()
            entry.set_net_prop("enctype",
                               encrypt_methods[entry.combo_encryption.
                                               get_active()][1])
            for x in encryption_info:
                if encryption_info[x].get_text() == "":
                    error(self.window, language['encrypt_info_missing'])
                    return False
                entry.set_net_prop(x, noneToString(encryption_info[x].
                                                   get_text()))
        elif not entry.chkbox_encryption.get_active() and \
             wireless.GetWirelessProperty(networkid, "encryption"):
            error(self.window, language['enable_encryption'])
            return False
        else:
            print 'encryption is ' + str(wireless.GetWirelessProperty(networkid, 
                                                                      "encryption"))
            print "no encryption specified..."
            entry.set_net_prop("enctype", "None")
        entry.set_net_prop("automatic",
                           noneToString(netent.chkbox_autoconnect.get_active()))
        if entry.chkbox_static_ip.get_active():
            entry.set_net_prop("ip", noneToString(entry.txt_ip.get_text()))
            entry.set_net_prop("netmask",
                               noneToString(entry.txt_netmask.get_text()))
            entry.set_net_prop("gateway",
                               noneToString(entry.txt_gateway.get_text()))
        else:
            entry.set_net_prop("ip", '')
            entry.set_net_prop("netmask", '')
            entry.set_net_prop("gateway", '')
        if entry.chkbox_static_dns.get_active() and \
           not entry.chkbox_global_dns.get_active():
            entry.set_net_prop('use_static_dns', True)
            entry.set_net_prop('use_global_dns', False)
            entry.set_net_prop('dns1', noneToString(entry.txt_dns_1.get_text()))
            entry.set_net_prop('dns2', noneToString(entry.txt_dns_2.get_text()))
            entry.set_net_prop('dns3', noneToString(entry.txt_dns_3.get_text()))
        elif entry.chkbox_static_dns.get_active() and \
             entry.chkbox_global_dns.get_active():
            entry.set_net_prop('use_static_dns', True)
            entry.set_net_prop('use_global_dns', True)
        else:
            entry.set_net_prop('use_static_dns', False) 
            entry.set_net_prop('use_global_dns', False)
            entry.set_net_prop('dns1', '')
            entry.set_net_prop('dns2', '')
            entry.set_net_prop('dns3', '')
        if entry.chkbox_global_settings.get_active():
            entry.set_net_prop('use_settings_globally', True)
        else:
            entry.set_net_prop('use_settings_globally', False)
            config.RemoveGlobalEssidEntry(networkid)
        config.SaveWirelessNetworkProfile(networkid)
        return True
    def edit_advanced(self, widget, event, ttype, networkid, networkentry):
        """ Display the advanced settings dialog.
        Displays the advanced settings dialog and saves any changes made.
        If errors occur in the settings, an error message will be displayed
        and the user won't be able to save the changes until the errors
        are fixed.
        """
        dialog = networkentry.advanced_dialog
        dialog.set_values()
        dialog.show_all()
        while True:
            if self.run_settings_dialog(dialog, ttype, networkid, networkentry):
                break
        dialog.hide()
    def run_settings_dialog(self, dialog, nettype, networkid, networkentry):
        """ Runs the settings dialog.
        Runs the settings dialog and returns True if settings are saved
        successfully, and false otherwise.
        """
        result = dialog.run()
        if result == gtk.RESPONSE_ACCEPT:
            if self.save_settings(nettype, networkid, networkentry):
                return True
            else:
                return False
        return True
    def check_encryption_valid(self, networkid, entry):
        """ Make sure that encryption settings are properly filled in. """
        if entry.chkbox_encryption.get_active():
            encryption_info = entry.encryption_info
            for x in encryption_info:
                if encryption_info[x].get_text() == "":
                    error(self.window, language['encrypt_info_missing'])
                    return False
        elif not entry.chkbox_encryption.get_active() and \
             wireless.GetWirelessProperty(networkid, "encryption"):
            error(self.window, language['enable_encryption'])
            return False
        return True
    def connect(self, widget, event, nettype, networkid, networkentry):
        """ Initiates the connection process in the daemon. """
        cancel_button = self.wTree.get_widget("cancel_button")
        cancel_button.set_sensitive(True)
        if nettype == "wireless":
            if not self.check_encryption_valid(networkid,
                                               networkentry.advanced_dialog):
                return False
            wireless.ConnectWireless(networkid)
        elif nettype == "wired":
            wired.ConnectWired()
        self.update_statusbar()
    def disconnect(self, widget, event, nettype, networkid, networkentry):
        """ Disconnects from the given network.
        Keyword arguments:
        widget -- The disconnect button that was pressed.
        event -- unused
        nettype -- "wired" or "wireless", depending on the network entry type.
        networkid -- unused
        networkentry -- The NetworkEntry containing the disconnect button.
        """
        widget.hide()
        networkentry.connect_button.show()
        if nettype == "wired":
            wired.DisconnectWired()
        else:
            wireless.DisconnectWireless()
    def wait_for_events(self, amt=0):
        """ Wait for any pending gtk events to finish before moving on. 
        Keyword arguments:
        amt -- a number specifying the number of ms to wait before checking
               for pending events.
        """
        time.sleep(amt)
        while gtk.events_pending():
            gtk.main_iteration()
    def exit(self, widget=None, event=None):
        """ Hide the wicd GUI.
        This method hides the wicd GUI and writes the current window size
        to disc for later use.  This method normally does NOT actually 
        destroy the GUI, it just hides it.
        """
        self.window.hide()
        [width, height] = self.window.get_size()
        config.WriteWindowSize(width, height, "main")
        if self.standalone:
            self.window.destroy()
            sys.exit(0)
        self.is_visible = False
        daemon.SetGUIOpen(False)
        self.wait_for_events()
        return True
    def show_win(self):
        """ Brings the GUI out of the hidden state. 
        Method to show the wicd GUI, alert the daemon that it is open,
        and refresh the network list.
        """
        self.window.present()
        self.wait_for_events()
        self.is_visible = True
        daemon.SetGUIOpen(True)
        self.wait_for_events(0.1)
        gobject.idle_add(self.refresh_networks)
setup_dbus()
if __name__ == '__main__':
    app = appGui(standalone=True)
    bus.add_signal_receiver(app.dbus_scan_finished, 'SendEndScanSignal',
                            'org.wicd.daemon')
    bus.add_signal_receiver(app.dbus_scan_started, 'SendStartScanSignal',
                            'org.wicd.daemon')
    bus.add_signal_receiver(app.update_connect_buttons, 'StatusChanged',
                            'org.wicd.daemon')
    gtk.main()
