import json

def feature_key_from_state_string(str):
    return json.loads(str.replace('.figure', ''))['feature']
