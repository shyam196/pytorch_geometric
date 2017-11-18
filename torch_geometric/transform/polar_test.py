from math import sqrt

from unittest import TestCase
import torch
from numpy.testing import assert_equal, assert_almost_equal

from .polar import PolarAdj


class PolarTest(TestCase):
    def test_polar_adj(self):
        position = torch.LongTensor([[1, 0], [0, 0], [-2, 2]])
        index = torch.LongTensor([[0, 1, 1, 2], [1, 0, 2, 1]])
        weight = torch.FloatTensor([1, 1, 1, 1])
        adj = torch.sparse.FloatTensor(index, weight, torch.Size([3, 3]))

        transform = PolarAdj()

        _, adj, position = transform((None, adj, position))
        adj = adj.to_dense()

        expected_position = [[1, 0], [0, 0], [-2, 2]]
        expected_adj_rho = [
            [0, 1 / sqrt(8), 0],
            [1 / sqrt(8), 0, 1],
            [0, 1, 0],
        ]
        expected_adj_theta = [
            [0, 0.5, 0],
            [0, 0, 0.375],
            [0, 0.875, 0],
        ]

        assert_equal(adj.size(), [3, 3, 2])
        assert_equal(position.numpy(), expected_position)
        assert_almost_equal(adj[:, :, 0].numpy(), expected_adj_rho)
        assert_almost_equal(adj[:, :, 1].numpy(), expected_adj_theta)
