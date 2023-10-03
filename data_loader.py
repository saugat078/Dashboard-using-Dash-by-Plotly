import pandas as pd
import requests
from io import StringIO

def load_data():
    url = "https://raw.githubusercontent.com/saugat078/files/main/mindfactory_updated%20-%20mindfactory_updated%20(1).csv"
    response = requests.get(url)
    df = pd.read_csv(StringIO(response.text))
    return df
