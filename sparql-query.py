from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

endpoint = "https://query.knowledgepixels.com/repo/full"

query = """
PREFIX np: <http://www.nanopub.org/nschema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT
  ?np
  ?timepoint
  ?location
  ?sampletype
  ?nucseq
WHERE {

  ?np np:hasAssertion ?assertion .

  FILTER NOT EXISTS {
    ?np a <http://purl.org/nanopub/x/DraftNanopub> .
  }
  
  GRAPH ?assertion {

    ?assoc rdf:type
      <https://w3id.org/kpxl/biodiv/terms/OrganismToNucleotideSequenceAssociation> .

    ?taxonNode
      <https://w3id.org/kpxl/biodiv/terms/hasTaxonName>
      <https://www.checklistbank.org/dataset/2169/taxon/1998> .

    OPTIONAL {
      ?timeNode
        <https://w3id.org/biolink/vocab/timepoint>
        ?timepoint .
    }

    OPTIONAL {
      ?locNode
        <http://www.w3.org/2003/01/geo/wgs84_pos#location>
        ?location .
    }

    OPTIONAL {
      ?sampleNode
        <https://w3id.org/kpxl/biodiv/terms/hasSampleType>
        ?sampletype .
    }

    OPTIONAL {
      ?nucNode
        <https://w3id.org/biolink/vocab/object>
        ?nucseq .
    }
  }
}
"""

sparql = SPARQLWrapper(endpoint)
sparql.setQuery(query)
sparql.setReturnFormat(JSON)

results = sparql.query().convert()

rows = []

for result in results["results"]["bindings"]:
    rows.append({
        "np": result.get("np", {}).get("value"),
        "timepoint": result.get("timepoint", {}).get("value"),
        "location": result.get("location", {}).get("value"),
        "sampletype": result.get("sampletype", {}).get("value"),
        "nucseq": result.get("nucseq", {}).get("value"),
    })

df = pd.DataFrame(rows)
df.drop_duplicates(inplace=True, subset=["nucseq"])

df.to_csv("sparql-query.csv", index=False)