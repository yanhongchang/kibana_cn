# coding: utf-8

import os
import sys
import json

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except Exception as e:
    pass


class Translate(object):
    def __init__(self, kibana_dir):
        self.dir = kibana_dir
        print sys.path[0]
        self.resource_path = sys.path[0] + '/kibana_resource.json'
        f = open(self.resource_path, "r")
        self.tran_content = json.loads(f.read())

    def trans(self):
        not_exist_file = []
        for item in self.tran_content:
            src_change = False
            try:
                with open(self.dir + item['path'], 'r') as f:
                    src_content = f.read()
            except Exception:
                not_exist_file.append(self.dir + item['path'])
                continue

            en = item['en']
            cn = item['cn']
            if src_content.find(str(en)) != -1:
                des_content = src_content.replace(en, cn)
                src_change = True

            if src_change:
                with open(self.dir + item['path'], 'w') as f:
                    f.write(des_content)

        if len(not_exist_file) > 0:
            print 'no exist file list:' + str(not_exist_file)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        kibana_dir = sys.argv[1]
        #kibana_dir = '/home/jourmin/PycharmProjects/kikaba_cn'
        otran = Translate(kibana_dir)
        otran.trans()

    else:
        print "使用示例： python tran_main.py '/usr/share/kibana/'"
