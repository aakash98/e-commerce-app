import json

def load_secrets_from_file(file_location=None):
    if not file_location:
        with open('secrets.json', 'r') as fp:
            secrets_data = json.load(fp)
            return secrets_data
    return {}
