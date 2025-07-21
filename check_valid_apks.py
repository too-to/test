import os
import zipfile

from tqdm import tqdm

def is_valid_apk(apk_path):
    return zipfile.is_zipfile(apk_path)

def scan_apk_directory(directory):
    invalid_apks = []
    total_apks = 0

    for root, _, files in os.walk(directory):
        apk_files = [f for f in files if f.endswith(".apk")]
        for file in tqdm(apk_files, desc=f"Scanning {root}"):
            apk_path = os.path.join(root, file)
            total_apks += 1
            if not is_valid_apk(apk_path):
                invalid_apks.append(apk_path)

    print(f"\n검사 완료: 총 {total_apks}개 중 {len(invalid_apks)}개가 손상됨.")
    return invalid_apks

def save_invalid_apks(invalid_apks, output_file="invalid_apks.txt"):
    with open(output_file, "w") as f:
        for path in invalid_apks:
            f.write(path + "\n")
    print(f"손상된 APK 목록이 {output_file}에 저장됨.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="APK 유효성 검사 스크립트")
    parser.add_argument("apk_directory", help="APK 파일들이 위치한 디렉토리")
    parser.add_argument("--output", default="invalid_apks.txt", help="결과 저장 파일 이름")

    args = parser.parse_args()

    bad_apks = scan_apk_directory(args.apk_directory)
    save_invalid_apks(bad_apks, args.output)
