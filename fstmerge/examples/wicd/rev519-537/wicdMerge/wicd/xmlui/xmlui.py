import xml.sax
the_interface = None
controls = None
class  XmlUi (xml.sax.ContentHandler) :
	def __init__(self, callback_handler, uiset):
        xml.sax.ContentHandler.__init__(self)
        self.callback_handler = callback_handler
        self.gui = None
        self.last_top_element = []
        self.last_element = []
        self.latest_text = []
        self.controls = {}
        self.uiset = uiset
    
	def startDocument(self):
        pass
    
	def endDocument(self):
        global the_interface, controls
        the_interface = self.gui
        controls = self.controls
    
	def _add_new_top_level(self, tag, item):
        self.add_interface_item(item)
        self.last_top_element.append((tag, item))
        self.last_element.append((tag, item))
    
	def _add_new(self, tag, item):
        self.add_interface_item(item)
        self.last_element.append((tag, item))
    
	def _connect_handler(self, item, signal, handler):
        if handler:
            handler.strip()
        if handler:
            getattr(item, 'connect_' + signal)(getattr(self.callback_handler, handler))
    
	def _process_attributes(self, item, attributes):
        for attribute, value in dict(attributes).iteritems():
            attribute = attribute.strip()
            value = value.strip()
            if attribute.startswith('action_'):
                self._connect_handler(item, attribute[7:], value)
            elif attribute == 'name':
                self.controls[value] = item
            else:
                method = getattr(item, 'set_' + attribute)
                method(value)
    
	def startElement(self, tag, attributes):
        if tag == 'text':
            self.latest_text = []
        else:
            ui_items = dir(self.uiset)
            match = None
            for item in ui_items:
                if item.startswith('Simple') and \
                        item[6:].lower() == tag.lower():
                    match = item
                    break
            uicomponent = getattr(self.uiset, match)
            object = uicomponent(self.callback_handler)
            self._process_attributes(object, attributes)
            if object.top_level:
                self._add_new_top_level(tag, object)
            else:
                self._add_new(tag, object)
    
	def characters(self, data):
        self.latest_text.append(data)
    
	def _print_debug(self):
        print 'Last top element:'
        print self.last_top_element
        print 'Last element:'
        print self.last_element
        print 'Latest text:'
        print self.latest_text
        print 'Controls:'
        print self.controls
    
	def endElement(self, tag):
        if self.latest_text and tag == 'text':
            text = ''.join(self.latest_text).strip()
            if text:
                self.latest_text = []
                self.set_label(text)
        if not len(self.last_top_element) > 0:
            return
        if self.last_top_element[-1][0] == tag:
            self.last_top_element.pop()
        if self.last_element[-1][0] == tag:
            self.last_element.pop()
    
	def set_label(self, label):
        self.last_element[-1][1].set_label(label)
    
	def add_interface_item(self, item):
        if self.gui is None:
            self.gui = item
            return
        attributes = dir(self.last_top_element[-1][1])
        self.last_top_element[-1][1].add(item.control)


def generate_interface(xmlstring, callback_handler, uiset):
    p = xml.sax.make_parser()
    p.setContentHandler(XmlUi(callback_handler, uiset))
    p.feed(xmlstring)
    p.close()
    return the_interface, controls

