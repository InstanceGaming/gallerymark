import os
from PyQt5.QtCore import QByteArray, QBuffer, QIODevice, QFile
from PyQt5.QtGui import QColor, QPixmap


def format_file_size(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(int(size)) + power_labels[n]+'B'


def get_file_size(path):
    return os.stat(path).st_size


def copyPixmap(src):
    return src.copy(0, 0, src.width(), src.height())


def generateDrawingPixmap(source):
    p = QPixmap(source.size())
    p.fill(QColor(255, 255, 255, alpha=0))
    return p


def generateTestPixmap(source):
    p = QPixmap(source.size())
    p.fill(QColor(255, 0, 0))
    return p


def writePixmap(pixmap, path, format):
    f = QFile(path)
    f.open(QFile.WriteOnly)
    pixmap.save(f, format)


def qtPixmapToJPG(pixmap):
    arr = QByteArray()
    b = QBuffer(arr)
    b.open(QIODevice.WriteOnly)

    if pixmap.save(b, "JPG"):
        return arr.data()
    return None


def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')
