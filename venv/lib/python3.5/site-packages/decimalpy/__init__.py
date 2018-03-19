#############################################################################
# The finance package is open source under the `Python Software Foundation  #
# License <http://www.opensource.org/licenses/PythonSoftFoundation.php>`_   #
#############################################################################

'''
*********************************
The decimalpy package for Python!
*********************************

Introduction
============

It has been decided to use the datatype Decimal as base for al calculations
in the `finance <..//rstFiles/200%20PythonHacks.html#the-finance-package>`_
package.

There are 2 reasons for this:

#. In finance decimals matters and when other financial systems use the IEEE
   standard 854-1987 the package finance need to do the same
#. For valuation purposes it is important that the financial calculations are
   the exact same as those performed in eg spreadsheets

`See also the chapter that examplifies the reasons for this. <..//rstFiles/600%20On%20Python.html#arrays-for-financial-calculations>`_

The Package decimalpy is inspired by `numpy <http://numpy.scipy.org>`_ and
eg the vector concept of `The R package <http://www.r-project.org>`_.
The key difference from numpy is that in decimalpy the only Decimal type is
decimal.

The Package contains:

* An n-dimensional array of decimals, a decimalvector
* An n-dimensional array of decimals where the keys can be of a specific
  type and not just integers as in a decimalvector, a
  SortedKeysDecimalValuedDict
* A decorator decimalvector_function that converts a simpel function into a
  function that given a decimalvector as an argument returns a decimalvector
  of function values. This makes it fairly easy to extend the Decimal of
  decimalvector functions. Also decimalvector functions makes it fairly easy
  to use other packages like eg matplotlib
* A set of decimalvector (typically financial) functions
* Meta functions (functions on functions) for numerical first
  (NumericalFirstOrder) and second (NumericalSecondOrder) order differention
* A meta function for finding the inverse value of a function

The package will be extended in order to support the needs in the package
`finance <..//rstFiles/200%20PythonHacks.html#the-finance-package>`_ .

The finance package is open source under the `Python Software Foundation
License <http://www.opensource.org/licenses/PythonSoftFoundation.php>`_

Class definitions and documentation
===================================

'''
__version__ = '0.1a beta'

from decimal import Decimal as _dec, getcontext as _getcontext
from math_types import Vector, vector_function, \
     Polynomial, PolyExponents, SortedKeysDecimalValuedDict
from math_vector_functions import exp, ln, PiecewiseConstant, \
     LinearSpline, NaturalCubicSpline, FinancialCubicSpline
from math_meta_functions import NumericalFirstOrder, NumericalSecondOrder, \
     Solver


def to_decimal(value):
    '''If value can be converted to a Decimal type then the decimal version
    of value is returned.
    This function becomes obsolete as soon as decimalpy get's it's own
    Decimal type.

    **Usage**

    >>> from decimal import Decimal
    >>> to_decimal(Decimal('4.5')), to_decimal('4.5'), to_decimal(4.5)
    (Decimal('4.5'), Decimal('4.5'), Decimal('4.5'))
    '''
    return _dec(str(value))


def round_decimal(value, nbr_of_decimals=7, rounding_method='ROUND_HALF_UP'):
    '''Rounds off Decimal by nbr_of_decimals using rounding_method.
    Decimal should be used whenever one is doing financial calculations.
    Decimal avoids small errors due Decimal representation etc.
    In other words calculations become similar to those in spreadsheets
    like eg Excel.

    Possible rounding methods are:
        * ROUND_CEILING - Always round upwards towards infinity
        * ROUND_DOWN - Always round toward zero
        * ROUND_FLOOR - Always round down towards negative infinity
        * ROUND_HALF_DOWN - Rounds away from zero if the last significant
          digit is greater than or equal to 5, otherwise toward zero
        * ROUND_HALF_EVEN - Like ROUND_HALF_DOWN except that if the value
          is 5 then the preceding digit is examined. Even values cause
          the result to be rounded down and odd digits cause the result
          to be rounded up
        * ROUND_HALF_UP - Like ROUND_HALF_DOWN except if the last
          significant digit
          is 5 the value is rounded away from zero
        * ROUND_UP - Round away from zero
        * ROUND_05UP - Round away from zero if the last digit is 0 or 5,
          otherwise towards zero
    '''
    if isinstance(nbr_of_decimals, int):
        if value and isinstance(value, (int, float, _dec)):
            value = to_decimal(value)
            rounding = _getcontext().rounding
            _getcontext().rounding = rounding_method
            value = _dec(value.quantize(_dec('.1') ** nbr_of_decimals))
            _getcontext().rounding = rounding
            return value


def linspace_iter(iter_min, iter_max, nbr_of_steps):
    '''Generates nbr_of_steps step values starting with min and ending with
    max, both included.

    **Usage**

    >>> ['%.3f' % step for step in linspace_iter(2, 3, 5)]
    ['2.000', '2.250', '2.500', '2.750', '3.000']
    '''
    iter_min = to_decimal(iter_min)
    iter_max = to_decimal(iter_max)
    assert isinstance(nbr_of_steps, int) and nbr_of_steps > 1, \
            'nbr_of_steps (%s) must be a integer larger than 1' % nbr_of_steps
    assert iter_min < iter_max, 'Min (%s) must be less than max(%s)' \
                                    % (iter_min, iter_max)
    step = (iter_max - iter_min) / (nbr_of_steps - 1)
    for step_nbr in range(nbr_of_steps):
        yield iter_min + step_nbr * step


def linspace(iter_min, iter_max, nbr_of_steps):
    '''Returns nbr_of_steps step values starting with min and ending with
    max, both included in a list.

    **Usage**

    >>> linspace(2, 3, 5)
    [Decimal('2.00'), Decimal('2.25'), Decimal('2.50'), Decimal('2.75'), Decimal('3.00')]
    '''
    return [step for step in linspace_iter(iter_min, iter_max, nbr_of_steps)]


__all__ = [
    'to_decimal',
    'round_decimal',
    'linspace_iter',
    'Vector',
    'SortedKeysDecimalValuedDict',
    'Polynomial',
    'PolyExponents',
    'vector_function',
    'exp',
    'ln',
    'PiecewiseConstant',
    'LinearSpline',
    'NaturalCubicSpline',
    'FinancialCubicSpline',
    'NumericalFirstOrder',
    'NumericalSecondOrder',
    'Solver'
    ]


if __name__ == '__main__':
    import doctest
    doctest.testmod()