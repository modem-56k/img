import os
import re
import shutil
from datetime import datetime

# 匹配日期的正则表达式，支持多种日期格式
date_patterns = [
    r'(\d{4})[.-_]?(\d{2})[.-_]?(\d{2})',  # 2024-01-15, 2024.01.15, 20240115, 2024_0115
]

# 根据文件名提取日期信息
def extract_date_from_filename(filename):
    for pattern in date_patterns:
        match = re.search(pattern, filename)
        if match:
            year, month, day = match.groups()
            return year, month, day
    return None

# 移动照片到正确的文件夹
def move_photos_to_correct_folder(root_folder):
    moved_files = 0
    created_folders = 0

    for year_folder in os.listdir(root_folder):
        year_path = os.path.join(root_folder, year_folder)
        if os.path.isdir(year_path) and year_folder.isdigit():  # 确保是年份文件夹
            for month_folder in os.listdir(year_path):
                month_path = os.path.join(year_path, month_folder)
                if os.path.isdir(month_path) and month_folder.isdigit():  # 确保是月份文件夹
                    for day_folder in os.listdir(month_path):
                        day_path = os.path.join(month_path, day_folder)
                        if os.path.isdir(day_path) and day_folder.isdigit():  # 确保是日期文件夹
                            for filename in os.listdir(day_path):
                                file_path = os.path.join(day_path, filename)
                                if os.path.isfile(file_path):
                                    date_info = extract_date_from_filename(filename)
                                    if date_info:
                                        correct_year, correct_month, correct_day = date_info
                                        correct_folder = os.path.join(root_folder, correct_year, correct_month, correct_day)

                                        if correct_day != day_folder:  # 如果日期不匹配
                                            # 创建正确的文件夹（如果不存在）
                                            if not os.path.exists(correct_folder):
                                                os.makedirs(correct_folder)
                                                created_folders += 1
                                            
                                            # 移动文件到正确的文件夹
                                            shutil.move(file_path, os.path.join(correct_folder, filename))
                                            moved_files += 1
    
    return moved_files, created_folders

if __name__ == "__main__":
    root_folder = os.path.abspath(os.path.dirname(__file__))  # 获取脚本所在的根目录
    moved_files, created_folders = move_photos_to_correct_folder(root_folder)

    print(f"移动了 {moved_files} 个文件， 新建了 {created_folders} 个文件夹。")
