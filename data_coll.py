import requests
import re
import os
# Import your settings from config.py
import config 

# Use os to create the directory from config
if not os.path.exists(config.OUTPUT_DIR):
    os.makedirs(config.OUTPUT_DIR)

def collect_dataset(query, filename_prefix, is_positive=True):
    url = "https://rest.uniprot.org/uniprotkb/search"
    params = {
        "query": query,
        "format": "json",
        "size": 500,
        "fields": "accession,id,sequence,ft_signal"
    }

    # Use os.path.join with the directory from config
    tsv_path = os.path.join(config.OUTPUT_DIR, f"{filename_prefix}.tsv")
    fasta_path = os.path.join(config.OUTPUT_DIR, f"{filename_prefix}.fasta")

    print(f"--- Downloading to {config.OUTPUT_DIR} ---")

    with open(tsv_path, "w") as tsv, open(fasta_path, "w") as fasta:
        tsv.write("Accession\tEntryName\tSP_Start\tSP_End\tSequence\n")
        
        current_url = url
        count = 0
        while current_url:
            response = requests.get(current_url, params=params if current_url == url else None)
            response.raise_for_status()
            results = response.json().get("results", [])

            for entry in results:
                acc = entry['primaryAccession']
                name = entry['uniProtkbId']
                seq = entry['sequence']['value']
                
                if is_positive:
                    signals = [f for f in entry.get('features', []) if f['type'] == 'Signal']
                    if not signals: continue
                    f = signals[0]
                    start, end = f['location']['start']['value'], f['location']['end']['value']
                    if not isinstance(start, int) or not isinstance(end, int):
                        continue

                    if (end - start + 1) < 14:
                        continue
                                        
                    tsv.write(f"{acc}\t{name}\t{start}\t{end}\t{seq}\n")
                else:
                    tsv.write(f"{acc}\t{name}\t\t\t{seq}\n")
                
                fasta.write(f">{acc}|{name}\n{seq}\n")
                count += 1

            link_header = response.headers.get("Link")
            if link_header and 'rel="next"' in link_header:
                current_url = re.search(r'<(.*)>; rel="next"', link_header).group(1)
            else:
                current_url = None
    
    print(f"Success! {count} entries saved.")

# --- Execution using Config constants ---
collect_dataset(config.QUERY_POSITIVE, "positive_data", is_positive=True)
collect_dataset(config.QUERY_NEGATIVE, "negative_data", is_positive=False)