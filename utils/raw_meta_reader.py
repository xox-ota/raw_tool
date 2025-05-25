import os.path
import pdb
import subprocess
import glob
import tqdm


def get_metadata(file_path):
    # 定义 Exiv2 命令
    command = ['exiv2', "-pt", file_path]

    # 执行命令并捕获输出
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return {}

    # 将输出分割成行
    lines = result.stdout.splitlines()

    # 创建一个字典来存储元数据
    metadata = {}

    # 遍历每一行，使用正则表达式提取键和值
    for line in lines:
        value = line.strip().split("  ")[-1]
        if "Exif.Photo.ExposureTime" in line:
            # '1/160 s'
            # metadata["ExposureTime"] = value.replace("/", "_").replace(" ", "")
            metadata["ExposureTime"] = value
        elif "Exif.Photo.FNumber" in line:
            metadata["FNumber"] = value
        elif "Exif.Photo.ISOSpeedRatings" in line:
            metadata["ISO"] = value
        elif "Exif.Photo.FocalLength" in line:
            metadata["FocalLength"] = value.replace(" ", "").replace(".0", "")
        elif "Exif.Photo.LensModel" in line:
            metadata["LensModel"] = value
        elif "Exif.Image.DateTime" in line:
            metadata["DateTime"] = value.replace(":", "").replace(" ", "_")
        elif "Exif.Image.Model" in line:
            metadata["Model"] = value.replace(":", "").replace(" ", "_")
        elif "FullImageSize" in line:
            # 9504 x 6336
            metadata["FullImageSize"] = value

            tmp = value.split(" ")
            pixel = int(tmp[0]) * int(tmp[2]) / 10000
            metadata["pixel"] = pixel


        elif "Exif.Photo.DateTimeOriginal" in line:
            # '2024:11:29 19:16:34'
            tmp = value.split(" ")
            date_str = tmp[0].replace(":", "-") + " " + tmp[1]
            metadata["DateTimeOriginal"] = date_str

        else:
            pass
            # print(line)

    return metadata


def do_rename(file_path, m):
    origin_name = file_path.split("/")[-1].split(".")[0]
    if 'ISO' in origin_name:
        origin_name = ""
    else:
        origin_name = " " + origin_name

    suffix = file_path.split(".")[-1]

    exposure = m.get('ExposureTime', '').replace("/", "_")

    if suffix == "DNG":
        new_name = f"{m['DateTime']} {m['FNumber']} {exposure} ISO{m['ISO']}.{suffix}"
    else:
        new_name = f"{m['DateTime']} {m['FNumber']} {exposure} ISO{m['ISO']} {m['FocalLength']} {m['LensModel']} {m['Model']}{origin_name}.{suffix}"
    new_fp = os.path.join(os.path.dirname(file_path), new_name)
    # print(new_fp)
    os.rename(file_path, new_fp)


if __name__ == "__main__":
    img_fp = "/Users/my/Desktop/X.ARW"
    out = get_metadata(img_fp)
    print(out)
    # out = {'Model': 'ILCE-7CR',
    #        'DateTime': '20241129_191634',
    #        'ExposureTime': '1/500 s',
    #        'FNumber': 'F1.4',
    #        'ISO': '125',
    #        'DateTimeOriginal': '2024-11-29 19:16:34', 'FocalLength': '50mm',
    #        'FullImageSize': '9504 x 6336', 'pixel': 6021.7344, 'LensModel': 'FE 50mm F1.4 GM'}
