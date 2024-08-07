import openai

with open('hidden.txt') as file:
    openai.api_key = file.read().strip()

def get_api_response(prompt: str) -> str | None:
    text: str | None = None

    try:
        response = dict = openai.Completion.create(
            engine="davinci-002",
            prompt=prompt,
            temperature=0.9,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[' Human:', ' AI:']
        )

        choices: dict = response.get("choices")[0]
        text = choices.get("text")

    except Exception as e:
        print('ERROR:', e)
    return text

def update_list(message: str, pl: list[str]):
    pl.append(message)

def create_prompt(message: str, pl: list[str]) -> str:
    p_message = str = f"\nHuman: {message}"
    update_list(p_message, pl)
    prompt: str = ''.join(pl)
    return prompt

def get_response(message: str, pl: list[str]) -> str:
    prompt: str = create_prompt(message, pl)
    bot_response: str = get_api_response(prompt)

    if bot_response:
        update_list(bot_response, pl)
        pos: int = bot_response.find('\nAI:')
        bot_response = bot_response[pos + 5:]

    else:
        bot_response = "Something went wrong... Please try again."

    return bot_response

def main():
    prompt_list: list[str] = ['You will pretend to be a figh dude that ends every response with "ye"',
    '\nHuman: what time is it?',
    '\nAI: It is 12:30, ye']

    while True:
        user_input: str = input("You: ")
        response: str = get_response(user_input, prompt_list)
        print(f"Bot: {response}")

if __name__ == "__main__":
    main()
