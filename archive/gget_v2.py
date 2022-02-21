# Packages for gget
import pandas as pd
import mysql.connector as sql
import time

# Packages for ftpget
from bs4 import BeautifulSoup
import requests
import re
import numpy as np

def gget(searchwords, species, limit=None):
    """
    Function to query Ensembl for genes based on species and free form search terms. 
    
    Parameters:
    - searchwords
    The parameter "searchwords" is a list of one or more strings containing free form search terms 
    (e.g.searchwords = ["GABA", "gamma-aminobutyric acid"]).
    All results that contain at least one of the search terms are returned.
    The search is not case-sensitive.
    
    - species
    Possible entries for species are:
    "homo_sapiens" (or "human")
    "mus_musculus" (or "mouse")
    "taeniopygia_guttata" (or "zebra finch")
    "caenorhabditis_elegans" (or "roundworm")
    Note: If you would like to access results from a different species, or restrain your results to a certain mouse strain, 
    you can instead enter the core database as the "species" variable (e.g. species = "rattus_norvegicus_core_105_72").
    You can find all availabale species databases here: http://ftp.ensembl.org/pub/release-105/mysql/
    
    - limit
    "Limit" limits the number of search results to the top {limit} genes found.
    
    Returns a data frame with the query results.
    """
    start_time = time.time()
    
    if species == "caenorhabditis_elegans" or species == "roundworm":
        db = "caenorhabditis_elegans_core_105_269"   
    elif species == "homo_sapiens" or species == "human":
        db = "homo_sapiens_core_105_38"
    elif species == "mus_musculus" or species == "mouse":
        db = "mus_musculus_core_105_39"
    elif species == "taeniopygia_guttata" or species == "zebra finch":
        db = "taeniopygia_guttata_core_105_12"
    else: 
        db = species
        
    print(f"Results fetched from database: {db}")

    db_connection = sql.connect(host='ensembldb.ensembl.org', 
                                database=db, 
                                user='anonymous', 
                                password='')
    
    # If single searchword passed as string, convert to list
    if type(searchwords) == str:
        searchwords = [searchwords]
        
    # For human and mouse, the gene name is saved in gene_attrib.value where gene_attrib.attrib_type_id = 4
    if db == "homo_sapiens_core_105_38" or db == "mus_musculus_core_105_39":
        for i, searchword in enumerate(searchwords):
            # If limit is specified, fetch only the first {limit} genes for which the searchword appears in the description
            if limit != None:
                query = f"""
                SELECT gene.stable_id, gene_attrib.value, gene.description, xref.description, gene.biotype
                FROM gene
                LEFT JOIN xref ON gene.display_xref_id = xref.xref_id
                LEFT JOIN gene_attrib ON gene.gene_id = gene_attrib.gene_id
                WHERE (gene_attrib.attrib_type_id = 4) 
                AND (gene_attrib.value LIKE '%{searchword}%' OR 
                gene.description LIKE '%{searchword}%' OR 
                xref.description LIKE '%{searchword}%')
                LIMIT {limit}
                """
            # Else, fetch all genes for which the searchword appears in the description
            else:
                query = f"""
                SELECT gene.stable_id, gene_attrib.value, gene.description, xref.description, gene.biotype
                FROM gene
                LEFT JOIN xref ON gene.display_xref_id = xref.xref_id
                LEFT JOIN gene_attrib ON gene.gene_id = gene_attrib.gene_id
                WHERE (gene_attrib.attrib_type_id = 4) 
                AND (gene_attrib.value LIKE '%{searchword}%' OR 
                gene.description LIKE '%{searchword}%' OR 
                xref.description LIKE '%{searchword}%')
                """

            # Fetch the search results form the host using the specified query
            df_temp = pd.read_sql(query, con=db_connection)
            # Order by ENSEMBL ID (I am using pandas for this instead of SQL to increase speed)
            df_temp = df_temp.sort_values("stable_id").reset_index(drop=True)

            # In the first iteration, make the search results equal to the master data frame
            if i == 0:
                df = df_temp.copy()
            # Add new search results to master data frame
            else:
                df = pd.concat([df, df_temp])

        # Rename columns
        df = df.rename(columns={"stable_id": "Ensembl_ID", 
                                "value": "Gene_name",
                                "biotype": "Biotype"})
        # Changing description columns name by column index since they were returned with the same name ("description")
        df.columns.values[2] = "Ensembl_description"
        df.columns.values[3] = "Ext_ref_description"
        
    # For other species, the gene name will not be fetched      
    else: 
        for i, searchword in enumerate(searchwords):
            # If limit is specified, fetch only the first {limit} genes for which the searchword appears in the description
            if limit != None:
                query = f"""
                SELECT gene.stable_id, gene.description, xref.description, gene.biotype
                FROM gene
                LEFT JOIN xref ON gene.display_xref_id = xref.xref_id
                WHERE (gene.description LIKE '%{searchword}%' OR xref.description LIKE '%{searchword}%')
                LIMIT {limit}
                """
            # Else, fetch all genes for which the searchword appears in the description
            else:
                query = f"""
                SELECT gene.stable_id, gene.description, xref.description, gene.biotype
                FROM gene
                LEFT JOIN xref ON gene.display_xref_id = xref.xref_id
                WHERE (gene.description LIKE '%{searchword}%' OR xref.description LIKE '%{searchword}%')
                """

            # Fetch the search results form the host using the specified query
            df_temp = pd.read_sql(query, con=db_connection)
            # Order by ENSEMBL ID (I am using pandas for this instead of SQL to increase speed)
            df_temp = df_temp.sort_values("stable_id").reset_index(drop=True)

            # In the first iteration, make the search results equal to the master data frame
            if i == 0:
                df = df_temp.copy()
            # Add new search results to master data frame
            else:
                df = pd.concat([df, df_temp])

        # Rename columns
        df = df.rename(columns={"stable_id": "Ensembl_ID", 
                                "biotype": "Biotype"})
        # Changing description columns name by column index since they were returned with the same name ("description")
        df.columns.values[1] = "Ensembl_description"
        df.columns.values[2] = "Ext_ref_description"
    
    # Add URL to gene summary on Ensembl
    df["URL"] = "https://uswest.ensembl.org/" + "_".join(db.split("_")[:2]) + "/Gene/Summary?g=" + df["Ensembl_ID"]
    
    # Remove any duplicate search results from the master data frame and reset the index
    df = df.drop_duplicates().reset_index(drop=True)
    
    print(f"Query time: {round(time.time() - start_time, 2)} seconds")
    print(f"Genes fetched: {len(df)}")
    
    return df

def ftpget(species, return_val="json", release="latest"):
    """
    Function to fetch GTF and FASTA (cDNA and DNA) files from the Ensemble FTP site.
    
    Parameters:
    - species
    Defines the species for which the files should be fetched in the format "<genus>_<species>", 
    e.g.species = "homo_sapiens".
    - return_val
    Defines which results to return. Possible entries are:
    "json" - Returns all links in a json/dictionary format (default).
    "gtf" - Returns the GTF FTP link as a string.
    "cdna" - Returns the cDNA FTP link as a string.
    "dna" - Returns the DNA FTP link as a string.
    
    - release
    Defines the Ensembl release number from which the files are fetched, e.g. release = 104.
    (Ensembl releases < 48 are not suupported.)
    By default, the latest Ensembl release is used.
    """

    # Find latest Ensembl release
    url = "http://ftp.ensembl.org/pub/"
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    # Find all releases
    releases = soup.body.findAll(text=re.compile("release-"))
    # Get release numbers
    rels = []
    for rel in releases:
        rels.append(rel.split("/")[0].split("-")[-1])

    # Find highest release number (= latest release)
    ENS_rel = np.array(rels).astype(int).max()
        
    # If release != "latest", use user-defined Ensembl release    
    if release != "latest":
        if release > ENS_rel:
            raise ValueError("Defined Ensembl release number cannot be greater than latest release.")
        else:
            ENS_rel = release
    
    # Get GTF link for this species and release
    url = f"http://ftp.ensembl.org/pub/release-{ENS_rel}/gtf/{species}/"
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    
    nones = []
    a_elements = []
    pre = soup.find('pre')
    for element in pre.descendants:
        if element.name == "a":
            a_elements.append(element)
        elif element.name != "a":
            nones.append(element)
    
    for i, string in enumerate(a_elements):
        if f"{ENS_rel}.gtf.gz" in string.text:
            gtf_str = string
            
    gtf_url = f"http://ftp.ensembl.org/pub/release-{ENS_rel}/gtf/{species}/{gtf_str['href']}"
            
    
    # Get release date and time of this GTF link
    for i, string in enumerate(nones):
        if f"{ENS_rel}.gtf.gz" in string.text:
            gtf_date_size = nones[i+1]
            
    gtf_date = gtf_date_size.strip().split("  ")[0]
    gtf_size = gtf_date_size.strip().split("  ")[-1]

    # Get cDNA FASTA link for this species and release
    url = f"http://ftp.ensembl.org/pub/release-{ENS_rel}/fasta/{species}/cdna"
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    
    nones = []
    a_elements = []
    pre = soup.find('pre')
    for element in pre.descendants:
        if element.name == "a":
            a_elements.append(element)
        elif element.name != "a":
            nones.append(element)
            
    for i, string in enumerate(a_elements):
        if "cdna.all.fa" in string.text:
            cdna_str = string
            
    cdna_url = f"http://ftp.ensembl.org/pub/release-{ENS_rel}/fasta/{species}/cdna/{cdna_str['href']}"
    
    # Get release date
    for i, string in enumerate(nones):
        if "cdna.all.fa" in string.text:
            cdna_date_size = nones[i+1]
            
    cdna_date = cdna_date_size.strip().split("  ")[0]
    cdna_size = cdna_date_size.strip().split("  ")[-1]
    
    # Get DNA FASTA link for this species and release
    url = f"http://ftp.ensembl.org/pub/release-{ENS_rel}/fasta/{species}/dna"
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    
    nones = []
    a_elements = []
    pre = soup.find('pre')
    for element in pre.descendants:
        if element.name == "a":
            a_elements.append(element)
        elif element.name != "a":
            nones.append(element)

    # Get primary assembly if available, otherwise toplevel assembly
    dna_str = None
    for string in a_elements:
        if ".dna.primary_assembly.fa" in string.text:
            dna_str = string
            dna_search = ".dna.primary_assembly.fa"
            
    if dna_str == None:
        for string in a_elements:
            if ".dna.toplevel.fa" in string.text:
                dna_str = string
                dna_search = ".dna.toplevel.fa"
        
    dna_url = f"http://ftp.ensembl.org/pub/release-{ENS_rel}/fasta/{species}/dna/{dna_str['href']}"
    
    # Get release date          
    for i, string in enumerate(nones):
        if dna_search in string.text:
            dna_date_size = nones[i+1]  
      
    dna_date = dna_date_size.strip().split("  ")[0]
    dna_size = dna_date_size.strip().split("  ")[-1]
    
    # Return results    
    if return_val == "json":
        return {
            species: {
                "transcriptome": {
                    "ftp":cdna_url,
                    "ensembl_release": ENS_rel,
                    "release_date": cdna_date.split(" ")[0],
                    "release_time": cdna_date.split(" ")[1],
                    "bytes": cdna_size
                },
                "genome": {
                    "ftp":dna_url,
                    "ensembl_release": ENS_rel,
                    "release_date": dna_date.split(" ")[0],
                    "release_time": dna_date.split(" ")[1],
                    "bytes": dna_size
                },
                "annotation": {
                    "ftp":gtf_url,
                    "ensembl_release": ENS_rel,
                    "release_date": gtf_date.split(" ")[0],
                    "release_time": gtf_date.split(" ")[1],
                    "bytes": gtf_size
                }
            }
        }
    
    elif return_val == "gtf":
        print(f"Fetching from Ensembl release: {ENS_rel}")
        print(f"GTF release date and time: {gtf_date}")
        return gtf_url
        
    elif return_val == "cdna":
        print(f"Fetching from Ensembl release: {ENS_rel}")
        print(f"Transcriptome release date and time: {cdna_date}")
        return cdna_url
    
    elif return_val == "dna":
        print(f"Fetching from Ensembl release: {ENS_rel}")
        print(f"Genome release date and time:{dna_date}")
        return dna_url
    
    else:
        raise ValueError("Parameter return_val must be one of the following: 'json', 'gtf', 'cdna', 'dna'.")
    