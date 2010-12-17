import ConfigParser
class Config(object):
    
    class __Parser(object):
        name = None
        def a(self, name = None):
            if name:
                self.name = name
                self.add_section(self.name)
        def s(self, key = None, value = None, name = None):
            if name:
                self.name = name
            if self.name and key:
                self.set(self.name, key, value)
        def w(self, file):
            with open(file, 'wb') as c:
                self.write(c)
                
    class Conf(ConfigParser.ConfigParser, __Parser):
        pass
    class Raw(ConfigParser.RawConfigParser, __Parser):
        pass
    class Safe(ConfigParser.SafeConfigParser, __Parser):
        pass
        
