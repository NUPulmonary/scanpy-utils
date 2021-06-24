import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scanpy as sc


def expr_colormap():
    cdict = {
        'red':   [
            (0.0, 220/256, 220/256),
            (0.5, 42/256, 42/256),
            (1.0, 6/256, 6/256)
        ],

        'green': [
            (0.0, 220/256, 220/256),
            (0.5, 145/256, 145/256),
            (1.0, 37/256, 27/256)
        ],

        'blue':  [
            (0.0, 220/256, 220/256),
            (0.5, 174/256, 174/256),
            (1.0, 170/256, 170/256)
        ]
    }
    return mpl.colors.LinearSegmentedColormap('testCmap', segmentdata=cdict, N=256)


def feature_plot(ds, feature, gridsize=(180, 70), linewidths=0.15, figsize=None):
    if feature in ds.obs.columns:
        values = ds.obs_vector(feature)
    else:
        values = ds.raw.obs_vector(feature)

    kwargs = {}
    if figsize is not None:
        kwargs["figsize"] = figsize
    fig, ax = plt.subplots(**kwargs)
    hb = ax.hexbin(
        ds.obsm["X_umap"][:, 0],
        ds.obsm["X_umap"][:, 1],
        C=values,
        cmap=expr_colormap(),
        gridsize=gridsize,
        linewidths=linewidths
    )
    cax = fig.add_axes((0.92, 0.8, 0.02, 0.15))
    fig.colorbar(hb, cax=cax, fraction=0.05, pad=0.02, aspect=40)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"{feature}")
    ax.set_xlabel("UMAP1")
    ax.set_ylabel("UMAP2")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    return fig


def plot_composition(ds, group_by, color, relative=False, palette=None, plot_numbers=False):
    left = np.zeros(len(ds.obs[group_by].unique()))
    total = None
    if relative:
        total = ds.obs[group_by].value_counts().sort_index(ascending=False)
    fig, ax = plt.subplots()
    num_colors = ds.obs[color].unique().size
    # TODO: adjust
    if palette is not None:
        colors = palette
    elif num_colors <= 10:
        colors = mpl.cm.tab10
    elif num_colors <= 20:
        colors = mpl.cm.tab20
    elif num_colors <= 28:
        colors = sc.pl.palettes.default_28
    else:
        colors = sc.pl.palettes.default_102
    for i, s in enumerate(ds.obs[color].cat.categories):
        cnt = ds.obs[group_by][ds.obs[color] == s].value_counts().sort_index(ascending=False)
        if relative:
            cnt = cnt / total * 100
        c = isinstance(colors, list) and colors[i] or colors(i)
        ax.barh(cnt.index, cnt, left=left, label=s, color=c)
        left += cnt
    if plot_numbers:
        for i, count in enumerate(total):
            ax.text(left[i] + 2, i, str(count), va="center")
    ax.legend(title=color.capitalize())
    ax.set_title(f"{group_by.capitalize()} by {color}")
    return ax
