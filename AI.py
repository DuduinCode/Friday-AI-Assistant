def aiProcess(command):
    chat_session = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    ).start_chat(history=[])
    
    response = chat_session.send_message(command)
    return response.text
