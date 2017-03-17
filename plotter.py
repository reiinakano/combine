import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools as it
import argparse

from logger import get_logger


logger = get_logger('plotter')


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help="Specify baler.py output file to plot. Defaults to harvest.csv")


def get_overlap_value(arr1, arr2):
    """Get overlap percentage from two array-like objects

    Args:
        arr1 (array-like): First array

        arr2 (array-like): Second array

    Returns:
        overlap_value (float): Overlap percentage in range [0, 1]

        sources (list): List containing ordered names of sources
    """
    set1, set2 = set(arr1), set(arr2)
    num_overlap = len(set1.intersection(set2))
    overlap_value = num_overlap / float(min(len(set1), len(set2)))
    return overlap_value


def build_overlap_matrix(dataframe, sources=None):
    """Builds overlap matrix

    Args:
        dataframe (pandas.DataFrame object): Dataframe containing data
            to plot overlap matrix for

        sources (list or None, optional): List of sources to display in
            the overlap matrix

    Returns:
        matrix (numpy.ndarray): Overlap matrix
    """
    unique_sources = dataframe["source"].unique()

    if sources is None:
        sources = list(unique_sources)
    else:
        sources = [x for x in sources if x in unique_sources]

    source_pairs = list(it.combinations(sources, 2))

    pair_overlap_values = []
    for pair in source_pairs:
        source1 = dataframe.loc[dataframe['source'] == pair[0]]['entity'].values
        source2 = dataframe.loc[dataframe['source'] == pair[1]]['entity'].values
        pair_overlap_values.append(get_overlap_value(source1, source2))

    # Initialize array to hold overlap matrix values
    matrix = np.full((len(sources), len(sources)), np.inf)
    for idx, pair in enumerate(source_pairs):
        matrix[sources.index(pair[0])][sources.index(pair[1])] = pair_overlap_values[idx]
        matrix[sources.index(pair[1])][sources.index(pair[0])] = pair_overlap_values[idx]

    for i in range(len(sources)):
        matrix[i][i] = 1.0

    return matrix, sources


def plot_overlap_matrix(matrix, sources):
    """Plots overlap matrix

    Args:
        matrix (array-like): NxN array containing overlap matrix

        sources (list): List of length N, containing ordered names of sources

    Returns:
        ax (matplotlib.axes.Axes object): Axes where overlap matrix is drawn
    """
    matrix = np.round(matrix, 2)

    fig, ax = plt.subplots(1, 1)

    ax.set_title('Overlap matrix')

    image = ax.imshow(matrix, interpolation='nearest', cmap=plt.cm.Blues)

    plt.colorbar(mappable=image)

    tick_marks = np.arange(len(sources))
    ax.set_xticks(tick_marks)
    ax.set_xticklabels(sources, rotation=45, ha='right')
    ax.set_yticks(tick_marks)
    ax.set_yticklabels(sources)

    thresh = matrix.max() / 2.
    for i, j in it.product(range(matrix.shape[0]), range(matrix.shape[1])):
        ax.text(j, i, matrix[i, j],
                horizontalalignment="center",
                verticalalignment="center",
                color="white" if matrix[i, j] > thresh else "black")

    return ax


def plot(file_to_plot, sources=None):
    logger.info('Preparing to generate plots for {}'.format(file_to_plot))

    try:
        df = pd.read_csv(file_to_plot)
    except Exception as e:
        logger.error('Error reading csv')
        raise

    logger.info('Plotting overlap matrix')
    plot_overlap_matrix(*build_overlap_matrix(df, sources))

    plt.show()


if __name__ == '__main__':
    args = parser.parse_args()
    file_to_plot = args.file if args.file else 'harvest.csv'
    plot(file_to_plot)
