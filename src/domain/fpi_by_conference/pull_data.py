import requests
import polars as pl

import src.constants as c

r = requests.get(
    'https://api.collegefootballdata.com/ratings/fpi',
    params={
        'year': 2024,
    },
    headers={'Authorization' : f'Bearer {c.CFBD_API_KEY}'},
)

data = r.json()
df = pl.from_dicts(data)
df.write_parquet('data/fpi_by_conference/2024_fpi.parquet')
