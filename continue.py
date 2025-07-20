import os
import subprocess
from tqdm import tqdm

target_dir = os.path.expanduser("~/my-path")
file_list_path = os.path.expanduser("~/selected_10k.txt")

def load_files():
    with open(file_list_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def copy_file(gs_path):
    filename = os.path.basename(gs_path)
    dst_path = os.path.join(target_dir, filename)

    if os.path.exists(dst_path):
        return "skip", gs_path

    cmd = ["gsutil", "cp", gs_path, dst_path]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return "success", gs_path
    except subprocess.CalledProcessError:
        return "fail", gs_path

def main():
    all_files = load_files()
    retry_fail = []

    for file in tqdm(all_files, desc="Resuming download"):
        status, path = copy_file(file)
        if status == "fail":
            retry_fail.append(path)

    if retry_fail:
        with open(os.path.expanduser("~/logs/retry_failed.txt"), "w") as f:
            for path in retry_fail:
                f.write(path + "\n")

if __name__ == "__main__":
    main()
