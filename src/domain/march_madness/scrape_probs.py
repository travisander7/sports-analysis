import requests
from bs4 import BeautifulSoup
import polars as pl
import re

# URL of the webpage containing the table
url = "https://kenpom.substack.com/p/2025-ncaa-tournament-probabilities"

# Send a GET request to the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the table element (you may need to inspect the webpage to find the correct element)
    table = soup.find_all("span")

    txt = soup.find_all('span')[3]

    # Extract the text content
    text_content = txt.get_text()

    # Split the text content into rows
    rows = text_content.strip().split('\n')

    # Split each row into columns
    data = []
    row = rows[0]
    row = rows[-1]
    for row in rows:
        seed = row[:4].strip()
        team = row[4:-42].strip()
        probs = row[-42:].split()
        data.append([seed, team] + probs)

    [len(i) for i in data]

    # Define the column names
    columns = ["Seed", "Team", "R64", "R32", "S16", "E8", "F4", "NCG"]

    # Create a Polars DataFrame
    df = pl.DataFrame(data=data, schema=columns, orient='row')

    # Optionally, save the DataFrame to a file
    df.write_parquet("tournament_probabilities.parquet")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
