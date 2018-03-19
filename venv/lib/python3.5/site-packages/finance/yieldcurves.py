#############################################################################
# The finance package is open source under the `Python Software Foundation  #
# License <http://www.opensource.org/licenses/PythonSoftFoundation.php>`_   #
#############################################################################

'''
**The module finance.yieldcurves**

The yieldcurves module is build for handling yieldcurves. The design of the
 code makes it easy to implement new yieldcurves.

The key element is _YieldCurveBase class which defines all necessary
 functionality.

A yieldcurves continous forward rate is defined as the sum of one or more
 yieldcurve functions.

All that needs to be added in order to implement is one or more yieldcurve
functions to be used for the calculations and set the __init__ method for the
new yieldcurve.

'''

#. http://stackoverflow.com/questions/533382/dynamic-runtime-method-creation-code-generation-in-python
#. http://stackoverflow.com/questions/4674875/python-function-parameter-count
#. http://code.activestate.com/recipes/82234-importing-a-dynamically-generated-module/

from decimalpy import vector_function as _vector_function, \
     NaturalCubicSpline as _NaturalCubicSpline, \
     FinancialCubicSpline as _FinancialCubicSpline, \
     PiecewiseConstant as _PiecewiseConstant, \
     LinearSpline as _LinearSpline, \
     exp as _exp, \
     NumericalFirstOrder as _slope, \
     NumericalSecondOrder as _curvature, \
     to_decimal as _to_decimal


__all__ = ['FinancialCubicSpline',
           'LinearSpline',
           'NaturalCubicSpline',
           'NelsonSiegel',
           'PiecewiseConstant'
           ]


class _YieldCurveError(Exception):
    '''A class to implement error messages from discount curve classes.'''
    pass


class _YieldCurveBase:
    '''Base class for all yield curves defining all relations between
    calculated values.
    Base is the discrete rate and bond discounting
    Typically a yield curve is defined by a rate function which again is a
    sum of a set of functions.
    Also when including credit risk a yieldcurve is a sum of yieldcurve
    functions.
    '''

    def __init__(self, list_yc_functions=None):
        ''':param list_yc_functions: A list of yield curve functions
        :type list_yc_functions: A list of yield curve functions
        '''
        self._list_yc_functions = []
        assert isinstance(list_yc_functions, (list, tuple)), \
            'Input must be a list or a tuple'
        for yc_function in list_yc_functions:
            self.add_function(yc_function)

    @_vector_function(1, True)
    def __call__(self, t_value):
        '''When an instance of this class is called with a time it returns the
        discountfactor.
        :param t_value: A time value
        :type t_value: a positive integer, float or decimal
        :return: The discount factor at time t_value
        '''
        return self.discount_factor(t_value)

    def __nonzero__(self):
        '''Validates whether the list of yieldcurve functions is empty
        '''
        if self._list_yc_functions:
            return True
        else:
            return False

    def __str__(self):
        '''return a default summary as string representation.
        '''
        return '\n'.join([str(func) for func in self.yieldcurve_functions()])
    __repr__ = __str__

    def add_function(self, yc_function):
        ''':param yc_function: The yc_function to be added
        :type yc_function: A yc_function is a class function with __call__ and
        __str__ specified
        '''
        self._list_yc_functions.append(yc_function)

    def yieldcurve_functions(self):
        ''':return: The list of yieldcurve functions
        '''
        return self._list_yc_functions

    @_vector_function(1, True)
    def continous_forward_rate(self, t_value):
        '''Base method - All other yield calculations are derived from this.
        :param t_value: A time value
        :type t_value: a positive integer, float or decimal
        :return: The continous forward rate at time t_value
        '''
        # Only validating input here
        if self.__nonzero__():
            return sum(f(t_value) for f in self._list_yc_functions)
        else:
            return 0

    @_vector_function(1, True)
    def continous_rate_timeslope(self, t_value):
        return _slope(self.continous_forward_rate)(t_value)

    @_vector_function(1, True)
    def continous_rate_timecurvature(self, t_value):
        return _curvature(self.continous_forward_rate)(t_value)

    @_vector_function(1, True)
    def instantanious_forward_rate(self, t_value):
        ''':param t_value: A time value
        :type t_value: a positive integer, float or decimal
        :return: The instantanious forward rate at time t_value
        '''
        # To be multiplied continous_rate_timeslope t_value be must a _Decimal
        return (t_value * self.continous_rate_timeslope(t_value)
                + self.continous_forward_rate(t_value))

    @_vector_function(1, True)
    def discount_factor(self, t_value):
        ''':param t_value: A time value
        :type t_value: a positive integer, float or decimal
        :return: The discount factor at time t_value
        '''
        if t_value >= 0:
            return _exp(-self.continous_forward_rate(t_value) * t_value)
        else:
            return 0

    @_vector_function(1, True)
    def zero_coupon_rate(self, t_value):
        ''':param t_value: A time value
        :type t_value: a positive integer, float or decimal
        :return: The zero coupon rate at time t_value
        '''
        return _exp(self.continous_forward_rate(t_value)) - 1

    @_vector_function(1, True)
    def discrete_forward_rate(self, t1_value, t2_value):
        ''':param t1_value: A time value
        :type t1_value: a positive integer, float or decimal,
                        t1_value < t2_value
        :param t2_value: A time value
        :type t2_value: a positive integer, float or decimal,
                        t1_value < t2_value
        :return: The discrete forward rate between time t1_value and t2_value
        '''
        rate1 = self.continous_forward_rate(t1_value)
        rate2 = self.continous_forward_rate(t2_value)
        average_rate = ((t2_value * rate2 - t1_value * rate1)
                        / (t2_value - t1_value))
        return _exp(average_rate) - 1


class NelsonSiegel(object, _YieldCurveBase):
    '''The Nelson Siegel defined with a level, slope, curvature and scale
    parameters.

    Instantiated by:

    :param level: A constant level in the definition
    :type level: a integer, float or decimal
    :param slope: The parameter for the slope contribution
    :type slope: a integer, float or decimal
    :param curvature: The parameter for the curvature contribution
    :type curvature: a integer, float or decimal
    :param scale: The parameter for the scale contribution
    :type scale: a integer, float or decimal


    **How to use:**

    Instantiate:

    >>> import finance
    >>> ns = finance.yieldcurves.NelsonSiegel(0.061, -0.01, -0.0241, 0.275)

    See the settings:

    >>> ns
    Nelson Siegel (level=0.061, slope=-0.01, curvature=-0.0241, scale=0.275)

    Get the discountfactors at times 1, 2, 5, 10:

    >>> times = [1, 2, 5, 10]
    >>> ns(times)
    Vector([0.9517121708497056177816078083, 0.9072377300179418172521412527, 0.7844132592062346545344544940, 0.6008958407659500402742872859])

    Get the zero coupon rate at time 5 and 7

    >>> r5, r7 = ns.zero_coupon_rate([5, 7])
    >>> r5, r7
    (Decimal('0.049762403554685553400657196'), Decimal('0.050625188777310061599365592'))

    Get the forward rate between time 5 and 7

    >>> f5_7 = ns.discrete_forward_rate(5, 7)
    >>> f5_7
    Decimal('0.052785255470657667493924028')

    Verify the results:

    >>> (1 + r5) ** 5 * (1 + f5_7) ** 2
    Decimal('1.412975598166187290121638358')

    >>> (1 + r7) ** 7
    Decimal('1.412975598166187290121638354')

    Only the last decimal differ!
    '''
    # An Arbitrage-Free Generalized Nelson-Siegel Term Structure Model - PDF
    def __init__(self, level, slope, curvature, scale):
        ''':param level: A constant level in the definition
        :type level: a integer, float or decimal
        :param slope: The parameter for the slope contribution
        :type slope: a integer, float or decimal
        :param curvature: The parameter for the curvature contribution
        :type curvature: a integer, float or decimal
        :param scale: The parameter for the scale contribution
        :type scale: a integer, float or decimal
        '''
        self.level = _to_decimal(level)
        self.slope = _to_decimal(slope)
        self.curvature = _to_decimal(curvature)
        self.scale = _to_decimal(scale)
        function_list = [self.Level, self.Slope, self.Curvature]
        _YieldCurveBase.__init__(self, function_list)

    #@staticmethod
    #def from_zerocoupon_points(x_data, y_data):
    #    pass

    def __str__(self):
        return 'Nelson Siegel (level=%s, slope=%s, curvature=%s, scale=%s)' \
                % (self.level, self.slope, self.curvature, self.scale)

    __repr__ = __str__

    @_vector_function(1, True)
    def Level(self, t_value):
        ''':param t_value: A time value
        :type t_value: a positive integer, float or decimal
        :return: The Level in a nelson Siegel curve at time t_value
        '''
        return self.level

    @_vector_function(1, True)
    def Slope(self, t_value):
        ''':param t_value: A time value
        :type t_value: a positive integer, float or decimal
        :return: The Slope in a nelson Siegel curve at time t_value
        '''
        weight = t_value * self.scale
        if weight:
            return self.slope * (1 - _exp(-weight)) / weight
        else:
            return self.slope

    @_vector_function(1, True)
    def Curvature(self, t_value):
        ''':param t_value: A time value
        :type t_value: a positive integer, float or decimal
        :return: The curvature in a nelson Siegel curve at time t_value
        '''
        weight = t_value * self.scale
        if weight:
            return (self.curvature * ((1 - _exp(-weight)) / weight
                    - _exp(-weight)))
        else:
            return 0


class NaturalCubicSpline(_YieldCurveBase):
    '''The NaturalCubicSpline is the spline where the curvatures are set to
    0 at extrapolation.
    This means that the extrapolation is a straight line with slope as the one
    at endpoints.

    Instantiated by:

    :param times: Times at which continous forward rates are observed.
    :type times: a list of positive integers, floats or decimals
    :param continous_forward_rates: The parameter for the slope contribution
    :type continous_forward_rates: a list of positive integers,
                                    floats or decimals

    **How to use:**

    Instantiate:

    >>> import finance
    >>> times = [0.5, 1, 2, 4, 5, 10, 15, 20]
    >>> rates = [0.0552, 0.06, 0.0682, 0.0801, 0.0843, 0.0931, 0.0912, 0.0857]
    >>> ncs = finance.yieldcurves.NaturalCubicSpline(times, rates)

    See the settings:

    >>> ncs
    Natural cubic spline based on points:
    .. (0.5000, 0.0552)
    .. (1.0000, 0.0600)
    .. (2.0000, 0.0682)
    .. (4.0000, 0.0801)
    .. (5.0000, 0.0843)
    .. (10.0000, 0.0931)
    .. (15.0000, 0.0912)
    .. (20.0000, 0.0857)

    Getting the continous forward rate:

    >>> print ncs.continous_forward_rate(times[:3])
    Vector([0.05520000000000000000000000000, 0.06000000000000000000000000000, 0.06820000000000000000000000000])

    Getting the slope of the continous forward rate at time 1

    >>> print ncs.continous_rate_timeslope(1)
    0.009216950866030399434428966667

    Getting the instantanous forward rate at time 1

    >>> print ncs.instantanious_forward_rate(1)
    0.06921695086603039943442896667
    '''
    def __init__(self, times, continous_forward_rates):
        ''':param times: Times at which continous forward rates are observed.
        :type times: a list of positive integers, floats or decimals
        :param continous_forward_rates: The parameter for the slope
                                            contribution
        :type continous_forward_rates: a list of positive integers,
                                            floats or decimals
        '''
        assert any(time >= 0 for time in times), 'Times must be non negative'
        _YieldCurveBase.__init__(self,
            [_NaturalCubicSpline(times, continous_forward_rates)]
            )


class FinancialCubicSpline(_YieldCurveBase):
    '''The FinancialCubicSpline is the spline where the curvatures are set to 0
    at extrapolation.
    This means that the extrapolation is a horizontal straight line at the
    endpoint far to the right.

    Instantiated by:

    :param times: Times at which continous forward rates are observed.
    :type times: a list of positive integers, floats or decimals
    :param continous_forward_rates: The parameter for the slope contribution
    :type continous_forward_rates: a list of positive integers,
                                    floats or decimals

    **How to use:**

    Instantiate:

    >>> import finance
    >>> times = [0.5, 1, 2, 4, 5, 10, 15, 20]
    >>> rates = [0.0552, 0.06, 0.0682, 0.0801, 0.0843, 0.0931, 0.0912, 0.0857]
    >>> fcs = finance.yieldcurves.FinancialCubicSpline(times, rates)

    See the settings:

    >>> fcs
    Financial cubic spline based on points:
    .. (0.5000, 0.0552)
    .. (1.0000, 0.0600)
    .. (2.0000, 0.0682)
    .. (4.0000, 0.0801)
    .. (5.0000, 0.0843)
    .. (10.0000, 0.0931)
    .. (15.0000, 0.0912)
    .. (20.0000, 0.0857)
    '''
    def __init__(self, times, continous_forward_rates):
        ''':param times: Times at which continous forward rates are observed.
        :type times: a list of positive integers, floats or decimals
        :param continous_forward_rates: The parameter for the slope
                                        contribution
        :type continous_forward_rates: a list of positive integers,
                                        floats or decimals
        '''
        assert any(time >= 0 for time in times), 'Times must be non negative'
        _YieldCurveBase.__init__(self,
            [_FinancialCubicSpline(times, continous_forward_rates)]
            )


class PiecewiseConstant(_YieldCurveBase):
    '''This yield curve is right continous and piecewise constant. The curve is
    instantiated by a set of right endpoints for each step in the curve.
    If time 0 isn't present in the set of times the point (0, 0) is added.

    Instantiated by:

    :param times: Times at which continous forward rates are observed.
    :type times: a list of positive integers, floats or decimals
    :param continous_forward_rates: The parameter for the slope contribution
    :type continous_forward_rates: a list of positive integers,
                                    floats or decimals

    **How to use:**

    Instantiate:

    >>> import finance
    >>> times = [0.5, 1, 2, 4, 5, 10, 15, 20]
    >>> rates = [0.0552, 0.06, 0.0682, 0.0801, 0.0843, 0.0931, 0.0912, 0.0857]
    >>> pc = finance.yieldcurves.PiecewiseConstant(times, rates)

    See the settings:

    >>> pc
    Piecewise constant curve based on points:
    .. (0.0000, 0.0000)
    .. (0.5000, 0.0552)
    .. (1.0000, 0.0600)
    .. (2.0000, 0.0682)
    .. (4.0000, 0.0801)
    .. (5.0000, 0.0843)
    .. (10.0000, 0.0931)
    .. (15.0000, 0.0912)
    .. (20.0000, 0.0857)

    >>> print pc.continous_forward_rate(times[:4])
    Vector([0.0552, 0.06, 0.0682, 0.0801])

    Getting the slope of the continous forward rate at time 1 (at a jump)
    and at time 1.1:

    >>> print pc.continous_rate_timeslope([1, 1.1])
    Vector([47.83333333333333333333333333, 0])

    Getting the instantanous forward rate at time 1 (at a jump) and at
    time 1.1:

    >>> print pc.instantanious_forward_rate([1, 1.1])
    Vector([47.89333333333333333333333333, 0.0682])
    '''
    def __init__(self, times, continous_forward_rates):
        ''':param times: Times at which continous forward rates are observed.
        :type times: a list of positive integers, floats or decimals
        :param continous_forward_rates: The parameter for the slope
                                        contribution
        :type continous_forward_rates: a list of positive integers,
                                        floats or decimals
        '''
        assert any(time >= 0 for time in times), 'Times must be non negative'
        if 0 not in times:
            times = [0] + times
            continous_forward_rates = [0] + continous_forward_rates
        pc = _PiecewiseConstant(times, continous_forward_rates)
        _YieldCurveBase.__init__(self, [pc])


class LinearSpline(_YieldCurveBase):
    '''This yield curve is right continous and piecewise constant. The curve is
    instantiated by a set of right endpoints for each step in the curve.
    If time 0 isn't present in the set of times the point (0, 0) is added.

    Instantiated by:

    :param times: Times at which continous forward rates are observed.
    :type times: a list of positive integers, floats or decimals
    :param continous_forward_rates: The parameter for the slope contribution
    :type continous_forward_rates: a list of positive integers,
                                    floats or decimals

    **How to use:**

    Instantiate:

    >>> import finance
    >>> times = [0.5, 1, 2, 4, 5, 10, 15, 20]
    >>> rates = [0.0552, 0.06, 0.0682, 0.0801, 0.0843, 0.0931, 0.0912, 0.0857]
    >>> li = finance.yieldcurves.LinearSpline(times, rates)

    See the settings:

    >>> li
    Linear interpolation curve based on points:
    .. (0.0000, 0.0000)
    .. (0.5000, 0.0552)
    .. (1.0000, 0.0600)
    .. (2.0000, 0.0682)
    .. (4.0000, 0.0801)
    .. (5.0000, 0.0843)
    .. (10.0000, 0.0931)
    .. (15.0000, 0.0912)
    .. (20.0000, 0.0857)

    >>> print li.continous_forward_rate(times[:4])
    Vector([0.0552, 0.0600, 0.0682, 0.0801])

    Getting the slope of the continous forward rate at time 1 (at a jump)
    and at time 1.1:

    >>> print li.continous_rate_timeslope([1, 1.1])
    Vector([0.0089, 0.0082])

    Getting the instantanous forward rate at time 1 (at a jump) and at
    time 1.1:

    >>> print li.instantanious_forward_rate([1, 1.1])
    Vector([0.0689, 0.06984])
    '''
    def __init__(self, times, continous_forward_rates):
        ''':param times: Times at which continous forward rates are observed.
        :type times: a list of positive integers, floats or decimals
        :param continous_forward_rates: The parameter for the slope
                                        contribution
        :type continous_forward_rates: a list of positive integers,
                                        floats or decimals
        '''
        assert any(time >= 0 for time in times), 'Times must be non negative'
        if 0 not in times:
            _YieldCurveBase.__init__(self,
                [_LinearSpline([0] + times, [0] + continous_forward_rates)]
                )
        else:
            _YieldCurveBase.__init__(self,
                [_LinearSpline(times, continous_forward_rates)]
                )


if __name__ == '__main__':
    import doctest
    doctest.testmod()