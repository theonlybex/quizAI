import openai

def check_openai_api_key(api_key):
    client = openai.OpenAI(api_key=api_key)
    try:
        client.models.list()
    except openai.AuthenticationError:
        return False
    else:
        return True


OPENAI_API_KEY = "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"

if check_openai_api_key(OPENAI_API_KEY):
    print("Valid OpenAI API key.")
else:
    print("Invalid OpenAI API key.")
