from openai.gpt import GPT


models = {
    "gpt-4": GPT(version="gpt-4-turbo"),
    "gpt-3": GPT(version="gpt-3.5"),
}
