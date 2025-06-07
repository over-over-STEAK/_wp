def dict_to_string(d):
    def stringify(value):
        if isinstance(value, dict):
            return '{' + dict_to_string(value) + '}'
        return str(value)

    return ', '.join(f"{k}:{stringify(v)}" for k, v in d.items())

# 測試
print(dict_to_string({'a': 1, 'b': {'x': 10, 'y': 20}}))
# 輸出: a:1, b:{x:10, y:20}
