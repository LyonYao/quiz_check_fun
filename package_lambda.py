import os
import zipfile

def zipdir(path, ziph):
    # 遍历目录树
    for root, dirs, files in os.walk(path):
        for file in files:
            # 排除__pycache__
            if '__pycache__' not in root:
                full_path = os.path.join(root, file)
                arcname = os.path.basename(os.path.dirname(full_path))+'/'+file
                print(f"Adding {full_path} as {arcname}")
                ziph.write(full_path, arcname)

if __name__ == "__main__":
    with zipfile.ZipFile('activity.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        directories = ["lambda/activity", "lambda/comm", "lambda/subject", "lambda/checker"]
        for directory in directories:
            zipdir(directory, zipf)