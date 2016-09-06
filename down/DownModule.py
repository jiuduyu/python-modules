
# encoding:utf-8
import os
import urllib


class DownModule(object):
    joinPath = './fonts'
    url = ''
    local = ''
    cusFileName = ''
    per = ''

    def __init__(self, *args, **kwargs):
        super(DownModule, self).__init__(*args, **kwargs)

    @staticmethod
    def makePath(path):
        DownModule.joinPath = path if path else DownModule.joinPath
        if os.path.exists(DownModule.joinPath) is False:
            os.makedirs(DownModule.joinPath)

    @staticmethod
    def downFile(url=None, path=None):
        DownModule.makePath(path)
        DownModule.url = url
        if DownModule.url is None:
            print "url is not empty"
            return False

        DownModule.cusFileName = os.path.basename(DownModule.url)

        DownModule.local = os.path.join(
            DownModule.joinPath, DownModule.cusFileName)
        urllib.urlretrieve(DownModule.url, DownModule.local)
        return str(DownModule.joinPath) + '/' + str(DownModule.cusFileName)
