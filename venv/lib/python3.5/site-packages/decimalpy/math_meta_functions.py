#############################################################################
# The finance package is open source under the `Python Software Foundation  #
# License <http://www.opensource.org/licenses/PythonSoftFoundation.php>`_   #
#############################################################################

'''
**The decimalpy.mathmetafunctions**

This module contains mathematical functions on functions such as numerical
first and second order derivative.
Also it contains tools in order to do decimal calculations.
'''
from decimal import Decimal


class NumericalFirstOrder:
    '''Is instantiated with a countinous derivable function and a possible
    step size (default = Decimal('0.0001')) for the numerical differentiation.

    **How to use:**

    >>> import decimalpy as dp
    >>> deriv_ln = dp.NumericalFirstOrder(dp.ln)
    >>> for x in (1, float(2), Decimal('8')): # must be (1, 0.5, 0.125)
    ...     print deriv_ln(x)
    ...
    0.9999999999999999199999971433
    0.49999999999999999749999975
    0.1249999999999999999975558333
    >>> isinstance(deriv_ln(4), Decimal)
    True


    References:

    #. http://amath.colorado.edu/faculty/fornberg/Docs/MathComp_88_FD_formulas.pdf
    #. http://en.wikipedia.org/wiki/Numerical_differentiation
    #. http://en.wikipedia.org/wiki/Lagrange_polynomial
    #. http://www.math-linux.com/spip.php?article71
    #. http://www.proofwiki.org/wiki/Lagrange_Polynomial_Approximation
    #. http://people.maths.ox.ac.uk/trefethen/barycentric.pdf
    '''
    def __init__(self, function, step_size=Decimal('0.0001')):
        ''':param function: A function
        :type function: A one dimensional function accepting and returning
        Decimal as values
        :param step_size: A Decimal specifying the step size
        :type step_size: Decimal or float
        '''
        self.function = function
        self.step_size = Decimal('%s' % step_size)

    def __call__(self, x_value):
        ''':param x_value: A value
        :type x_value: a positive integer, float or decimal
        :return: The first order derivative at the x_value
        '''
        x_value = Decimal(x_value)
        if x_value:
            upper2 = self.function(x_value + 2 * self.step_size)
            lower2 = self.function(x_value - 2 * self.step_size)
            upper1 = self.function(x_value + self.step_size)
            lower1 = self.function(x_value - self.step_size)
            return ((8 * (upper1 - lower1) - (upper2 - lower2))
                    / self.step_size / Decimal('12'))


class NumericalSecondOrder:
    '''Is instantiated with a countinous derivable function and a possible step
    size (default = Decimal('0.0001')) for the numerical differentiation.

    **How to use:**

    >>> import decimalpy as dp
    >>> curvature = dp.NumericalSecondOrder(dp.ln)
    >>> for x in (1, float(2), Decimal('4')): # must be (-1, -0.25, -0.0625)
    ...     print curvature(x)
    ...
    -0.9999999999999998666666641667
    -0.2499999999999999978333333333
    -0.06250000000000000009166666667

    References:

    #. http://amath.colorado.edu/faculty/fornberg/Docs/MathComp_88_FD_formulas.pdf
    #. http://en.wikipedia.org/wiki/Numerical_differentiation
    #. http://en.wikipedia.org/wiki/Lagrange_polynomial
    #. http://www.math-linux.com/spip.php?article71
    #. http://www.proofwiki.org/wiki/Lagrange_Polynomial_Approximation
    #. http://people.maths.ox.ac.uk/trefethen/barycentric.pdf
    '''

    def __init__(self, function, step_size=Decimal('0.0001')):
        ''':param function: A function
        :type function: A one dimensional function accepting and returning
        Decimal as values
        :param step_size: A Decimal specifying the step size
        :type step_size: Decimal or float
        '''
        self.function = function
        self.step_size = Decimal('%s' % step_size)

    def __call__(self, x_value):
        ''':param x_value: A value
        :type x_value: a positive integer, float or decimal
        :return: The first order derivative at the x_value
        '''
        x_value = Decimal(x_value)
        if x_value:
            upper2 = self.function(x_value + 2 * self.step_size)
            lower2 = self.function(x_value - 2 * self.step_size)
            upper1 = self.function(x_value + self.step_size)
            lower1 = self.function(x_value - self.step_size)
            middle = self.function(x_value)
            return ((-30 * middle + 16 * (upper1 + lower1) - (upper2 + lower2))
                    / self.step_size / self.step_size / Decimal('12'))


class Solver:
    '''Solver
    **How to use:**

    >>> import decimalpy as dp
    >>> f = lambda x: x*x
    >>> numeric_sqrt = Solver(f)
    >>> for x in [4, 9.0, Decimal('16')]:
    ...     print numeric_sqrt(x, 1)
    2.000000000000002158638110942
    3.000000000000000000325260652
    4.000000000000050672229330380
    '''
    def __init__(self,
                function,
                derivative=None,
                precision=Decimal('1e-6'),
                max_iteration=30
                ):
        self.function = function
        if derivative:
            self.derivative = derivative
        else:
            self.derivative = NumericalFirstOrder(function)
        self.precision = Decimal('%s' % precision)
        if isinstance(max_iteration, int):
            self.max_iteration = max_iteration
        else:
            self.max_iteration = 30

    def __call__(self,
                 target,
                 minimum=Decimal('0'),  # Or start value
                 maximum=None
                 ):
        '''
        The structure is copied from [Kiusalaas]_ p. 155, newtonRaphson
        '''
        target = Decimal(target)
        minimum = Decimal(minimum)
        if target and isinstance(minimum, Decimal):
            maximum = Decimal(maximum) if maximum else None
            bracketed = False
            if maximum:
                diff_min = target - self.function(minimum)
                diff_max = target - self.function(maximum)
                bracketed = (diff_min * diff_max > 0)
            value = minimum
            for i in range(self.max_iteration):
                use_bisection = False
                diff = target - self.function(value)
                try:
                    delta = diff / self.derivative(value)
                    value += delta
                    use_bisection = bracketed and not minimum <= value <= maximum
                except ZeroDivisionError:
                    if bracketed:
                        use_bisection = True
                        if minimum <= value <= maximum and diff * diff_min:
                            maximum = value
                        if minimum <= value <= maximum and diff * diff_max:
                            minimum = value
                    else:
                        raise ZeroDivisionError(
                        'Division by derivative value equal to zero')
                if use_bisection:
                    value = (maximum + maximum) * Decimal('0.5')
                    delta = (maximum - maximum) * Decimal('0.5')
                if abs(delta) < self.precision:
                    return value
            raise Exception('Precision cannot be meet by iterations')


if __name__ == '__main__':
    import doctest
    doctest.testmod()