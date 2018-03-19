#############################################################################
# The finance package is open source under the `Python Software Foundation  #
# License <http://www.opensource.org/licenses/PythonSoftFoundation.php>`_   #
#############################################################################

'''
**decimalpy.math_constants_and_functions**

This module implements standard mathematical constants and functions build
solely on the type decimal.Decimal, ie it is based on the IEEE standard
854-1987.


It has been decided to use Taylor expansions as a default algorithm.
However if a more efficient algorithm should appear then that one is used.

I've had high hope on getting efficient algorithms based on continued
fractions.
But since I found that (due to Euler) any fractions can be transformed and
vice versa:

.. math::
    c_0 + \\frac{c_1}{1 + \\frac{-\\frac{c_2}{c_1}}{1 + \\frac{c_2}{c_1}}} &= c_0 + \\frac{c_1}{1 - \\frac{c_2}{c_1 + c_2}} \\\\
        &= c_0 + \\frac{c_1}{\\frac{c_1}{c_1 + c_2}} \\\\
        &= c_0 + \\frac{1}{\\frac{1}{c_1 + c_2}} \\\\
        &= c_0 + c_1 + c_2

Since it is easier to evaluate the precision with series than fractions
Taylor expansions are chosen as default.
'''


# -*- coding: utf-8 -*-
from decimal_to_number import Nbr, precision_decorator
from fractions import Fraction


@precision_decorator
def pi():
    pi_last, pi = Nbr(10), Nbr(0)
    a, b, t, p = Nbr(1), Nbr(0.5).sqrt(), Nbr(0.25), Nbr(1)
    while (pi - pi_last).round():
        t, p = t - Nbr(0.25) * p * (a - b) ** 2, 2 * p
        a, b = (a + b) / 2, (a * b).sqrt()
        pi_last, pi = pi, Nbr(0.25) * (a + b) ** 2 / t
    return pi


class PiFraction(Fraction):
    '''
    Tool to convert decimals to fractions of pi.
    Is used to help build trigonometric functions.
    It contains a static method for pi.

    **Usage**

    >>> x = PiFraction(2 * pi() / 3, 2)
    >>> print x, PiFraction(5), x() * 6
    1/3 2pi 995207/625307 pi 12.56637061435917295385057353

    >>> x = PiFraction(200 * pi() / 3)
    >>> print x, x.lowest_fraction()
    200/3 pi 2/3 pi

    >>> x = PiFraction(-100 * pi() / 3)
    >>> print x, x.lowest_fraction()
    -100/3 pi 2/3 pi

    >>> x = PiFraction(-1000  / 7)
    >>> print x, x.lowest_fraction()
    -4445273/97659 pi 47041/97659 pi
    '''
    def __new__(cls, x, pi_scale=1):
        self = super(Fraction, cls).__new__(cls)
        self.pi_scale = Nbr(pi_scale)
        pi_frac = Fraction(Nbr(x) / pi() / self.pi_scale).limit_denominator()
        self._numerator = pi_frac.numerator
        self._denominator = pi_frac.denominator
        return self

    def __str__(self):
        if self.pi_scale == Nbr(1):
            scale = 'pi'
        else:
            scale = '%spi' % self.pi_scale
        return '%s/%s %s' % (self.numerator, self.denominator, scale)

    __repr__ = __str__

    def __call__(self):
        '''Return self as decimal'''
        return pi() / self.denominator * self.numerator * self.pi_scale

    def lowest_fraction(self):
        lowest_fraction = PiFraction(1)
        lowest_fraction._numerator = self.numerator % self.denominator
        lowest_fraction._denominator = self.denominator
        return lowest_fraction


@precision_decorator
def sin(x):
    '''
    *Usage*

    >>> pi = pi()
    >>> sin(0), sin(pi/2), sin(pi), sin(3*pi/2), sin(2*pi)
    (Nbr('0'), Nbr('1'), Nbr('0'), Nbr('-1'), Nbr('0'))
    >>> sin(pi/4) ** 2, sin(pi/6), sin(pi/3) ** 2
    (Decimal('0.5000000000000000000000000000'), Decimal('0.5000000000000000000000000000'), Decimal('0.7499999999999999999999999999'))
    '''
    pi_frac = PiFraction(x, 2).lowest_fraction()
    if pi_frac.denominator == 4:
        if pi_frac.numerator == 1:
            return Nbr(1)
        elif pi_frac.numerator == 3:
            return Nbr(-1)
    elif pi_frac.denominator == 2 and pi_frac.numerator == 1:
        return Nbr(0)
    elif pi_frac.denominator == 1 and pi_frac.numerator == 0:
        return Nbr(0)
    else:
        x_value = pi_frac()
        sine = Nbr(x)
        sine_step = Nbr(x)
        i = Nbr(1)
        while abs(sine_step.round()) != Nbr(0).round():
            i += Nbr(2)
            sine_step = - sine_step * x * x / i / (i - 1)
            sine += Nbr(sine_step)
        return sine


@precision_decorator
def arc_sin(x):
    '''
    *Usage*

    >>> for i in range(13): print i, arc_sin(i / 6. - 1)
    0 -3.141592653589793238462643383
    1 -0.9851107833371426369244089000
    2 -0.7297276562274135770502967072
    3 -0.5235987755982988730771072305
    4 -0.3398369094537683837057992617
    5 -0.1674480792200273922551660223
    6 0.0
    7 0.1674480792200273922551660223
    8 0.3398369094537683837057992617
    9 0.5235987755982988730771072305
    10 0.7297276562274135770502967072
    11 0.9851107833371426369244089000
    12 3.141592653589793238462643383
    '''
    x = Nbr(x)
    if abs(x) == Nbr(1):
        return x * pi()
    elif abs(x) < Nbr(1):
        arc_sine = x
        arc_sine_step = x
        i = Nbr(1)
        while abs(arc_sine_step.round()) != Nbr(0).round():
            i += Nbr(2)
            arc_sine_step = arc_sine_step * (x * (i - 2)) ** 2 / (i - 1) / i
            arc_sine += arc_sine_step
        return arc_sine
    return Nbr('NaN')


if __name__ == '__main__':
    import doctest
    doctest.testmod()