import os
import sys
import warnings
import argparse
from pathlib import Path
import shutil

def get_args():
    parser = argparse.ArgumentParser(
        usage=
        f'python {os.path.basename(__file__)} -n <label names in .txt> <dataset dir1> <dataset dir2> ...',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'paths',
        default='./',
        nargs='+',
        metavar="DIR",
        help='input paths',
        type=str,
    )
    parser.add_argument(
        '-r',
        default=False,
        dest='recursive',
        action="store_true",
        help='recursive clear',
    )
    parser.add_argument(
        '-i',
        default=False,
        dest='interactive',
        action="store_true",
        help='interactive mode',
    )

    args = parser.parse_args()
    return args


def main():
    """
    CLean empty files, 清理空文件夹和空文件
    :param path: 文件路径，检查此文件路径下的子文件
    :return: None
    """
    args = get_args()
    for p in args.paths:
        path = Path(p)
        if args.recursive: 
            p = path.glob("**/*")
        else:
            p = path.iterdir()

        for file in p:
            if file.is_dir():
                print(f'Traversal at {file}')
                delete=False
                if 0 == len(os.listdir(file)):  # 如果子文件为空
                    if args.interactive:
                        if 'y' == input(f'! delete {file} ? y/n :'):
                           delete = True
                    else:
                        delete = True
                    if delete:
                        print(f"Deleting {file}")
                        os.rmdir(file)  # 删除这个空文件夹
        print (f'Dispose [{path}] over!')

if __name__ == "__main__":  # 执行本文件则执行下述代码
    main()
