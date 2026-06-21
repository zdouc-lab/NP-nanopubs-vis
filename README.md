# Nanopublications in Natural Product Research

This repo contains scripts to illustrate the application of nanopublications.

It consists of three scripts:

`sparql-query.py` runs a SPARQL query that extracts all nanopublication with the association `OrganismToNucleotideSequenceAssociation`.
It will filter `hasTaxonName` for the genus [*Planomonospora*](https://www.checklistbank.org/dataset/2169/taxon/1998) and extract several other associations.
This data will be dumped as `sparql-query.csv`.

`format-input.py` runs API calls to convert ontology terms to human-readable labels.

`create-figure.py` visualizes the data by plotting it onto a map.

# Step-by-step figure generation protocol
*assumes `uv` to be installed*

```commandline
uv sync
uv run python sparql-query.py
uv run python format-input.py <geonames username># performs api calls, costly
uv run python create-figure.py
```

This will create a static `map.svg` file and an interactive `map.html` file.

Open the interactive map with
```commandline
python -m http.server 8000
firefox http://localhost:8000/map.html # or any other browser
```