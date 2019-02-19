def search_file(rootdir):  # 搜索文件夹unicode ur"D:\20170818"
    import os
    import os.path
    search_reault = {}
    for parent, dirnames, filenames in os.walk(rootdir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        search_reault[parent] = {'dir': [], 'file': []}
        for dirname in dirnames:  # 文件夹信息
            search_reault[parent]['dir'].append(dirname)
        for filename in filenames:  # 文件信息
            search_reault[parent]['file'].append(filename)
            # os.rename(os.path.join(parent, filename), os.path.join(parent, urllib.unquote(filename.encode('utf-8'))))  # rename
    return search_reault  # {path: {'dir': [], 'file': []},...}

os.path.realpath(__file__)  # 获取当前文件__file__的路径
os.path.dirname(os.path.realpath(__file__))  # 获取当前文件__file__的所在目录
os.path.join(os.path.dirname(os.path.realpath(__file__)), "data.json")  # 拼接路径
