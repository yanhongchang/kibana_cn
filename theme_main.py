# coding: utf-8

import os
import sys
import json
import shutil
import ConfigParser

conf = ConfigParser.ConfigParser()
conf.read("./etc/theme.conf")
old_logo = "src/ui/public/images/kibana.svg"
new_logo = "./images/kibana.svg"
optimize_path = "optimize/bundles/"

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except Exception as e:
    pass


class ThemeModify(object):
    def __init__(self, kibana_dir):
        self.kibana_path = kibana_dir
        self.old_logo = os.path.join(self.kibana_path, old_logo)
        self.new_log = new_logo
        self.optimize_path = optimize_path
        self.resource_path = './resource/theme_resource.json'
        with open(self.resource_path, "r") as f:
            theme_content = f.read()
        self.theme_content = json.loads(theme_content)

    def update_theme(self):
        theme_update = False
        for item in self.theme_content:
            path = item.get("path", "")
            abs_path = os.path.join(self.kibana_path, path)
            old_color = item.get("old_color", "")
            new_color = item.get("new_color", "")
            if old_color == "" or new_color == "":
                continue
            with open(abs_path, "r") as f:
                file_content = f.read()
                if file_content.find(str(old_color)) != -1:
                    file_content = file_content.replace(old_color, new_color)
                theme_update = True

            if theme_update:
                print "文件{0}中主题颜色已被更新。".format(abs_path)
                with open(abs_path, "w") as f:
                    f.write(str(file_content))


    def update_logo(self):
        print self.old_logo+".bak"
        if not os.path.exists(self.old_logo+".bak"):
            shutil.move(self.old_logo, self.old_logo+".bak")
        try:
            shutil.copy(new_logo, self.old_logo)
        except Exception as e:
            raise

    def clean_optim_file(self, logo_update=True):
        opt_list = os.listdir(os.path.join(self.kibana_path, self.optimize_path))
        for f in opt_list:
            f_abspath = os.path.join(self.kibana_path, self.optimize_path, f)
            if os.path.isfile(f_abspath) and logo_update:
                    if f.split(".")[1] == "svg":
                        os.remove(f_abspath)


if __name__ == "__main__":
    path = "/home/jourmin/PycharmProjects/kibana_test/kibana-6.2.2-linux-x86_64/"
    if len(sys.argv) == 2 or len(path) != 0:
        try:
            #kibana_dir = sys.argv[1]
            #if not str(kibana_dir).endswith('/'):
            #    kibana_dir = kibana_dir + '/'
            kibana_dir = path
            themeObj = ThemeModify(kibana_dir)
            themeObj.update_theme()
            logo_update = conf.getboolean("default", "logo_update")
            if logo_update:
                themeObj.update_logo()
            #themeObj.clean_optim_file(logo_update=logo_update)
            print "恭喜! 您的kibana主题更新成功,请重新启动kibana服务生效"
        except Exception as e:
            print "oh,抱歉! 您的kibana主题更新失败，错误如下：{0}".format(str(e))
    else:
        print "使用示例： python translate_main.py '/usr/share/kibana/'"