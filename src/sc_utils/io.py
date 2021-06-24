import gzip
import os

import pandas as pd
import scipy.io


def write_mtx(ds, output_dir):
    pd.DataFrame({
        0: ds.var.index,
        1: ds.var.index,
        2: "Gene Expression"
    }).to_csv(
        os.path.join(output_dir, "features.tsv.gz"),
        sep="\t",
        index=False,
        header=False
    )
    pd.DataFrame(ds.obs.index).to_csv(
        os.path.join(output_dir, "barcodes.tsv.gz"),
        sep="\t",
        index=False,
        header=False
    )
    with gzip.open(os.path.join(output_dir, "matrix.mtx.gz"), "wb") as f:
        scipy.io.mmwrite(f, ds.X.T)
