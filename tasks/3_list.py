def get_by_path(data, path):
    cur = data
    for key in path.split("."):
        if isinstance(cur, list):
            key = int(key)
        cur = cur[key]
    return cur


data = {
    "a": {
        "b": {
            "c": "+++"
        }
    }
}

print(get_by_path(data, "a.b.c"))
