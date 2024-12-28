import os

def wipe_dir(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            wipe_dir(os.path.join(root, dir))