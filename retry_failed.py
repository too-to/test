import os
import subprocess
from tqdm import tqdm

error_log = os.path.expanduser("~/logs/error.txt")
success_log = os.path.expanduser("~/logs/success.txt")
target_dir = os.path.expanduser("~/my-path") # 경로 설정 

def load_failed():
    with open(error_log, "r") as f:
        return [line.strip() for line in f if line.strip()]

def copy_file(gs_path):
    filename = os.path.basename(gs_path)
    dst_path = os.path.join(target_dir, filename)

    if os.path.exists(dst_path):
        return "skip", gs_path

    cmd = ["gsutil", "cp", gs_path, dst_path]
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return "success", gs_path
    except subprocess.CalledProcessError:
        return "fail", gs_path

def append_log(filepath, paths):
    with open(filepath, "a") as f:
        for path in paths:
            f.write(path + "\n")

def main():
    failed_files = load_failed()
    retry_success = []
    retry_fail = []

    for file in tqdm(failed_files, desc="Retrying failed copies"):
        status, path = copy_file(file)
        if status == "success":
            retry_success.append(path)
        elif status == "fail":
            retry_fail.append(path)

    append_log(success_log, retry_success)
    with open(error_log, "w") as f:
        for path in retry_fail:
            f.write(path + "\n")

if __name__ == "__main__":
    main()
