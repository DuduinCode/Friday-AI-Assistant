from openai import OpenAI
 
# pip install openai 
# if you saved the key under a different environment variable name, you can do something like:
AI= OpenAI(
  api_key="<your openai api key>",
)

completion = AI.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named friday skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": "what is coding"}
  ]
)

print(completion.choices[0].message.content)