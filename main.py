import os
import requests
import argparse
from dotenv import load_dotenv
from pathlib import Path  # python3 only

def is_bitlink(header, url):
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{url}',
        headers=header
    )

    return response.ok

    
def shorten_link(header, url):
    body = {
        'long_url' : url
    }
      
    response = requests.post(
        'https://api-ssl.bitly.com/v4/bitlinks',
        headers=header,
        json=body
    )
    response.raise_for_status()
    
    return response.json()['id']


def count_clicks(header, bitlink):
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary',
        headers=header
    )
    response.raise_for_status()

    return response.json()['total_clicks']


def main():
    parser = argparse.ArgumentParser(
        description='Эта программа из ссылки делает битлинк и считает кол-во кликов по битлинку'
    )
    parser.add_argument('url', help='Ваша ссылка или битлинк')
    args = parser.parse_args()

    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    token = os.environ['BITLY_TOKEN']
    header = {
        'Authorization' : f'Bearer {token}'
    }
    url = args.url

    if is_bitlink(header, url):
        print('Кол-во кликов по ссылке', count_clicks(header, url))
    else:
        print('Битлинк', shorten_link(header, url))
        
        
if __name__ == '__main__':
    main()
