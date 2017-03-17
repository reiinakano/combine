import unittest
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotter


class TestGetOverlapValue(unittest.TestCase):
    def test_overlap_value(self):
        arr1 = ['a', 'b', 'c', 'd']
        arr2 = ['a', 'b', 'c', 'e', 'f']
        assert plotter.get_overlap_value(arr1, arr2) == 0.75

        arr2 = ['a', 'b', 'c', 'e', 'f', 'd']
        assert plotter.get_overlap_value(arr1, arr2) == 1

        arr2 = np.array([1, 2, 3, 4])
        assert plotter.get_overlap_value(arr1, arr2) == 0


class TestBuildOverlapMatrix(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame(
            [
                ['a', 'src1'],
                ['b', 'src2'],
                ['a', 'src2'],
                ['d', 'src1'],
                ['e', 'src2'],
                ['g', 'src3'],
                ['h', 'src3'],
                ['a', 'src3']
            ],
            columns=['entity', 'source']
        )

    def test_build_overlap_matrix_all_sources(self):
        matrix, sources = plotter.build_overlap_matrix(self.df)

        np.testing.assert_array_equal(
            [
                [1.0, 0.5, 0.5],
                [0.5, 1.0, 1./3],
                [0.5, 1./3, 1.0]
            ],
            matrix
        )

        assert sources == ['src1', 'src2', 'src3']

    def test_build_overlap_matrix_specifi_sources(self):
        matrix, sources = plotter.build_overlap_matrix(self.df, ['src1', 'src2'])

        np.testing.assert_array_equal(
            [
                [1.0, 0.5],
                [0.5, 1.0]
            ],
            matrix
        )

        assert sources == ['src1', 'src2']


class TestPlotOverlapMatrix(unittest.TestCase):
    def tearDown(self):
        plt.close('all')

    def test_plot_overlap_matrix(self):
        matrix = np.array(
            [
                [1.0, 0.5, 0.5],
                [0.5, 1.0, 1./3],
                [0.5, 1./3, 1.0]
            ]
        )
        sources = ['src1', 'src2', 'src3']

        plotter.plot_overlap_matrix(matrix, sources)
