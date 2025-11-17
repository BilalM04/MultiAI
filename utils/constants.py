from models.active_models import text_models, tts_models, stt_models, get_voices

default_text_model = text_models[0]
default_tts_model = tts_models[0]
default_stt_model = stt_models[0]
wikipedia_tool_name = "Wikipedia"
duckduckgo_tool_name = "DuckDuckGo"
default_search_tool = wikipedia_tool_name
search_tool_options = [wikipedia_tool_name, duckduckgo_tool_name]
chatbot_state = 0
searchbot_state = 1
voicebot_state = 2
fileqna_state = 3
account_state = 4
about_state = 5
rate_limit_message = "Rate limit reached for **{model}**. Please wait a moment and try again or try a different model."
generic_error_message = "An unexpected error occurred."
