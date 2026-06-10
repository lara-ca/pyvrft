import unittest
from unittest.mock import patch
from io import StringIO
import numpy as np
import vrft
import scipy.signal as signal
from vrft.control_fisher import check_Z 

class TestCheckZ(unittest.TestCase):

    def _make_Z(self, eigenvalues):
        n = len(eigenvalues)
        Q, _ = np.linalg.qr(np.random.randn(n, n))
        return Q @ np.diag(eigenvalues) @ Q.T

    def test_well_conditioned(self):
        Z = self._make_Z([100.0, 50.0, 10.0])
        result_Z, min_eig = check_Z(Z, threshold=1e-4)
        self.assertTrue(np.allclose(result_Z, Z))
        self.assertAlmostEqual(min_eig, 10.0, places=8)

    def test_ill_conditioned_warns(self):
        Z = self._make_Z([100.0, 10.0, 1e-6])
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            result_Z, min_eig = check_Z(Z, threshold=1e-4)
            output = mock_stdout.getvalue()
        self.assertIn("Warning", output)
        self.assertTrue(np.allclose(result_Z, Z))  # still returns Z normally

    def test_design(self):

        G11 = signal.TransferFunction([1], [1, -0.9], dt=1)
        G12 = 0
        G21 = 0
        G22 = signal.TransferFunction([1], [1, -0.9], dt=1)
        G = [[G11, G12], [G21, G22]]
        Td11 = signal.TransferFunction([0.2], [1, -0.8], dt=1)
        Td12 = 0
        Td21 = 0
        Td22 = signal.TransferFunction([0.2], [1, -0.8], dt=1)
        Td = [[Td11, Td12], [Td21, Td22]]
        L = Td
        Cpi = [
            [signal.TransferFunction([1, 0], [1, -1], dt=1)],
            [signal.TransferFunction([1], [1, -1], dt=1)],
        ]
        C = [[Cpi, []], [[], Cpi]]
        N = 350
        t = np.linspace(0, N - 1, N)
        t.shape = (1, N)
        ts = N
        fs = 1 / ts
        u1 = 0.5 - 0.5 * signal.square(2 * np.pi * fs * t).T
        u2 = 0.5 - 0.5 * signal.square(2 * np.pi * fs * t - 3 * np.pi / 2).T
        u = np.concatenate((u1, u2), axis=1)
        y = vrft.filter(G, u)
        p, Z, min_eigenvalue= vrft.design_fisher(u, y, y, Td, C, L)

        p0 = np.array([[0.2], [-0.18], [0.2], [-0.18]])
        Z0 = np.array([
            [383861, 382566,      0,      0],
            [382566, 381361,      0,      0],
            [     0,      0, 410223, 410133],
            [     0,      0, 410133, 410223],
        ])
        min_eigenvalue0 = 42.86180529592093

        self.assertTrue(np.linalg.norm(p - p0) < np.finfo(np.float32).eps)
        self.assertTrue(np.allclose(Z, Z0, atol=1))
        self.assertTrue(np.allclose(min_eigenvalue, min_eigenvalue0, atol=1))

if __name__ == "__main__":
    unittest.main()