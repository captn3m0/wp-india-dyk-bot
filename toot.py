from mastodon import Mastodon
from DYK import DYK
import os

def get_toot():
    d = DYK().getRandomFact()
    return d['text'] + "\n" + d['url']

if __name__ == '__main__':
    mastodon = Mastodon(
        api_base_url = os.environ['MASTODON_API_BASE_URL'],
        access_token = os.environ['MASTODON_ACCESS_TOKEN']
    )
    mastodon.toot(get_toot())