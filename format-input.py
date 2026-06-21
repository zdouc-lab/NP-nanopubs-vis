from sys import argv
import pandas as pd
import requests
from urllib.parse import quote

try:
    username = argv[1]
except IndexError as e:
    raise RuntimeError("No GeoNames username provided - aborting.") from e

def get_coord(geoname: int) -> tuple:
    """Query the GeoNames API for a Geoname ID to get latitude and longitude"""
    rsps_meta = requests.get(
        f"http://api.geonames.org/getJSON?geonameId={geoname}&username={username}"
    )
    rsps_meta.raise_for_status()
    data = rsps_meta.json()
    print(data)
    print(f"{data['lat']},{data['lng']}")
    return data['lat'], data['lng']


def get_envo_term(uri: str) -> str:
    """Query the EMBL-EBI Ontology Lookup Service for an ENVO term"""
    url = (
        "https://www.ebi.ac.uk/ols4/api/ontologies/envo/terms/"
        + quote(quote(uri, safe=""), safe="")
    )
    r = requests.get(url)
    r.raise_for_status()
    data_envo = r.json()
    print(data_envo["label"])
    return data_envo["label"]


df = pd.read_csv("sparql-query.csv")


df["nucseq_id"] = df["nucseq"].apply(lambda x: x.split("/")[-1])

coords = df["location"].apply(
    lambda x: get_coord(x.split("/")[-2].split("/")[-1])
)
df[["lat", "lng"]] = pd.DataFrame(coords.tolist(), index=df.index)

df["sampletype_label"] = df["sampletype"].apply(lambda x: get_envo_term(x))

df.to_csv("data_formatted.csv", index=False)