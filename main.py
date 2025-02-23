import os.path

from utils import raw_meta_reader
import glob
import argparse
import tqdm

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default="/Users/cyy/Desktop/图片筛选")
    args = parser.parse_args()

    assert os.path.isdir(args.path) and os.path.exists(args.path), "无效文件夹路径"

    if not args.path.endswith("/"):
        args.path += "/"

    for fp in tqdm.tqdm(glob.glob(f"{args.path}**/*.ARW", recursive=True)):
        meta = raw_meta_reader.get_metadata(fp)
        raw_meta_reader.do_rename(fp, meta)
