
import shutil
import os
import sys
from pathlib import Path
import requests

def main():
    dist_path = Path("dist").resolve()
    dist_path.mkdir(exist_ok=True)
    url1="https://releases.linaro.org/components/toolchain/binaries/latest-7/aarch64-linux-gnu/gcc-linaro-7.5.0-2019.12-x86_64_aarch64-linux-gnu.tar.xz"
    filename=url1[url1.rindex('/')+1:]+".new"
    download(url1, str(dist_path/filename))



def download(url:str, file_path:str)->None:
    res = requests.get(url, stream=True)
    chunk_size = 4096
    total_chunk = int(res.headers.get('content-length'))/chunk_size
    chunk_num=0
    with open(file_path, "wb") as f:
        for chunk in res.iter_content(chunk_size=chunk_size):
            show_progress(100*chunk_num/total_chunk, "downloading:")
            chunk_num+=1
            if chunk:
                f.write(chunk)

def show_progress(i: int, prefix: str = "progress:"):
    i = int(i)
    print("{} {}%: ".format(prefix, i), "▋" * (i // 2), end="\r")
    sys.stdout.flush()

if __name__ == "__main__":
    main()

