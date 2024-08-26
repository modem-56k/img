import os
from PIL import Image
from PIL.ExifTags import TAGS

def get_date_taken(path):
    try:
        image = Image.open(path)
        exif_data = image._getexif()
        for tag, value in exif_data.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "DateTimeOriginal":
                # 格式化为 yyyymmdd_hhmmss
                return value.replace(':', '').replace(' ', '_')
    except Exception as e:
        print(f"Could not process {path}: {e}")
        return None

def rename_images(directory):
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.tif', '.tiff', '.heic')):
            filepath = os.path.join(directory, filename)
            date_taken = get_date_taken(filepath)
            if date_taken:
                new_filename = f"{date_taken}{os.path.splitext(filename)[1]}"
                new_filepath = os.path.join(directory, new_filename)
                os.rename(filepath, new_filepath)
                print(f"Renamed: {filename} -> {new_filename}")
            else:
                print(f"No date found for: {filename}, keeping original name.")

# 指定图片所在的目录
if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))  # 当前脚本所在的文件夹
    rename_images(directory)
