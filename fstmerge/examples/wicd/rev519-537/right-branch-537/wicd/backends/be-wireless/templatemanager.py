import os, sys
class EncryptionTemplate: pass
class TemplateManager:
    def __init__(self):
        self._templates = {}
        path = os.path.dirname(os.path.realpath(__file__))
        self.template_dir = os.path.join(path, 'templates')
    def get_available_template_files(self):
        template_list = []
        for f in os.listdir(self.template_dir):
            if self._valid_template_file(f):
                template_list.append(f)
        return template_list
    def _valid_template_file(self,template):
        ''' Checks if a file is a valid template. '''
        isnttemplatepy = not (template == 'template.py')
        endswithpy = template.endswith('.py')
        return isnttemplatepy and endswithpy
    def load_all_available_templates(self):
        self.clear_all()
        for template in self.get_available_template_files():
            print 'loading wpa_supplicant template %s' % template
            self.load_template(template)
    def load_template(self, template):
        if self._valid_template_file(template):
            shortname = template[:-3]
            sys.path.insert(0, self.template_dir)
            template = __import__(shortname)
            sys.path.remove(self.template_dir)
            for item in dir(template):
                if item.startswith('Template'):
                    template_class = getattr(template, item)
                    self._templates[item[8:]] = template_class
    def clear_all(self):
        self._templates = {}
    def get_template(self, name):
        return self._templates.get(name)
