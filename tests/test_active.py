from unittest import TestCase
import numpy as np
from athena.active import ActiveSubspaces
from contextlib import contextmanager
import matplotlib.pyplot as plt


@contextmanager
def assert_plot_figures_added():
    """
    Assert that the number of figures is higher than when you started the test
    """
    num_figures_before = plt.gcf().number
    yield
    num_figures_after = plt.gcf().number
    assert num_figures_before < num_figures_after


class TestUtils(TestCase):
    def test_init_W1(self):
        ss = ActiveSubspaces()
        self.assertIsNone(ss.W1)

    def test_init_W2(self):
        ss = ActiveSubspaces()
        self.assertIsNone(ss.W2)

    def test_init_evals(self):
        ss = ActiveSubspaces()
        self.assertIsNone(ss.evals)

    def test_init_evects(self):
        ss = ActiveSubspaces()
        self.assertIsNone(ss.evects)

    def test_init_evals_br(self):
        ss = ActiveSubspaces()
        self.assertIsNone(ss.evals_br)

    def test_init_subs_br(self):
        ss = ActiveSubspaces()
        self.assertIsNone(ss.subs_br)

    def test_init_dim(self):
        ss = ActiveSubspaces()
        self.assertIsNone(ss.dim)

    def test_init_cov_matrix(self):
        ss = ActiveSubspaces()
        self.assertIsNone(ss.cov_matrix)

    def test_compute_01(self):
        ss = ActiveSubspaces()
        with self.assertRaises(ValueError):
            ss.compute()

    def test_compute_02(self):
        np.random.seed(42)
        gradients = np.random.uniform(-1, 1, 60).reshape(15, 4)
        weights = np.ones((15, 1)) / 15
        ss = ActiveSubspaces()
        ss.compute(gradients=gradients,
                   weights=weights,
                   method='exact',
                   nboot=150)
        true_evals = np.array([0.571596, 0.465819, 0.272198, 0.175012])
        np.testing.assert_array_almost_equal(true_evals, ss.evals)

    def test_compute_03(self):
        np.random.seed(42)
        gradients = np.random.uniform(-1, 1, 60).reshape(15, 4)
        weights = np.ones((15, 1)) / 15
        ss = ActiveSubspaces()
        ss.compute(gradients=gradients,
                   weights=weights,
                   method='exact',
                   nboot=200)
        true_evects = np.array([[-0.019091, -0.408566, 0.861223, -0.301669],
                                [-0.767799, 0.199069, 0.268823, 0.546434],
                                [-0.463451, -0.758442, -0.427696, -0.164486],
                                [-0.441965, 0.467131, -0.055723, -0.763774]])
        np.testing.assert_array_almost_equal(true_evects, ss.evects)

    # def test_compute_04(self): np.random.seed(42) gradients =
    #     np.random.uniform(-1, 1, 60).reshape(15, 4) weights = np.ones((15, 1))
    #     / 15 ss = ActiveSubspaces() ss.compute(gradients=gradients,
    #     weights=weights, method='exact', nboot=250) true_cov_matrix =
    #     np.array([[0.295783, 0.004661, 0.057825, -0.056819], [0.004661,
    #     0.427352, 0.086039, 0.160164], [0.057825, 0.086039, 0.445253,
    #     -0.019482], [-0.056819, 0.160164, -0.019482, 0.316237]])
    #     np.testing.assert_array_almost_equal(true_cov_matrix, ss.cov_matrix)

    def test_compute_05(self):
        np.random.seed(42)
        inputs = np.random.uniform(-1, 1, 60).reshape(15, 4)
        outputs = np.random.uniform(0, 5, 15)
        ss = ActiveSubspaces()
        ss.compute(inputs=inputs, outputs=outputs, method='local', nboot=150)
        true_evals = np.array([13.794711, 11.102377, 3.467318, 1.116324])
        np.testing.assert_array_almost_equal(true_evals, ss.evals)

    def test_compute_06(self):
        np.random.seed(42)
        inputs = np.random.uniform(-1, 1, 60).reshape(15, 4)
        outputs = np.random.uniform(0, 5, 15)
        ss = ActiveSubspaces()
        ss.compute(inputs=inputs, outputs=outputs, method='local', nboot=200)
        true_evects = np.array([[-0.164383, 0.717021, -0.237246, -0.634486],
                                [-0.885808, 0.177628, 0.004112, 0.428691],
                                [0.255722, 0.558199, 0.734083, 0.290071],
                                [0.350612, 0.377813, -0.636254, 0.574029]])
        np.testing.assert_array_almost_equal(true_evects, ss.evects)

    def test_compute_07(self):
        np.random.seed(42)
        gradients = np.random.uniform(-1, 1, 180).reshape(15, 3, 4)
        weights = np.ones((15, 1)) / 15
        ss = ActiveSubspaces()
        ss.compute(gradients=gradients,
                   weights=weights,
                   method='exact',
                   nboot=150)
        true_evals = np.array([1.32606312, 1.20519582, 0.94811868, 0.68505712])
        np.testing.assert_array_almost_equal(true_evals, ss.evals)

    def test_compute_08(self):
        np.random.seed(42)
        gradients = np.random.uniform(-1, 1, 180).reshape(15, 3, 4)
        weights = np.ones((15, 1)) / 15
        ss = ActiveSubspaces()
        ss.compute(gradients=gradients,
                   weights=weights,
                   method='exact',
                   nboot=150)
        true_evects = np.array(
            [[0.67237041, 0.49917148, 0.50889687, 0.1994238],
             [0.20398894, -0.66183856, 0.09970486, 0.71443486],
             [-0.52895262, -0.11348076, 0.83802337, -0.07104981],
             [0.47593663, -0.54764923, 0.16970489, -0.66690696]])
        np.testing.assert_array_almost_equal(true_evects, ss.evects)

    def test_compute_9(self):
        np.random.seed(42)
        gradients = np.random.uniform(-1, 1, 180).reshape(15, 3, 4)
        weights = np.ones((15, 1)) / 15
        metric = np.diag(2 * np.ones(3))
        ss = ActiveSubspaces()
        ss.compute(gradients=gradients,
                   weights=weights,
                   method='exact',
                   nboot=150,
                   metric=metric)
        true_evects = np.array(
            [[0.67237041, 0.49917148, 0.50889687, 0.1994238],
             [0.20398894, -0.66183856, 0.09970486, 0.71443486],
             [-0.52895262, -0.11348076, 0.83802337, -0.07104981],
             [0.47593663, -0.54764923, 0.16970489, -0.66690696]])
        np.testing.assert_array_almost_equal(true_evects, ss.evects)

    def test_compute_10(self):
        np.random.seed(42)
        inputs = np.random.uniform(-1, 1, 60).reshape(15, 4)
        outputs = np.random.uniform(0, 5, 45).reshape(15, 3)
        weights = np.ones((15, 1)) / 15
        ss = ActiveSubspaces()
        ss.compute(inputs=inputs,
                   outputs=outputs,
                   weights=weights,
                   method='local',
                   nboot=150)
        true_evals = np.array(
            [84.08055975, 25.87980349, 9.61982202, 8.29248646])
        np.testing.assert_array_almost_equal(true_evals, ss.evals)

    def test_compute_11(self):
        np.random.seed(42)
        inputs = np.random.uniform(-1, 1, 60).reshape(15, 4)
        outputs = np.random.uniform(0, 5, 45).reshape(15, 3)
        weights = np.ones((15, 1)) / 15
        metric = np.diag(2 * np.ones(3))
        ss = ActiveSubspaces()
        ss.compute(inputs=inputs,
                   outputs=outputs,
                   weights=weights,
                   method='local',
                   nboot=150,
                   metric=metric)
        true_evects = np.array(
            [[0.75159386, 0.34814972, 0.5093598, 0.23334745],
             [-0.44047075, 0.89306499, -0.00249322, 0.09172904],
             [0.35007644, 0.2587911, -0.30548878, -0.84684725],
             [0.34429445, 0.11938954, -0.8045017, 0.46902504]])
        np.testing.assert_array_almost_equal(true_evects, ss.evects)

    def test_forward_01(self):
        np.random.seed(42)
        inputs = np.random.uniform(-1, 1, 60).reshape(15, 4)
        outputs = np.random.uniform(0, 5, 15)
        ss = ActiveSubspaces()
        ss.compute(inputs=inputs, outputs=outputs, method='local', nboot=250)
        ss.partition(2)
        active = ss.forward(np.random.uniform(-1, 1, 8).reshape(2, 4))[0]
        true_active = np.array([[-0.004748, 0.331107], [-0.949099, 0.347534]])
        np.testing.assert_array_almost_equal(true_active, active)

    def test_forward_02(self):
        np.random.seed(42)
        inputs = np.random.uniform(-1, 1, 60).reshape(15, 4)
        outputs = np.random.uniform(0, 5, 15)
        ss = ActiveSubspaces()
        ss.compute(inputs=inputs, outputs=outputs, method='local', nboot=250)
        ss.partition(2)
        inactive = ss.forward(np.random.uniform(-1, 1, 8).reshape(2, 4))[1]
        true_inactive = np.array([[-1.03574242, -0.04662904],
                                  [-0.49850367, -0.37146678]])
        np.testing.assert_array_almost_equal(true_inactive, inactive)

    def test_forward_03(self):
        np.random.seed(42)
        inputs = np.random.uniform(-1, 1, 60).reshape(15, 4)
        outputs = np.random.uniform(0, 5, 45).reshape(15, 3)
        ss = ActiveSubspaces()
        ss.compute(inputs=inputs,
                   outputs=outputs,
                   method='local',
                   nboot=250,
                   metric=np.diag(np.ones(3)))
        ss.partition(2)
        new_inputs = np.random.uniform(-1, 1, 8).reshape(2, 4)
        active, inactive = ss.forward(new_inputs)
        reconstructed_inputs = active.dot(ss.W1.T) + inactive.dot(ss.W2.T)
        np.testing.assert_array_almost_equal(new_inputs, reconstructed_inputs)

    def test_forward_04(self):
        np.random.seed(42)
        inputs = np.random.uniform(-1, 1, 60).reshape(15, 4)
        outputs = np.random.uniform(0, 5, 45).reshape(15, 3)
        ss = ActiveSubspaces()
        ss.compute(inputs=inputs, outputs=outputs, method='local', nboot=250)
        ss.partition(2)
        active = ss.forward(np.random.uniform(-1, 1, 8).reshape(2, 4))[0]
        true_active = np.array([[0.15284753, 0.67109407],
                                [0.69006622, -0.4165206]])
        np.testing.assert_array_almost_equal(true_active, active)

    def test_forward_05(self):
        np.random.seed(42)
        inputs = np.random.uniform(-1, 1, 60).reshape(15, 4)
        outputs = np.random.uniform(0, 5, 15)
        ss = ActiveSubspaces()
        ss.compute(inputs=inputs, outputs=outputs, method='local', nboot=250)
        ss.partition(2)
        inactive = ss.forward(np.random.uniform(-1, 1, 8).reshape(2, 4))[1]
        true_inactive = np.array([[-1.03574242, -0.04662904],
                                  [-0.49850367, -0.37146678]])
        np.testing.assert_array_almost_equal(true_inactive, inactive)

    def test_backward_01(self):
        np.random.seed(42)
        inputs = np.random.uniform(-1, 1, 60).reshape(15, 4)
        outputs = np.random.uniform(0, 5, 15)
        ss = ActiveSubspaces()
        ss.compute(inputs=inputs, outputs=outputs, method='local', nboot=250)
        ss.partition(1)
        new_inputs = np.random.uniform(-1, 1, 8).reshape(2, 4)
        active = ss.forward(new_inputs)[0]
        new_inputs = ss.backward(reduced_inputs=active, n_points=5)[0]
        np.testing.assert_array_almost_equal(np.kron(active, np.ones((5, 1))),
                                             new_inputs.dot(ss.W1))

    def test_backward_02(self):
        np.random.seed(42)
        inputs = np.random.uniform(-1, 1, 80).reshape(16, 5)
        outputs = np.random.uniform(-1, 3, 16)
        ss = ActiveSubspaces()
        ss.compute(inputs=inputs, outputs=outputs, method='local', nboot=250)
        ss.partition(2)
        new_inputs = np.random.uniform(-1, 1, 15).reshape(3, 5)
        active = ss.forward(new_inputs)[0]
        new_inputs = ss.backward(reduced_inputs=active, n_points=500)[0]
        np.testing.assert_array_almost_equal(np.kron(active, np.ones((500, 1))),
                                             new_inputs.dot(ss.W1))

    def test_rejection_sampling_inactive_01(self):
        np.random.seed(42)
        inputs = np.random.uniform(-1, 1, 60).reshape(15, 4)
        outputs = np.random.uniform(0, 5, 15)
        ss = ActiveSubspaces()
        ss.compute(inputs=inputs, outputs=outputs, method='local', nboot=250)
        ss.partition(1)
        new_inputs = np.random.uniform(-1, 1, 8).reshape(2, 4)
        active = ss.forward(new_inputs)[0]
        inactive_swap = np.array([
            ss._rejection_sampling_inactive(reduced_input=red_inp, n_points=1)
            for red_inp in active
        ])
        inactive_inputs = np.swapaxes(inactive_swap, 1, 2)
        new_inputs = ss._rotate_x(reduced_inputs=active,
                                  inactive_inputs=inactive_inputs)[0]
        np.testing.assert_array_almost_equal(active, new_inputs.dot(ss.W1))

    def test_rejection_sampling_inactive_02(self):
        np.random.seed(42)
        inputs = np.random.uniform(-1, 1, 60).reshape(15, 4)
        outputs = np.random.uniform(0, 5, 15)
        ss = ActiveSubspaces()
        ss.compute(inputs=inputs, outputs=outputs, method='local', nboot=250)
        ss.partition(1)
        new_inputs = np.random.uniform(-1, 1, 8).reshape(2, 4)
        active = ss.forward(new_inputs)[0]
        inactive_swap = np.array([
            ss._rejection_sampling_inactive(reduced_input=red_inp, n_points=10)
            for red_inp in active
        ])
        inactive_inputs = np.swapaxes(inactive_swap, 1, 2)
        new_inputs = ss._rotate_x(reduced_inputs=active,
                                  inactive_inputs=inactive_inputs)[0]
        np.testing.assert_array_almost_equal(np.kron(active, np.ones((10, 1))),
                                             new_inputs.dot(ss.W1))

    def test_hit_and_run_inactive_01(self):
        np.random.seed(42)
        inputs = np.random.uniform(-1, 1, 60).reshape(15, 4)
        outputs = np.random.uniform(0, 5, 15)
        ss = ActiveSubspaces()
        ss.compute(inputs=inputs, outputs=outputs, method='local', nboot=250)
        ss.partition(1)
        new_inputs = np.random.uniform(-1, 1, 8).reshape(2, 4)
        active = ss.forward(new_inputs)[0]
        inactive_swap = np.array([
            ss._hit_and_run_inactive(reduced_input=red_inp, n_points=1)
            for red_inp in active
        ])
        inactive_inputs = np.swapaxes(inactive_swap, 1, 2)
        new_inputs = ss._rotate_x(reduced_inputs=active,
                                  inactive_inputs=inactive_inputs)[0]
        np.testing.assert_array_almost_equal(active, new_inputs.dot(ss.W1))

    def test_hit_and_run_inactive_02(self):
        np.random.seed(42)
        inputs = np.random.uniform(-1, 1, 60).reshape(15, 4)
        outputs = np.random.uniform(0, 5, 15)
        ss = ActiveSubspaces()
        ss.compute(inputs=inputs, outputs=outputs, method='local', nboot=250)
        ss.partition(1)
        new_inputs = np.random.uniform(-1, 1, 8).reshape(2, 4)
        active = ss.forward(new_inputs)[0]
        inactive_swap = np.array([
            ss._hit_and_run_inactive(reduced_input=red_inp, n_points=10)
            for red_inp in active
        ])
        inactive_inputs = np.swapaxes(inactive_swap, 1, 2)
        new_inputs = ss._rotate_x(reduced_inputs=active,
                                  inactive_inputs=inactive_inputs)[0]
        np.testing.assert_array_almost_equal(np.kron(active, np.ones((10, 1))),
                                             new_inputs.dot(ss.W1))

    def test_partition_01(self):
        np.random.seed(42)
        matrix = np.random.uniform(-1, 1, 9).reshape(3, 3)
        ss = ActiveSubspaces()
        ss.evects = matrix
        ss.partition(dim=2)
        np.testing.assert_array_almost_equal(matrix[:, :2], ss.W1)

    def test_partition_02(self):
        np.random.seed(42)
        matrix = np.random.uniform(-1, 1, 9).reshape(3, 3)
        ss = ActiveSubspaces()
        ss.evects = matrix
        ss.partition(dim=2)
        np.testing.assert_array_almost_equal(matrix[:, 2:], ss.W2)

    def test_partition_03(self):
        np.random.seed(42)
        matrix = np.random.uniform(-1, 1, 9).reshape(3, 3)
        ss = ActiveSubspaces()
        ss.evects = matrix
        with self.assertRaises(TypeError):
            ss.partition(dim=2.0)

    def test_partition_04(self):
        np.random.seed(42)
        matrix = np.random.uniform(-1, 1, 9).reshape(3, 3)
        ss = ActiveSubspaces()
        ss.evects = matrix
        with self.assertRaises(ValueError):
            ss.partition(dim=0)

    def test_partition_05(self):
        np.random.seed(42)
        matrix = np.random.uniform(-1, 1, 9).reshape(3, 3)
        ss = ActiveSubspaces()
        ss.evects = matrix
        with self.assertRaises(ValueError):
            ss.partition(dim=4)

    def test_bootstrap_replicate_01(self):
        np.random.seed(42)
        matrix = np.random.uniform(-1, 1, 9).reshape(3, 3)
        weights = np.ones((3, 1)) / 3
        ss = ActiveSubspaces()
        wei = ss._bootstrap_replicate(matrix, weights)[1]
        np.testing.assert_array_almost_equal(weights, wei)

    def test_bootstrap_replicate_02(self):
        np.random.seed(42)
        matrix = np.random.uniform(-1, 1, 9).reshape(3, 3)
        weights = np.ones((3, 1)) / 3
        ss = ActiveSubspaces()
        mat = ss._bootstrap_replicate(matrix, weights)[0]
        true_matrix = np.array([[-0.88383278, 0.73235229, 0.20223002],
                                [0.19731697, -0.68796272, -0.68801096],
                                [-0.25091976, 0.90142861, 0.46398788]])
        np.testing.assert_array_almost_equal(true_matrix, mat)

    def test_bootstrap_replicate_03(self):
        np.random.seed(42)
        matrix = np.random.uniform(-1, 1, 27).reshape(3, 3, 3)
        weights = np.ones((3, 1)) / 3
        ss = ActiveSubspaces()
        wei = ss._bootstrap_replicate(matrix, weights)[1]
        np.testing.assert_array_almost_equal(weights, wei)

    def test_bootstrap_replicate_04(self):
        np.random.seed(42)
        matrix = np.random.uniform(-1, 1, 27).reshape(3, 3, 3)
        weights = np.ones((3, 1)) / 3
        ss = ActiveSubspaces()
        mat = ss._bootstrap_replicate(matrix, weights)[0]
        true_matrix = np.array([[[-0.13610996, -0.41754172, 0.22370579],
                                 [-0.72101228, -0.4157107, -0.26727631],
                                 [-0.08786003, 0.57035192, -0.60065244]],
                                [[-0.25091976, 0.90142861, 0.46398788],
                                 [0.19731697, -0.68796272, -0.68801096],
                                 [-0.88383278, 0.73235229, 0.20223002]],
                                [[-0.13610996, -0.41754172, 0.22370579],
                                 [-0.72101228, -0.4157107, -0.26727631],
                                 [-0.08786003, 0.57035192, -0.60065244]]])
        np.testing.assert_array_almost_equal(true_matrix, mat)

    def test_compute_bootstrap_ranges_01(self):
        np.random.seed(42)
        gradients = np.random.uniform(-1, 1, 60).reshape(30, 2)
        weights = np.ones((30, 1)) / 30
        ss = ActiveSubspaces()
        ss.compute(gradients=gradients, weights=weights, nboot=100)
        true_bounds_evals = np.array([[0.3000497, 0.59008536],
                                      [0.17398718, 0.40959827]])
        np.testing.assert_array_almost_equal(true_bounds_evals, ss.evals_br)

    def test_compute_bootstrap_ranges_02(self):
        np.random.seed(42)
        gradients = np.random.uniform(-1, 1, 60).reshape(30, 2)
        weights = np.ones((30, 1)) / 30
        ss = ActiveSubspaces()
        ss.compute(gradients=gradients,
                   weights=weights,
                   method='exact',
                   nboot=100)
        true_bounds_subspace = np.array([[0.00261813, 0.58863862, 0.99998352]])
        np.testing.assert_array_almost_equal(true_bounds_subspace, ss.subs_br)

    def test_compute_bootstrap_ranges_03(self):
        np.random.seed(42)
        gradients = np.random.uniform(-1, 1, 180).reshape(30, 3, 2)
        weights = np.ones((30, 1)) / 30
        ss = ActiveSubspaces()
        ss.compute(gradients=gradients, weights=weights, nboot=100)
        true_bounds_evals = np.array([[0.99330673, 1.62694823],
                                      [0.65987633, 1.11751475]])
        np.testing.assert_array_almost_equal(true_bounds_evals, ss.evals_br)

    def test_compute_bootstrap_ranges_04(self):
        np.random.seed(42)
        gradients = np.random.uniform(-1, 1, 180).reshape(30, 3, 2)
        weights = np.ones((30, 1)) / 30
        ss = ActiveSubspaces()
        ss.compute(gradients=gradients,
                   weights=weights,
                   method='exact',
                   nboot=100)
        true_bounds_subspace = np.array([[0.00109331, 0.30254992, 0.90447872]])
        np.testing.assert_array_almost_equal(true_bounds_subspace, ss.subs_br)

    def test_plot_eigenvalues_01(self):
        ss = ActiveSubspaces()
        with self.assertRaises(ValueError):
            ss.plot_eigenvalues(figsize=(7, 7), title='Eigenvalues')

    def test_plot_eigenvalues_02(self):
        np.random.seed(42)
        gradients = np.random.uniform(-1, 1, 200).reshape(50, 4)
        weights = np.ones((50, 1)) / 50
        ss = ActiveSubspaces()
        ss.compute(gradients=gradients, weights=weights, nboot=200)
        with assert_plot_figures_added():
            ss.plot_eigenvalues(figsize=(7, 7), title='Eigenvalues')

    def test_plot_eigenvalues_03(self):
        np.random.seed(42)
        gradients = np.random.uniform(-1, 1, 200).reshape(50, 4)
        weights = np.ones((50, 1)) / 50
        ss = ActiveSubspaces()
        ss.compute(gradients=gradients, weights=weights, nboot=200)
        with assert_plot_figures_added():
            ss.plot_eigenvalues(n_evals=3, figsize=(7, 7), title='Eigenvalues')

    def test_plot_eigenvectors_01(self):
        ss = ActiveSubspaces()
        with self.assertRaises(ValueError):
            ss.plot_eigenvectors(figsize=(7, 7), title='Eigenvalues')

    def test_plot_eigenvectors_02(self):
        np.random.seed(42)
        gradients = np.random.uniform(-1, 1, 200).reshape(50, 4)
        weights = np.ones((50, 1)) / 50
        ss = ActiveSubspaces()
        ss.compute(gradients=gradients, weights=weights, nboot=200)
        with assert_plot_figures_added():
            ss.plot_eigenvectors(n_evects=2,
                                 figsize=(7, 7),
                                 title='Eigenvectors')

    def test_plot_eigenvectors_03(self):
        np.random.seed(42)
        gradients = np.random.uniform(-1, 1, 200).reshape(50, 4)
        weights = np.ones((50, 1)) / 50
        ss = ActiveSubspaces()
        ss.compute(gradients=gradients, weights=weights, nboot=200)
        with assert_plot_figures_added():
            ss.plot_eigenvectors(n_evects=2,
                                 figsize=(5, 8),
                                 labels=[r'$x$', r'$y$', r'$r$', r'$z$'])

    def test_plot_sufficient_summary_01(self):
        ss = ActiveSubspaces()
        with self.assertRaises(ValueError):
            ss.plot_sufficient_summary(10, 10)

    def test_plot_sufficient_summary_02(self):
        np.random.seed(42)
        gradients = np.random.uniform(-1, 1, 200).reshape(50, 4)
        weights = np.ones((50, 1)) / 50
        ss = ActiveSubspaces()
        ss.compute(gradients=gradients, weights=weights, nboot=200)
        ss.partition(3)
        with self.assertRaises(ValueError):
            ss.plot_sufficient_summary(10, 10)

    def test_plot_sufficient_summary_03(self):
        np.random.seed(42)
        gradients = np.random.uniform(-1, 1, 200).reshape(50, 4)
        weights = np.ones((50, 1)) / 50
        ss = ActiveSubspaces()
        ss.compute(gradients=gradients, weights=weights, nboot=200)
        ss.partition(2)
        with assert_plot_figures_added():
            ss.plot_sufficient_summary(
                np.random.uniform(-1, 1, 100).reshape(25, 4),
                np.random.uniform(-1, 1, 25).reshape(-1, 1))
