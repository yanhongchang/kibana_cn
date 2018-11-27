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
        self.kibana_dir = kibana_dir
        self.tran_file_ext = ["js", "html", "json"]
        self.resource_path = './resource/cn_resource.json'
        with open(self.resource_path, "r") as f:
            trans_content = f.read()
        self.tran_content = json.loads(trans_content)

    def trans_cn(self):
        tran_file_count = 0
        item_count_sum = 0
        for root_dir, dirs, files in os.walk(self.kibana_dir):
            for f in files:
                if not self._check_file(f, self.tran_file_ext):
                    continue
                # windows os need replace '\\' to '/'
                source_file_path = root_dir.replace('\\', '/') + '/' + f.replace('\\', '/')
                with open(source_file_path, 'r') as fi:
                    f_content = fi.read()
                file_changed = False
                for item in self.tran_content:
                    path = item.get("path", "")
                    if source_file_path.find(str(path)) == -1:
                        continue
                    en = item.get("en", "")
                    cn = item.get("cn", "")
                    if en == "" or cn == "":
                        continue
                    if f_content.find(str(en)) != -1:
                        item_count_sum += 1
                        f_content = f_content.replace(en, cn)
                        file_changed = True

                if file_changed:
                    print "文件{0}已被翻译。".format(source_file_path)
                    with open(source_file_path, "w") as f:
                        f.write(str(f_content))
                    tran_file_count += 1

        return tran_file_count, item_count_sum

        # not_exist_file = []
        # for item in self.tran_content:
        #     src_changed = False
        #     try:
        #         with open(self.dir + item['path'], 'r') as f:
        #             src_content = f.read()
        #     except Exception:
        #         not_exist_file.append(self.dir + item['path'])
        #         continue
        #
        #     en = item['en']
        #     cn = item['cn']
        #     if src_content.find(str(en)) != -1:
        #         des_content = src_content.replace(en, cn)
        #         src_change = True
        #
        #     if src_changed:
        #         with open(self.dir + item['path'], 'w') as f:
        #             f.write(des_content)
        #
        # if len(not_exist_file) > 0:
        #     print 'no exist file list:' + str(not_exist_file)

    @staticmethod
    def _check_file(f, whitelist):
        if len(whitelist) == 0:
            return True
        ext = os.path.splitext(f)[1]
        if ext.strip('.') in whitelist:
            return True
        else:
            return False


if __name__ == '__main__':
    if len(sys.argv) == 2:
        try:
            kibana_dir = sys.argv[1]
            if not str(kibana_dir).endswith('/'):
                kibana_dir = kibana_dir + '/'
            otran = Translate(kibana_dir)
            tran_file_counts, tran_item_counts = otran.trans_cn()
            print "恭喜! 您的kibana汉化成功，{0}个文件总共翻译了{1}处".format(tran_file_counts, tran_item_counts)
        except Exception as e:
            print "oh,抱歉! 您的kibana汉化失败，错误如下：{0}".format(str(e))
    else:
        print "使用示例： python translate_main.py '/usr/share/kibana/'"
