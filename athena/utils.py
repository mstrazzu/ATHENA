"""Utility functions module.
"""
import numpy as np
from scipy.optimize import linprog


class Normalizer(object):
    """A class for normalizing and unnormalizing bounded inputs.

    :param numpy.ndarray lb: array n_params-by-1 that contains lower bounds
        on the simulation inputs.
    :param numpy.ndarray ub: array n_params-by-1 that contains upper bounds
        on the simulation inputs.
    """
    def __init__(self, lb, ub):
        self.lb = lb
        self.ub = ub

    def fit_transform(self, inputs):
        """Return corresponding points shifted and scaled to [-1, 1]^n_params.

        :param numpy.ndarray inputs: contains all input points to normalize.
            The shape is n_samples-by-n_params. The components of each row of
            `inputs` should be between `self.lb` and `self.ub`.
        :return: the normalized inputs. The components of each row should be
            between -1 and 1.
        :rtype: numpy.ndarray
        """
        inputs_norm = 2.0 * (inputs - self.lb) / (self.ub - self.lb) - 1.0
        return inputs_norm

    def inverse_transform(self, inputs):
        """Return corresponding points shifted and scaled to
        `[self.lb, self.ub]`.

        :param numpy.ndarray inputs: contains all input points to unnormalize.
            The shape is n_samples-by-n_params. The components of each row of
            `inputs` should be between -1 and 1.
        :return: the unnormalized inputs. The components of each row should be
            between `self.lb` and `self.ub`.
        :rtype: numpy.ndarray
        """
        inputs_unnorm = (self.ub - self.lb) * (inputs + 1.0) / 2.0 + self.lb
        return inputs_unnorm


def initialize_weights(matrix):
    """
    TO DOC
    """
    return np.ones((matrix.shape[0], 1)) / matrix.shape[0]


def linear_program_ineq(c, A, b):
    """Solves an equality constrained linear program with variable bounds.
    This method returns the minimizer of the following linear program.

    minimize  c^T x
    subject to  A x >= b

    :param numpy.ndarray c: coefficients vector of the linear objective
        function to be minimized.
    :param numpy.ndarray A: 2-D array which, when matrix-multiplied by x,
        gives the values of the lower-bound inequality constraints at x.
    :param numpy.ndarray b: 1-D array of values representing the lower-bound
        of each inequality constraint (row) in A.
    :return: the independent variable vector which minimizes the linear
        programming problem.
    :rtype: numpy.ndarray
    :raises: RuntimeError
    """
    c = c.reshape(-1, )
    b = b.reshape(-1, )

    # make unbounded bounds
    bounds = [(None, None) for i in range(c.shape[0])]
    res = linprog(c=c, A_ub=-A, b_ub=-b, bounds=bounds)
    if res.success:
        return res.x.reshape(-1, 1)
    else:
        raise RuntimeError('Scipy did not solve the LP. {}'.format(res.message))


def local_linear_gradients(inputs, outputs, weights=None, n_neighbors=None):
    """Estimate a collection of gradients from input/output pairs.

    Given a set of input/output pairs, choose subsets of neighboring points and
    build a local linear model for each subset. The gradients of these local
    linear models comprise estimates of sampled gradients.
    Parameters
    ----------
    inputs : ndarray
        M-by-m matrix that contains the m-dimensional inputs
    outputs : ndarray
        M-by-1 matrix that contains scalar outputs
    n_neighbors : int, optional
        how many nearest neighbors to use when constructing the local linear
        model. the default value is floor(1.7*m)
    weights : ndarray, optional
        M-by-1 matrix that contains the weights for each observation (default
        None)
    Returns
    -------
    gradients : ndarray
        M-by-m matrix that contains estimated partial derivatives approximated
        by the local linear models

    :raises: ValueError, TypeError
    """
    n_samples, n_pars = inputs.shape

    if n_samples <= n_pars:
        raise ValueError('Not enough samples for local linear models.')
    if n_neighbors is None:
        n_neighbors = int(min(np.floor(1.7 * n_pars), n_samples))
    elif not isinstance(n_neighbors, int):
        raise TypeError(
            'n_neighbors ({}) must be an integer.'.format(n_neighbors))

    if n_neighbors <= n_pars or n_neighbors > n_samples:
        raise ValueError(
            'n_neighbors must be between the number of parameters '
            'and the number of samples. Unsatisfied: {} < {} < {}.'.format(
                n_pars, n_neighbors, n_samples))

    if weights is None:
        weights = initialize_weights(inputs)

    MM = min(int(np.ceil(10 * n_pars * np.log(n_pars))), n_samples - 1)

    # distinguish between scalar and vectorial outputs
    if len(outputs.shape) == 1 or outputs.shape[1] == 0:
        gradients = np.zeros((MM, n_pars))
    else:
        gradients = np.zeros((MM, outputs.shape[1], n_pars))

    # new inputs are defined since MM is different from n_samples
    new_inputs = np.zeros((MM, n_pars))

    for i in range(MM):
        ii = np.random.randint(n_samples)
        inputs_rand_row = inputs[ii, :]
        D2 = np.sum((inputs - inputs_rand_row)**2, axis=1)
        ind = np.argsort(D2)
        ind = ind[D2 != 0]
        A = np.hstack((np.ones(
            (n_neighbors, 1)), inputs[ind[:n_neighbors], :])) * np.sqrt(
                weights[ii])
        b = outputs[ind[:n_neighbors]] * np.sqrt(weights[ii])
        u = np.linalg.lstsq(A, b, rcond=None)[0]
        gradients[i] = u[1:].T
        new_inputs[i, :] = (1 / n_neighbors) * np.sum(
            inputs[ind[:n_neighbors], :], axis=0)
    return gradients, new_inputs


def sort_eigpairs(matrix):
    """Compute eigenpairs and sort.

    :param numpy.ndarray matrix: matrix whose eigenpairs you want.
    :return: vector of sorted eigenvalues; orthogonal matrix of corresponding
        eigenvectors.
    :rtype: numpy.ndarray, numpy.ndarray

    .. note::

        Eigenvectors are unique up to a sign. We make the choice to normalize
        the eigenvectors so that the first component of each eigenvector is
        positive. This normalization is very helpful for the bootstrapping.
    """
    evals, evects = np.linalg.eigh(matrix)
    evals = abs(evals)
    ind = np.argsort(evals)
    evals = evals[ind[::-1]]
    evects = evects[:, ind[::-1]]
    s = np.sign(evects[0, :])
    s[s == 0] = 1
    evects *= s
    return evals.reshape(-1, 1), evects
