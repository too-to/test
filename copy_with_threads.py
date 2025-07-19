import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

JOBS = 6
success_log = os.path.expanduser("~/logs/success.txt")
error_log = os.path.expanduser("~/logs/error.txt")
target_dir = os.path.expanduser("~/내-경로/")
file_list_path = "~/selected_10k.txt"

os.makedirs(os.path.dirname(success_log), exist_ok=True)
os.makedirs(target_dir, exist_ok=True)

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
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return "success", gs_path
    except subprocess.CalledProcessError:
        return "fail", gs_path

def log_results(results):
    with open(success_log, "w") as s_log, open(error_log, "w") as e_log:
        for status, path in results:
            if status == "success":
                s_log.write(path + "\n")
            elif status == "fail":
                e_log.write(path + "\n")

def main():
    files = load_files()
    results = []

    with ThreadPoolExecutor(max_workers=JOBS) as executor:
        futures = {executor.submit(copy_file, f): f for f in files}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Copying files"):
            result = future.result()
            results.append(result)

    log_results(results)

if __name__ == "__main__":
    main()
