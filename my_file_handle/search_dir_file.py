def search_file(rootdir):  # �����ļ���unicode ur"D:\20170818"
    import os
    import os.path
    search_reault = {}
    for parent, dirnames, filenames in os.walk(rootdir):  # �����������ֱ𷵻�1.��Ŀ¼ 2.�����ļ������֣�����·���� 3.�����ļ�����
        search_reault[parent] = {'dir': [], 'file': []}
        for dirname in dirnames:  # �ļ�����Ϣ
            search_reault[parent]['dir'].append(dirname)
        for filename in filenames:  # �ļ���Ϣ
            search_reault[parent]['file'].append(filename)
            # os.rename(os.path.join(parent, filename), os.path.join(parent, urllib.unquote(filename.encode('utf-8'))))  # rename
    return search_reault  # {path: {'dir': [], 'file': []},...}