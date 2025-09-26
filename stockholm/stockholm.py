from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


WANNACRY_EXTENSIONS = {
    '123', '3dm', '3ds', '3g2', '3gp', '602', '7z', 'accdb', 'aes', 'ai',
    'asp', 'aspx', 'avhd', 'back', 'bak', 'bmp', 'brd', 'bz2', 'cgm', 'class',
    'cmd', 'cpp', 'crt', 'cs', 'csv', 'db', 'dbf', 'dch', 'der', 'dif', 'dip',
    'djvu', 'doc', 'docb', 'docm', 'docx', 'dot', 'dotm', 'dotx', 'dwg', 'edb',
    'eml', 'fdb', 'fla', 'flv', 'frm', 'gif', 'gpg', 'gz', 'hwp', 'ibd', 'iso',
    'jar', 'java', 'jpeg', 'jpg', 'js', 'jsp', 'key', 'lay', 'lay6', 'ldf', 'm3u',
    'm4u', 'max', 'mdb', 'mdf', 'myd', 'myi', 'nef', 'odb', 'odg', 'odp', 'ods',
    'odt', 'onepkg', 'ost', 'otg', 'otp', 'ots', 'ott', 'p12', 'pas', 'pdf', 'pem',
    'pfx', 'php', 'pl', 'png', 'pot', 'potm', 'potx', 'ppam', 'pps', 'ppsm', 'ppsx',
    'ppt', 'pptm', 'pptx', 'ps1', 'psd', 'pst', 'rar', 'raw', 'rb', 'rtf', 'sch',
    'sh', 'sldm', 'sldx', 'sln', 'snt', 'sql', 'sqlite3', 'sqlitedb', 'stc', 'std',
    'sti', 'stw', 'suo', 'svg', 'swf', 'sxc', 'sxd', 'sxi', 'sxm', 'sxw', 'tar',
    'tbk', 'tgz', 'tif', 'tiff', 'txt', 'uop', 'uot', 'vb', 'vbs', 'vcd', 'vdi',
    'vmdk', 'vmx', 'vob', 'vsd', 'vsdx', 'wav', 'wb2', 'wk1', 'wks', 'wma', 'wmv',
    'xlc', 'xlm', 'xls', 'xlsb', 'xlsm', 'xlsx', 'xlt', 'xltm', 'xltx', 'xlw',
    'xml', 'zip'
}

def main():
    print("Hello")

if __name__ == '__main__':
   main()