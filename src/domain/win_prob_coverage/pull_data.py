import requests
import polars as pl

import src.constants as c

r = requests.get(
    'https://api.collegefootballdata.com/games',
    params={
        'year': 2024,
        'team': 'BYU',
    },
    headers={'Authorization' : f'Bearer {c.CFBD_API_KEY}'},
)

data = r.json()
df = pl.from_dicts(data)

r = requests.get(
    'https://api.collegefootballdata.com/metrics/wp',
    params={
        'gameId': 401634765,
    },
    headers={'Authorization' : f'Bearer {c.CFBD_API_KEY}'},
)

data = r.json()
df = pl.from_dicts(data)

df.write_parquet('data/win_prob_coverage/byu_smu_plays.parquet')


def pull_data(endpoint, **params):
    r = requests.get(
        c.CFBD_URL + '/' + endpoint,
        params=params,
        headers={'Authorization' : f'Bearer {c.CFBD_API_KEY}'},
    )

    data = r.json()
    df = pl.from_dicts(data)
    df.write_parquet(c.BASE_PATH / endpoint)

