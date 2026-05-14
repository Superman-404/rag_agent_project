import os.path

def get_current_path():
    """
    获取工程所在的根目录
    :return: 字符串根目录
    """
    # 当前文件的绝对路径
    current_file = os.path.abspath(__file__)
    # 当前文件所在的文件夹绝对路径
    current_dir = os.path.dirname(current_file)
    # 当前文件所在文件夹的root路径
    project_root = os.path.dirname(current_dir)
    return project_root

def get_asb_path(relative_path : str)-> str:
    """
    获取绝对路径
    :param relative_path: 相对路径
    :return: 绝对路径
    """
    return os.path.join(get_current_path(), relative_path)

if __name__ == '__main__':
    print(get_asb_path('config/config.txt'))
    print(get_current_path())