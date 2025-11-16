import json

# Read JSON data from file
with open('models/models.json', 'r') as file:
    models_data = json.load(file)

with open('models/voices.json', 'r') as file:
    voices_data = json.load(file)

# Extract active model IDs
active_models = [model for model in models_data.get("data") if model.get("active")]
text_models = [model.get("id") for model in active_models if model.get("type") is None]
tts_models = [model.get("id") for model in active_models if model.get("type") == "tts"]
stt_models = [model.get("id") for model in active_models if model.get("type") == "stt"]

def get_owner(model_id):
    for model in models_data.get("data"):
        if model.get("id") == model_id:
            return model["owned_by"]
    return None

def get_voices(model_id):
    return voices_data.get(model_id)
