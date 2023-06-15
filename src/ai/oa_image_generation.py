import openai

from config import SphinxConfig


def generate_image(key_word: str) -> str:
    openai.api_key = SphinxConfig.open_ai_key
    response = openai.Image.create(
        prompt=key_word,
        n=1,
        size="1024x1024"
    )

    return response['data'][0]['url']


if __name__ == '__main__':
    url = generate_image('a small cat')
    print(url)
