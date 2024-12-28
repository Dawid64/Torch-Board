import os

def wipe_dir(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            wipe_dir(os.path.join(root, dir))
            
def transform_history_dict(history):
    if len(history) == 0:
        return {}
    keys = set(history[0].keys())
    for change in history[1:]:
        keys = keys.union(set(change.keys()))
    changes = {key: [item[key] for item in history if key in item] for key in keys}
    return changes