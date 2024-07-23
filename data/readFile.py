import os

# 设置你想要遍历的文件夹路径
folder_path = './'


def writeData(file_path, data):
    # 设置文件路径
    file_path = 'data.txt'

    # 使用'a'模式打开文件，这将允许我们在文件末尾追加内容
    # 如果文件不存在，'a'模式会创建文件
    with open(file_path, 'a') as file:
        file.write(data)

def getData(file_path):

    file_content = ""
    # 打开文件并读取内容
    if("ana" not in file_path):
        return
    with open(file_path, 'r') as file:
        file_content = file.read()

    # 打印文件内容
    # print(file_content)
    import re

    # 模拟的文件内容，通常这里应该是文件读取操作得到的字符串
    """
    Application:AntPat 2.0
    File:SR4BC-HF3P4LDF(D00-PIP)_806.ana
    Brand:Sinclair Technologies Inc.
    Model:SR4BC-HF3P4LDF(D00-PIP)
    ...
    Test Freq(MHz):806
    Magnitude Type:TRUE LOG
    Horizontal Pattern:
    0.00 11.670
    ...
    Vertical Pattern:
    0.00 12.350
    ...
    """
    # 使用正则表达式查找Test Freq数值
    test_freq_pattern = re.compile(r"Test Freq\(MHz\):(\d+\.?\d*)")
    test_freq_match = test_freq_pattern.search(file_content)
    test_freq = float(test_freq_match.group(1)) if test_freq_match else None
    if(test_freq==None):
        return
    # 使用正则表达式查找Test Freq数值
    test_freq_pattern = re.compile(r"Test Freq\(MHz\):(\d+\.?\d*)")
    test_freq_match = test_freq_pattern.search(file_content)
    test_freq = float(test_freq_match.group(1)) if test_freq_match else None

    # 提取Horizontal和Vertical Pattern下的角度和增益
    pattern_pattern = re.compile(r"(\d+\.\d+)\s+(-?\d+\.\d+)")
    # vertical_pattern = pattern_pattern.findall(file_content, "Vertical Pattern:")
    horizontal_pattern = pattern_pattern.findall(file_content)
    # vertical_pattern = pattern_pattern.findall(file_content, "Vertical Pattern:")
    if(horizontal_pattern.__len__()<400):
        len = horizontal_pattern.__len__()
        flag = "0 "
        if("Vertical Pattern" in file_content):
            flag = "1 "
        for i in range(1, len):
            data = ""
            data = data + str(test_freq) + " " + flag + str(horizontal_pattern[i][0]) + " " + str(horizontal_pattern[i][1]) + "\n"
            writeData("data.txt", data)
    if(horizontal_pattern.__len__()>400):
        for i in range(0, 359):
            data = ""
            data = data + str(test_freq) + " " + "0 "+ str(horizontal_pattern[i][0]) + " " + str(horizontal_pattern[i][1]) + "\n"
            writeData("data.txt", data)
        len = horizontal_pattern.__len__()
        for i in range(360, len):
            data = ""
            data = data + str(test_freq) + " " + "1 "+ str(horizontal_pattern[i][0]) + " " + str(horizontal_pattern[i][1]) + "\n"
            writeData("data.txt", data)

# 遍历文件夹
import tqdm            
### 遍历文件夹，添加进度条

for filename in tqdm.tqdm(os.listdir(folder_path)):
    file_path = filename
    # 检查这个路径是否确实是一个文件
    if os.path.isfile(file_path):
        # 打印文件路径
        getData(file_path)