# encoding: utf-8
"""
@author: liuyun
@time: 2019/5/10/010 17:33
@desc:
"""

import re
import os
import tempfile


class Properties:

    def __init__(self, file_name):
        self.file_name = file_name
        self.properties = {}
        try:
            fopen = open(self.file_name, 'r')
            for line in fopen:
                line = line.strip()
                if line.find('=') > 0 and not line.startswith('#'):
                    strs = line.split('=')
                    self.properties[strs[0].strip()] = strs[1].strip()
        except Exception as e:
            raise e
        else:
            fopen.close()

    def has_key(self, key):
        return key in self.properties

    def get(self, key, default_value=''):
        if key in self.properties:
            return self.properties[key]
        return default_value

    def put(self, key, value):
        self.properties[key] = value
        replace_property(self.file_name, key + '=.*', key + '=' + value, True)

    def get_by_api(self, api, ip=''):
        for k in self.properties:
            r = k.split(':')
            if self._match_api(api, r[1]) and self._match_ip(ip, r[0]):
                return self.properties[k]
        return None

    def _match_ip(self, ip, value):
        if not ip:
            return True
        if ip == value:
            return True
        if value == '.*':
            return True

        return False

    def _match_api(self, api, value):
        return api == value

    def get_default(self, ip):
        default_ip = ''
        for k in self.properties:
            r = k.split(":")
            if self._match_ip(ip, r[0]) and r[1] == '.*':
                default_ip = self.properties[k]
        return default_ip






def parse(file_name):
    return Properties(file_name)


def replace_property(file_name, from_regex, to_str, append_on_not_exists=True):
    tmpfile = tempfile.TemporaryFile()

    if os.path.exists(file_name):
        r_open = open(file_name, 'r')
        pattern = re.compile(r'' + from_regex)
        found = None
        for line in r_open:
            if pattern.search(line) and not line.strip().startswith('#'):
                found = True
                line = re.sub(from_regex, to_str, line)
            tmpfile.write(bytes(line, encoding='utf-8'))
        if not found and append_on_not_exists:
            tmpfile.write(bytes('\n' + to_str, encoding='utf-8'))
        r_open.close()
        tmpfile.seek(0)

        content = tmpfile.read()

        if os.path.exists(file_name):
            os.remove(file_name)

        with open(file_name, 'w') as w_open:
            w_open.write(str(content, encoding='utf-8'))

        tmpfile.close()
    else:
        print ("file %s not found" % file_name)


# if __name__ == '__main__':
#     f = parse('test2.properties')
#     f.put('aaa', 'cccc')
