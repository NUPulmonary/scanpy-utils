

def clean_metadata(ds):
    x = ds.var.loc[:, ds.var.columns[ds.var.columns.str.match("gene_ids-\d+")]]
    cols = x.T.notna().idxmax()
    x = x.reset_index().melt("index")
    ds.var.insert(
        0,
        "gene_ids",
        x.set_index(["index", "variable"]).loc[zip(cols.index, cols.values), :].droplevel("variable")
    )
    ds.var.drop(ds.var.columns[ds.var.columns.str.match("gene_ids-\d+")], inplace=True, axis=1)
    ds.var.insert(1, "feature_types", "Gene Expression")
    ds.var.drop(ds.var.columns[ds.var.columns.str.match("feature_types-\d+")], inplace=True, axis=1)
    x = ds.var.loc[:, ds.var.columns[ds.var.columns.str.match("genome-\d+")]]
    cols = x.T.notna().idxmax()
    x = x.reset_index().melt("index")
    ds.var.insert(
        2,
        "genome",
        x.set_index(["index", "variable"]).loc[zip(cols.index, cols.values), :].droplevel("variable")
    )
    ds.var.drop(ds.var.columns[ds.var.columns.str.match("genome-\d+")], inplace=True, axis=1)
