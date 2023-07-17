# 文件夹路径
folder_path = ""
# 获取文件夹中的点云文件列表
file_list = sorted([f for f in os.listdir(folder_path) if f.endswith('.bin')])