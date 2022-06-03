from collections import OrderedDict

def read_motus2_lin(ifile_path, drop_zeros=False, replace_unknown=False):
    from pandas import read_csv
    df = read_csv(
        ifile_path,
        sep="\t",
        skiprows=2
    )
    # remove zero counts
    if drop_zeros:
        df = df.loc[df.iloc[:,3] > 0]
    # replace -1/NA by "Unknown" 
    if replace_unknown:
        df.loc[df["#mOTU"] == "-1","#mOTU"] = "Unknown"
        df.loc[df["consensus_taxonomy"] == "-1","consensus_taxonomy"] = "Unknown"
        df.loc[df["NCBI_tax_id"] == "NA","NCBI_tax_id"] = "Unknown"
    return df

def read_metaphlan3_rel_ab_w_read_stats(ifile_path, rank=None, replace_unknown=False):
    import re
    from pandas import read_csv
    df = read_csv(
        ifile_path,
        sep="\t",
        skiprows=4
    )
    # filter by rank
    if rank is not None:
        df = df.loc[df["#clade_name"].str.contains('\|%s__|^UNKNOWN' % rank)]
    # replace -1/UNKNOWN by "Unknown"
    if replace_unknown:
        df.loc[df["#clade_name"] == "UNKNOWN","#clade_name"] = "Unknown"
        df.loc[df["clade_taxid"] == "UNKNOWN","clade_taxid"] = "Unknown"
    return df

def read_kraken2_report2biom2tsv(ifile_path):
    import re
    from pandas import read_csv
    df = read_csv(
        ifile_path,
        sep="\t",
        comment='#',
        names=["taxid", "count", "lineage"]
    )
    # tax ID: to string
    df["taxid"] = df["taxid"].apply(lambda x: "taxid_%d" % int(x))
    # lineage: add "Unknown" if no taxon name and replace separator
    df["lineage"] = df["lineage"].apply(lambda x: re.sub("__(;|$)", "__Unknown;", x))
    df["lineage"] = df["lineage"].apply(lambda x: re.sub(";\s*", "|", re.sub(";$", "", x)))
    # lineage: put genus and species strings together
    df["lineage"] = df["lineage"].apply(lambda x: lineage_cat_ranks(lin=x, r1="g", r2="s"))
    return df

def parse_kraken2_labels(ifile_path):
    # https://github.com/DerrickWood/kraken2/wiki/Manual#standard-kraken-output-format
    #   "C"/"U": a one letter code indicating that the sequence was either classified or unclassified.
    #   The sequence ID, obtained from the FASTA/FASTQ header.
    #   The taxonomy ID Kraken 2 used to label the sequence; this is 0 if the sequence is unclassified.
    #   The length of the sequence in bp.
    #   A space-delimited list indicating the LCA mapping of each k-mer in the sequence(s).
    import re
    import pandas
    columns=["class_flag", "seq_id", "taxon", "seq_length", "matches"]
    df = pandas.read_csv(ifile_path, sep="\t", header=None, names=columns)
    df = df.assign(tax_name=df["taxon"].apply(lambda x: re.search("(?P<tname>^.*) \(taxid (?P<tid>[0-9]+)\)$", x).group("tname")))
    df = df.assign(tax_id=df["taxon"].apply(lambda x: re.search("(?P<tname>^.*) \(taxid (?P<tid>[0-9]+)\)$", x).group("tid")))
    df.drop(columns=["matches", "taxon"], inplace=True)
    df.set_index(["seq_id"], drop=True, inplace=True, verify_integrity=True)
    return df

def lineage_cat_ranks(lin, r1="g", r2="s"):
    # to concat taxon names from different ranks, e.g. genus + species
    # lin: unprocessed lineage string: <rank>_<name>, separated by "|"
    import re
    lin   = lin.split("|")
    lin   = [re.search("(?P<rank>^[a-zA-Z])__(?P<taxon>.*$)", taxon).groups() for taxon in lin]
    lin_d = dict(lin)
    if lin_d[r2] and lin_d[r2] != "Unknown":
        lin_d[r2] = lin_d[r1] + " " + lin_d[r2]
    return "|".join([t[0] + "__" + lin_d[t[0]] for t in lin])

def lineage2dict(lin):
    import re
    if lin == "Unknown":
        return dict([(k, "Unknown") for k in RANKS.keys()])
    lin = lin.split("|")
    lin = [re.search("(?P<rank>^[a-zA-Z])__(?P<taxon>.*$)", taxon).groups() for taxon in lin]
    lin = dict(lin)
    return lin

RANKS = OrderedDict({'k': 'kingdom', 'p': 'phylum', 'c': 'class', 'o': 'order', 'f': 'family', 'g': 'genus', 's': 'species'})

def parse_prodigal_faa_headers(ifile_path):
    import re
    from pandas import DataFrame
    genes = []
    with open(ifile_path) as ifile:
        for line in ifile:
            if not re.match(">", line):
                continue
            line = re.sub("^>", "", line.strip())
            pid, pstart, pend, pstrand, pinfo = line.split(" # ")
            genes.append({
                "prot_id": pid,
                "contig_id": "_".join(pid.split("_")[:-1]),
                "start": int(pstart),
                "end": int(pend),
                "strand": pstrand,
                "info": pinfo
            })
    genes = DataFrame(genes)
    genes.set_index(["prot_id"], drop=True, inplace=True, verify_integrity=True)
    assert (genes.start < genes.end).all()
    return genes

def parse_hmmer_tbl(ifile_path):
    import re
    import pandas
    header = [
        "target", "tacc", "query", "qacc",
        "evalue_fs", "score_fs", "bias_fs",
        "evalue_b1d", "score_b1d", "bias_b1d",
        "exp", "reg", "clu", "ov", "env", "dom", "rep", "inc",
        # "target_descr"
    ]
    hits = []
    with open(ifile_path, "r") as ifile:
        for line in ifile:
            if not re.match("#", line):
                line = re.sub("\s+", "\t", line.strip()).split("\t")[0:18]
                hits.append(pandas.Series(data=line, index=header))
    if len(hits) == 0:
        hits = None
    else:
        hits = pandas.concat(hits, axis=1).transpose()
        hits.set_index(["target"], drop=True, inplace=True, verify_integrity=True)
        hits.drop(columns=["tacc", "qacc"], inplace=True)
    return hits

