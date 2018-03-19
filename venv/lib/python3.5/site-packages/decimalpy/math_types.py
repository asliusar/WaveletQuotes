#############################################################################
# The finance package is open source under the `Python Software Foundation  #
# License <http://www.opensource.org/licenses/PythonSoftFoundation.php>`_   #
#############################################################################

'''
**The decimalpy.mathtypes**

This module contains the Decimal subtype Vector and the decorator
vector_function that converts a simple function into a Vector
function ie a function that can handle and return a Vector.

Finally the module contains a base class for a Decimal valued dictionary with
sorted keys.
'''
from decimal import Decimal
from mathematical_meta_code import CummutativeAddition, \
                                   CummutativeMultiplication, Power
from math_meta_functions import Solver


def vector_function(variable_index, argument_is_decimal=False):
    '''A decorator to convert python functions to numpy universal functions

    A standard function of 1 variable is extended by a decorator to handle
    all values in a list or tuple

    :param variable_index: Specifies index for args to use as variable.
        This way the function can be used in classes as well as functions
    :type variable_index: An positive integer

    **How to use:**

    In the example below vector_function is used on the first
    parameter x:

    >>> from decimal import Decimal
    >>> @vector_function(0)
    ... def test(x, y=2):
    ...     return x+y
    ...
    >>> x0 = 4
    >>> x1 = (1, float(2), Decimal('3'))
    >>> x2 = [2, 3, 4]
    >>> x3 = Vector(x1) + 2
    >>> test(x0)
    Decimal('6')
    >>> print test(x1)
    Vector([3, 4.0, 5])
    >>> print test(x2)
    Vector([4, 5, 6])
    >>> print test(x3)
    Vector([5, 6.0, 7])

    Note that since argument y has a default value 2 it isn't set in the
    function call. So these are not handled by the vector_function.
    To see this do:

    >>> @vector_function(1)
    ... def test(x, y=2):
    ...     return x+y
    ...
    >>> try:
    ...     test(1)
    ... except Exception, error_tekst:
    ...     print error_tekst
    ...
    tuple index out of range
    * variable_index=1
    * args=(1,)
    * kwargs={}
    * argument_is_decimal=False

    In the example above args is a tuple of length 1, we want's to let the
    vector_function work on argument Decimal 2 at position 1, but
    there are no argument Decimal 2 in the call.

    However the call below works just fine:

    >>> test(1, (1, float(2), Decimal('3')))
    Vector([2, 3.0, 4])

    It is just that the value has to be set in the function call in order to
    have vector_function working.
    Therefore setting a default value make's no sense.

    If argument_is_decimal is True it means that the argument is transformed
    into a Decimal if possible  else the value is returned.

    >>> @vector_function(0)
    ... def test(x):
    ...     return 2/x
    ...
    >>> test(3)
    Decimal('0')

    Here the division becomes integer part division since the argument is an
    integer and hence both nominator and denominator are integers.

    If on the other hand argument_is_decimal is True the argument becomes a
    Decimal and division becomes division between real Decimals as shown
    below:

    >>> @vector_function(0, True)
    ... def test(x):
    ...     return 2/x
    ...
    >>> test(3)
    Decimal('0.6666666666666666666666666667')

    Remember that arguments at instantiation must be decimals. Hence use of
    the function Decimal in __init__

    >>> class Test:
    ...     def __init__(self, x):
    ...         self.x = Decimal(x)
    ...     @vector_function(1, True)
    ...     def __call__(self, y):
    ...        return self.x * y
    ...
    >>> test = Test(2.)
    >>> test([3., 6, 9])
    Vector([6.0, 12, 18])
    '''
    def real_vector_function(old_function):
        '''Function to replace old_function
        '''

        def wrap_func(*args, **kwargs):
            '''Function specifying that input and output is decimal.
            '''

            def to_decimal(x_value):
                if argument_is_decimal:
                    if isinstance(x_value, (int, float, Decimal)):
                        return Decimal(str(x_value))
                return x_value

            try:
                if len(args) >= variable_index:
                    before = list(args[:variable_index])
                    arguments = args[variable_index]
                    after = list(args[variable_index + 1:])
                    if isinstance(arguments, (list, tuple, Vector)):
                        return Vector([old_function(*(before
                                                     + [to_decimal(x)]
                                                     + after)
                                                    )
                                                for x in arguments
                                        ])
                    elif isinstance(arguments, (int, float, Decimal)):
                        return Decimal('%s' % old_function(*(before
                                                            + [to_decimal(arguments)]
                                                            + after)
                                                            )
                                       )
            except Exception, error_text:
                raise Exception('%s\n* variable_index=%s\n' \
                                '* args=%s\n' \
                                '* kwargs=%s\n' \
                                '* argument_is_decimal=%s'
                                % (error_text,
                                   variable_index,
                                   args,
                                   kwargs,
                                   argument_is_decimal
                                   )
                                )
            return Decimal('%s' % old_function(*args))
        wrap_func.__name__ = old_function.__name__
        wrap_func.__doc__ = old_function.__doc__
        wrap_func.__module__ = old_function.__module__
        return wrap_func
    return real_vector_function


class Vector(CummutativeAddition,
             CummutativeMultiplication,
             Power,
             list
             ):
    '''An abstract datatype integrating the qualities of numpy's array
    and the class decimal.s

    **How to use**

    >>> cf = Vector(5, 0.1)
    >>> cf[-1] += 1
    >>> cf
    Vector([0.1, 0.1, 0.1, 0.1, 1.1])
    >>> times = Vector(range(1,6))
    >>> discount = Decimal('1.1') ** - times
    >>> sum(discount * cf) # Present value
    Decimal('1.000000000000000000000000000')
    >>> discount(cf) # Present value by dot product
    Decimal('1.000000000000000000000000000')
    >>> sum(cf * Decimal('1.1') ** - times) # Present value
    Decimal('1.000000000000000000000000000')
    >>> cf(Decimal('1.1') ** - times) # Present value by dot product
    Decimal('1.000000000000000000000000000')
    >>> sum(cf / Decimal('1.1') ** times) # Present value
    Decimal('1.000000000000000000000000000')
    >>> times[:4] - times[1:]
    Vector([-1, -1, -1, -1])
    '''
    def __init__(self, tuple_or_length, default=1):
        if isinstance(tuple_or_length, int) and tuple_or_length > 0:
            list.__init__(self, [Decimal(str(default))] * tuple_or_length)
        elif isinstance(tuple_or_length, (tuple, list)):
            list.__init__(self, [Decimal(str(val)) for val in tuple_or_length])
        elif tuple_or_length.__class__.__name__ == 'Vector':
            self = tuple_or_length
        else:
            list.__init__(self, [])

    def __str__(self):
        return 'Vector([%s])' % ', '.join([str(x) for x in self])

    def __call__(self, d_vector):  # Vector dot product
        '''Vector dot product can be considered as a function with rhs of the
        dot as the argument whereas the lhs is the "matrix"
        '''
        return sum(self * d_vector)

    __repr__ = __str__

    def __getslice__(self, start, stop):
        return Vector(list.__getslice__(self, start, stop))

    def __setitem__(self, key, value):
        list.__setitem__(self, key, Decimal(value))

    def __setslice__(self, start, stop, values):
        list.__setslice__(self, start, stop, Vector(values))

    def __neg__(self):
        return Vector([-1 * x for x in self])

    def __abs__(self):
        return Vector([abs(x) for x in self])

    def __add__(self, d_vector):
        if isinstance(d_vector, (int, float, Decimal)):
            d_vector = len(self) * [Decimal(str(d_vector))]
        elif isinstance(d_vector, (tuple, list)):
            assert any(isinstance(val, (int, float, Decimal)) for val in
                            d_vector), 'list must be list of Decimals'
            d_vector = [Decimal(val) for val in d_vector]
        assert len(self) == len(d_vector), \
                'Vectors must have same length'
        if isinstance(d_vector, (Vector, list)):
            return Vector([x + y for x, y in zip(self, d_vector)])
        elif isinstance(d_vector, SortedKeysDecimalValuedDict):
            return d_vector.__radd__(self)

    def __mul__(self, d_vector):
        if isinstance(d_vector, (int, float, Decimal)):
            d_vector = len(self) * [Decimal(d_vector)]
        elif isinstance(d_vector, (tuple, list)):
            assert any(isinstance(val, (int, float, Decimal)) for val in
                            d_vector), 'list must be list of Decimals'
            d_vector = [Decimal(val) for val in d_vector]
        assert len(self) == len(d_vector), \
                'Vectors must have same length'
        if isinstance(d_vector, (Vector, list)):
            return Vector([x * y for x, y in zip(self, d_vector)])
        elif isinstance(d_vector, SortedKeysDecimalValuedDict):
            return d_vector.__rmul__(self)

    def __div__(self, d_vector):
        if isinstance(d_vector, (int, float, Decimal)):
            d_vector = len(self) * [Decimal(d_vector)]
        elif isinstance(d_vector, (tuple, list)):
            assert any(isinstance(val, (int, float, Decimal)) for val in
                            d_vector), 'list must be list of Decimals'
            d_vector = [Decimal(val) for val in d_vector]
        assert len(self) == len(d_vector), \
                'Vectors must have same length'
        if isinstance(d_vector, (Vector, list)):
            return Vector([x / y for x, y in zip(self, d_vector)])
        elif isinstance(d_vector, SortedKeysDecimalValuedDict):
            return d_vector.__rdiv__(self)

    def __rdiv__(self, d_vector):
        if isinstance(d_vector, (int, float, Decimal)):
            d_vector = len(self) * [Decimal(d_vector)]
        elif isinstance(d_vector, (tuple, list)):
            assert any(isinstance(val, (int, float, Decimal)) for val in
                            d_vector), 'list must be list of Decimals'
            d_vector = [Decimal(val) for val in d_vector]
        assert len(self) == len(d_vector), \
                'Vectors must have same length'
        if isinstance(d_vector, (Vector, list)):
            return Vector([x / y for x, y in zip(d_vector, self)])
        elif isinstance(d_vector, SortedKeysDecimalValuedDict):
            return d_vector.__div__(self)

    def __pow__(self, d_vector):
        if isinstance(d_vector, (int, float, Decimal)):
            d_vector = len(self) * [Decimal(d_vector)]
        elif isinstance(d_vector, (tuple, list)):
            assert any(isinstance(val, (int, float, Decimal)) for val in
                            d_vector), 'list must be list of Decimals'
            d_vector = [Decimal(val) for val in d_vector]
        if isinstance(d_vector, (Vector, list)):
            assert len(self) == len(d_vector), \
                    'Vectors must have same length'
            return Vector([x ** y for x, y in zip(self, d_vector)])

    def __rpow__(self, d_vector):
        if isinstance(d_vector, (int, float, Decimal)):
            d_vector = len(self) * [Decimal(d_vector)]
        elif isinstance(d_vector, (tuple, list)):
            assert any(isinstance(val, (int, float, Decimal)) for val in
                            d_vector), 'list must be list of Decimals'
            d_vector = [Decimal(val) for val in d_vector]
        if isinstance(d_vector, (Vector, list)):
            assert len(self) == len(d_vector), \
                    'Vectors must have same length'
            return Vector([x ** y for x, y in zip(d_vector, self)])


class SortedKeysDecimalValuedDict(CummutativeAddition,
                                  CummutativeMultiplication,
                                  dict
                                  ):
    '''SortedKeysDecimalValuedDict is a generalisation of Vector. The
    later is a SortedKeysDecimalValuedDict where the keys are consequtive
    integers starting with zero.

    In SortedKeysDecimalValuedDict the keys can be any ordered set of elements
    of the same type.

    The values are off course still Decimals. And the vectorlike functionality
    is still valid if the keys are of the same type.

    Arguments at instantiation should be:

    * a SortedKeysDecimalValuedDict
    * a Vector
    * a dictionary where the values are decimals
    * a list of pairs of key and value. Values are of type Decimals

    The type setting of keys can be defined at the static method
    __validate_key__ which has to return an validated value if possible.
    Otherwise it has to return the value None.

    So to create a SortedKeysDecimalValuedDict with keys converted to strings
    eg just do:

    >>> class string_based_Vector(SortedKeysDecimalValuedDict):
    ...     @staticmethod
    ...     def __validate_key__(key):
    ...         return str(key)

    Now any attempted key is converted to it's string representation.


    **How to use**

    >>> class TimeFlow(SortedKeysDecimalValuedDict):
    ...     @staticmethod
    ...     def __validate_key__(key):
    ...         return SortedKeysDecimalValuedDict.__validate_value__(key)
    ...

    >>> cf = TimeFlow(Vector(5, 0.1))
    >>> cf[4] += 1 # This is not the index 4, but the key 4
    >>> cf
    Data for the TimeFlow:
    * key: 0, value: 0.1
    * key: 1, value: 0.1
    * key: 2, value: 0.1
    * key: 3, value: 0.1
    * key: 4, value: 1.1

    >>> times = TimeFlow(Vector(range(1,6)))
    >>> -times
    Data for the TimeFlow:
    * key: 0, value: -1
    * key: 1, value: -2
    * key: 2, value: -3
    * key: 3, value: -4
    * key: 4, value: -5
    >>> discount = Decimal('1.1') ** - times
    >>> discount
    Data for the TimeFlow:
    * key: 0, value: 0.9090909090909090909090909091
    * key: 1, value: 0.8264462809917355371900826446
    * key: 2, value: 0.7513148009015777610818933133
    * key: 3, value: 0.6830134553650706918926302848
    * key: 4, value: 0.6209213230591551744478457135
    >>> present_values = discount * cf
    >>> sum(present_values.values()) # Present value
    Decimal('1.000000000000000000000000000')
    '''
    def __init__(self, init_arg={}, reverse=False):
        self.reverse = reverse
        pairs = []
        if isinstance(init_arg, self.__class__):
            pairs = init_arg.iteritems()
        elif isinstance(init_arg, dict):
            pairs = init_arg.iteritems()
        elif isinstance(init_arg, Vector):
            l = len(init_arg) + 1
            pairs = zip(range(l), init_arg)
        outdict = {}
        for key, value in pairs:
            key = self.__validate_key__(key)
            value = self.__validate_value__(value)
            if key != None and value != None:
                outdict[key] = value
        dict.__init__(self,  outdict)

    @staticmethod
    def __validate_key__(key):
        raise NotImplementedError(
                '__validate_key__ must always be implemented'
                )

    @staticmethod
    def __validate_value__(value):
        if isinstance(value, (int, float, Decimal)):
            return Decimal(str(value))

    def keys(self):
        return sorted(dict.keys(self), reverse=self.reverse)

    def values(self):
        return Vector([self[key] for key in self.keys()])

    def items(self):
        return [(key, self[key]) for key in self.keys()]

    def iterkeys(self):
        for key in self.keys():
            yield key

    def itervalues(self):
        for key in self.keys():
            yield self[key]

    def iteritems(self):
        for key in self.keys():
            yield (key, self[key])

    def last_key(self):
        return self.keys()[-1]

    def first_key(self):
        return self.keys()[0]

    def __getitem__(self,  key):
        if isinstance(key, slice):
            # slice = [key.start, key.stop]
            if key.start == None:
                first_key = self.first_key()
            else:
                first_key = self.__validate_key__(key.start)
            if key.stop == None:
                last_key = self.last_key()
            else:
                last_key = self.__validate_key__(key.stop)
            if first_key and last_key and first_key <= last_key:
                dct = dict([(key, value) for key, value in self.items()
                        if first_key <= key <= last_key
                        ])
                return self.__class__(dct, reverse=self.reverse)
            else:
                return self.__class__({}, reverse=self.reverse)
        elif self.__validate_key__(key) in self.keys():
            return dict.__getitem__(self,  self.__validate_key__(key))

    def __setitem__(self,  key,  value):
        key = self.__validate_key__(key)
        value = self.__validate_value__(value)
        if key != None and value != None:
            dict.__setitem__(self,  key,  value)

    def __str__(self):
        content = '\n* '.join(sorted(['key: %s, value: %s' % (key, value)
                                    for key, value in self.items()]))
        return 'Data for the %s:\n* %s' % (self.__class__.__name__, content)

    __repr__ = __str__

    def __add__(self, value):
        out = self.__class__(self)
        if isinstance(value, self.__class__):
            for key in value.keys():
                if key in out.keys():
                    out[key] += value[key]
                else:
                    out[key] = value[key]
        elif isinstance(value, Vector) and len(self) == len(value):
            out = self.__class__(self)
            for key, val in zip(out.keys(), out.values() + value):
                out[key] = val
        else:
            value = self.__validate_value__(value)
            if value:
                for key in out.keys():
                    out[key] += value
        return out

    def __mul__(self, value):
        out = self.__class__(self)
        if isinstance(value, self.__class__) and self.keys() == value.keys():
            # multiplication with a SortedKeysDecimalValuedDict is not
            # possible unless same set of keys
            for key in out.keys():
                out[key] *= value[key]
        elif isinstance(value, Vector) and len(self) == len(value):
            out = self.__class__(self)
            for key, val in zip(out.keys(), out.values() * value):
                out[key] = val
        else:
            value = self.__validate_value__(value)
            if value:
                for key in out.keys():
                    out[key] *= value
        return out

    def __neg__(self):
        out = self.__class__(self)
        for key, value in out.items():
            out[key] = - value
        return out

    def __abs__(self):
        out = self.__class__(self)
        for key, value in out.items():
            out[key] = abs(value)
        return out

    def __rsub__(self, value):
        out = self.__class__({})
        if isinstance(value, self.__class__):
            for key in self.keys():
                if key in value.keys():
                    out[key] = value[key] - self[key]
                else:
                    out[key] = -self[key]
        elif isinstance(value, Vector) and len(self) == len(value):
            out = self.__class__(self)
            for key, val in zip(out.keys(), value - self.values()):
                out[key] = val
        else:
            value = self.__validate_value__(value)
            if value:
                for key in self.keys():
                    out[key] = value - self[key]
        return out

    @staticmethod
    def _decimal_division__(numerator, denominator):
        '''Standardize division. If denominator is zero, Decimal('NaN') is
        returned
        '''
        if isinstance(numerator, Decimal) and isinstance(denominator, Decimal):
            if denominator != Decimal('0'):
                return numerator / denominator
        return Decimal('NaN')

    def __div__(self, value):
        out = self.__class__(self)
        if (isinstance(value, self.__class__)
          and self.keys() == value.keys()):
            for key in self.keys():
                out[key] = self._decimal_division_(self[key], value[key])
        elif isinstance(value, Vector) and len(self) == len(value):
            out = self.__class__(self)
            for key, val in zip(out.keys(), out.values() / value):
                out[key] = val
        else:
            value = self.__validate_value__(value)
            if value:
                for key in self.keys():
                    out[key] = self._decimal_division_(self[key], value)
        return out

    def __rdiv(self, value):
        out = self.__class__(self)
        if (isinstance(value, self.__class__)
          and self.keys() == value.keys()):
            for key in self.keys():
                out[key] = decimal_division(self[key], value[key])
        elif isinstance(value, Vector) and len(self) == len(value):
            out = self.__class__(self)
            for key, val in zip(out.keys(), value / out.values()):
                out[key] = val
        else:
            value = self.__validate_value__(value)
            if value:
                for key in self.keys():
                    out[key] = self._decimal_division_(self[key], value)
        return out

    @staticmethod
    def _decimal_power_(base, exponent):
        exponent = Decimal(exponent)
        if exponent == Decimal('0'):
            return Decimal('1')
        elif base == Decimal('0'):
            return Decimal('0')
        else:
            if base >= Decimal('0'):
                return base ** exponent
            else:
                if exponent._isinteger():
                    return base ** exponent

    def __pow__(self, value):
        out = self.__class__(self)
        if (isinstance(value, self.__class__)
          and self.keys() == value.keys()):
            for key in self.keys():
                out[key] = self._decimal_power_(self[key], value[key])
        else:
            value = self.__validate_value__(value)
            if value:
                for key in self.keys():
                    out[key] = self._decimal_power_(self[key], value)
        return out

    def __rpow__(self, value):
        out = self.__class__(self)
        if (isinstance(value, self.__class__)
          and self.keys() == value.keys()):
            for key in self.keys():
                out[key] = self._decimal_power_(value[key], self[key])
        else:
            value = self.__validate_value__(value)
            if value != None:
                for key in self.keys():
                    out[key] = self._decimal_power_(value, self[key])
        return out


class Polynomial(SortedKeysDecimalValuedDict):
    '''Polynomials has exponents as integers and factors as decimals.

    It uses an extended Horners method for evaluation.
    And derivatives can found exact by specifying a degree of differention.

    The price paid for this extension is that PolyExponents can only have
    positive arguments.

    **At instantiation:**

    :param dct_of_exponents_and_factors: Array of x-coordinates
    :type dct_of_exponents_and_factors: A dictionary where the keys
        are exponents and the values are factors.

    **When called as a function**

    :param base_value: Specifying the degree of differention
    :type base_value: A Decimal (Integer, float or Decimal)
    :return: When called as a function returns the functional value.
        If a degree is specified then the degree order derivative is returned

    **How to use:**

    Let's start with a simple polynomial: :math:`p(x)=x^2 + 2 \cdot x + 2`.
    Then the dct_of_exponents_and_factors is {2:1, 1:2, 0:2}.
    The dct_of_exponents_and_factors of the first derivative is {1:2, 0:2}.
    And the dct_of_exponents_and_factors of the first derivative is {0:2}.

    Instantiation is done as:

    >>> pe = Polynomial({2:1, 1:2, 0:2})
    >>> print pe
    <Polynomial(x^2 + 2 x + 2)>

    >>> pe
    <Polynomial(x^2 + 2 x + 2)>

    >>> pe.derivative()
    <Polynomial(2 x + 2)>

    >>> pe.derivative().derivative()
    <Polynomial(2)>

    >>> pe.derivative().integral()
    <Polynomial(x^2 + 2 x)>

    >>> pe.derivative().integral(-5)
    <Polynomial(x^2 + 2 x - 5)>

    >>> -pe
    <Polynomial(- x^2 - 2 x - 2)>

    >>> Polynomial({}), pe + (-pe), pe - pe
    (<Polynomial(0)>, <Polynomial(0)>, <Polynomial(0)>)

    >>> pe * 2
    <Polynomial(2 x^2 + 4 x + 4)>

    >>> pe + pe
    <Polynomial(2 x^2 + 4 x + 4)>

    >>> pe * pe
    <Polynomial(x^4 + 4 x^3 + 8 x^2 + 8 x + 4)>

    >>> pe ** 2
    <Polynomial(x^4 + 4 x^3 + 8 x^2 + 8 x + 4)>

    >>> Polynomial({1:1, 0:1}) ** 5
    <Polynomial(x^5 + 5 x^4 + 10 x^3 + 10 x^2 + 5 x + 1)>

    Get function value at x = -1  and 1 and the first order derivative and
    second order derivative at x = 1:

    >>> pe([-1, 1]), pe.derivative()(1), pe.derivative().derivative()(1)
    (Vector([1, 5]), Decimal('4'), Decimal('2'))

    >>> pe[1] = 0
    >>> pe
    <Polynomial(x^2 + 2)>

    >>> pe = Polynomial({1:1, 0:1}) ** 3
    >>> pe(2)
    Decimal('27')
    >>> pe.inverse(27)
    Decimal('2.000000000000000000000000000')

    >>> pe = Polynomial({2:1, 1:1}) ** 2
    >>> pe(2)
    Decimal('36')

    >>> pe =Polynomial({0:1, -1:1, -2:1, 1:2})
    >>> pe
    <Polynomial(2 x + 1)>
    >>> pe(2)
    Decimal('5')
    '''
    def __init__(self, exponents_and_factors, variable='x'):
        self._variable = str(variable)
        SortedKeysDecimalValuedDict.__init__(self,
                                             exponents_and_factors,
                                             True
                                             )
        for exponent, factor in self.items():
            if not (factor or not exponent):
                del self[exponent]
        if self == {}:
            self[0] = 0

    @staticmethod
    def __validate_key__(key):
        if isinstance(key, int) and key >= 0:
            return key

    def to_latex(self, reverse=True):
        get_sign = lambda nbr: '+' if nbr >= 0 else '-'
        latex = ''
        for exponent, factor in sorted(self.items(), reverse=reverse):
            sign = get_sign(factor)
            if abs(factor) != Decimal('1'):
                latex += ' %s %s' % (sign, abs(factor))
            else:
                latex += ' %s' % sign
            if exponent == self.__validate_key__(1):
                latex += ' %s' % self._variable
            elif exponent:
                latex += ' %s^%s' % (self._variable, exponent)
            elif abs(factor) == Decimal('1'):
                latex += ' %s' % abs(factor)
        if latex[1] == '+':
            latex = latex[3:]
        else:
            latex = latex[1:]
        return '<%s(%s)>' % (self.__class__.__name__, latex)

    __str__ = to_latex
    __repr__ = to_latex

    @vector_function(1)
    def __call__(self, base_value):
        base_value = PolyExponents.__validate_value__(base_value)
        exponent1, factor = self.items()[0]
        if len(self.items()) == 1:
            return self._decimal_power_(base_value, exponent1) * factor
        for exponent2, addend in self.items()[1:]:
            factor = self._decimal_power_(base_value, exponent1 - exponent2) \
                    * factor + addend
            exponent1 = exponent2
        if exponent2 != Decimal('0'):
            factor = self._decimal_power_(base_value, exponent2) * factor
        return factor

    def __setitem__(self,  exponent, factor):
        exponent = self.__validate_key__(exponent)
        factor = self.__validate_value__(factor)
        if factor == Decimal('0') and exponent != self.__validate_key__(0):
            del self[exponent]
        else:
            SortedKeysDecimalValuedDict.__setitem__(self, exponent, factor)

    def __add__(self, value):
        out = SortedKeysDecimalValuedDict.__add__(self, value)
        for exponent, factor in out.items():
            if not (factor or not exponent):
                del out[exponent]
        if not out.keys():
            out[0] = 0
        return out

    def __mul__(self, value):
        if isinstance(value, self.__class__):
            out = self.__class__({})
            for self_exponent in self.keys():
                for value_exponent in value.keys():
                    new_exponent = self_exponent + value_exponent
                    new_factor = self[self_exponent] * value[value_exponent]
                    if new_exponent in out:
                        out[new_exponent] += new_factor
                    else:
                        out[new_exponent] = new_factor
        else:
            out = SortedKeysDecimalValuedDict.__mul__(self, value)
        for exponent, factor in out.items():
            if not (factor or not exponent):
                del out[exponent]
        if not out.keys():
            out[0] = 0
        return out

    def __div__(self, value):
        out = self.__class__(self)
        value = self.__validate_value__(value)
        if value:
            for key in self.keys():
                out[key] = decimal_division(self[key], value)
        return out

    def __rdiv(self, value):
        out = self.__class__(self)
        value = self.__validate_value__(value)
        if value:
            for key in self.keys() and value:
                out[key] = self[key] / value
        return out

    def __pow__(self, value):

        def local_power(root, exponent):
            if exponent == 1:
                return root
            elif exponent % 2:
                return local_power(root, exponent - 1) * root
            else:
                return local_power(root * root, exponent / 2)

        out = self.__class__(self)
        if isinstance(value, int) and value > 0:
            return local_power(out, value)

    def __rpow__(self, value):
        pass

    def derivative(self):
        out = self.__class__({})
        for exponent, factor in self.__class__(self).items():
            if exponent != Decimal('0'):
                out[exponent - 1] = exponent * factor
        return out

    def integral(self, constant=Decimal('0')):
        out = self.__class__({})
        if constant == Decimal('0'):
            del out[0]
        else:
            out[0] = constant
        for exponent, factor in self.__class__(self).items():
            out[exponent + 1] = factor / (exponent + 1)
        return out

    def inverse(self,
                value,
                minimum=Decimal('0'),  # Or start value
                maximum=None,
                precision=Decimal('1e-20'),
                max_iteration=30
                ):
        value = self.__validate_value__(value)
        if value:
            f = lambda x: self.__call__(x)
            df = lambda x: self.derivative()(x)
            root = Solver(f, df, precision, max_iteration)
            return root(value, minimum, maximum)


class PolyExponents(Polynomial):
    '''PolyExponents are an extension of polynomials.
    Here the exponents doesn't have to be just integers.
    All decimal type values are accepted as exponents.
    So it is fair to say that a PolyExponents is a linear combination of
    roots, negative and positive powers.

    It uses an extended Horners method for evaluation.
    And derivatives can found exact by specifying a degree of differention.

    The price paid for this extension is that PolyExponents can only have
    positive arguments.

    **At instantiation:**

    :param dct_of_exponents_and_factors: Array of x-coordinates
    :type dct_of_exponents_and_factors: A dictionary where the keys
        are exponents and the values are factors.

    **When called as a function**

    :param base_value: Specifying the degree of differention
    :type base_value: A Decimal (Integer, float or Decimal)
    :return: When called as a function returns the functional value.
        If a degree is specified then the degree order derivative is returned

    **How to use:**

    Use PolyExponents in financial calculations. First construct the npv as
    a function of 1 + r

    >>> from decimalpy import Vector, PolyExponents
    >>> cf = Vector(5, 0.1)
    >>> cf[-1] += 1
    >>> cf
    Vector([0.1, 0.1, 0.1, 0.1, 1.1])
    >>> times = Vector(range(0,5)) + 0.783
    >>> times_and_payments = dict(zip(-times, cf))
    >>> npv = PolyExponents(times_and_payments, '(1+r)')
    >>> npv # doctest: +NORMALIZE_WHITESPACE
    <PolyExponents(0.1 (1+r)^-0.783 + 0.1 (1+r)^-1.783 + 0.1 (1+r)^-2.783 + 0.1 (1+r)^-3.783 + 1.1 (1+r)^-4.783)>

    >>> try:
    ...     npv(-1)
    ... except Exception, error_text:
    ...     print error_text
    Only non-negative arguments are allowed
    * variable_index=1
    * args=(<PolyExponents(0.1 (1+r)^-0.783 + 0.1 (1+r)^-1.783 + 0.1 (1+r)^-2.783 + 0.1 (1+r)^-3.783 + 1.1 (1+r)^-4.783)>, -1)
    * kwargs={}
    * argument_is_decimal=False

    Get the npv at rate 10%, ie 1 + r = 1.1:

    >>> OnePlusR = 1.1
    >>> npv(OnePlusR)
    Decimal('1.020897670129900750434884605')

    Now find the internal rate, ie npv = 1 (note that default starting value
    is 0, which isn't a good starting point in this case. A far better
    starting point is 1 which is the second parameter in the call of method
    inverse):

    >>> npv.inverse(1, 1) - 1
    Decimal('0.105777770945873634162979715')

    So the internal rate is approximately 10.78%

    Now let's add some discountfactors, eg reduce with 5% p.a.:

    So the discount factors are:

    >>> discount = Decimal('1.05') ** - times

    And the discounted cashflows are:

    >>> disc_npv = npv * discount
    >>> disc_npv
    <PolyExponents(0.09625178201551631581068644778 x^-0.783 + 0.09166836382430125315303471217 x^-1.783 + 0.08730320364219166966955686873 x^-2.783 + 0.08314590823065873301862558927 x^-3.783 + 0.8710523719402343459094109352 x^-4.783)>

    And the internal rate is:

    >>> disc_npv.inverse(1, 1) - 1
    Decimal('0.053121686615117746821885443')

    And now it is seen that the internal rate is a multiplicative spread:

    >>> disc_npv.inverse(1, 1) * Decimal('1.05') - 1
    Decimal('0.105777770945873634162979715')

    which is the same rate as before.
    '''

    @staticmethod
    def __validate_key__(key):
        if isinstance(key, (int, float, Decimal)):
            return Decimal(str(key))

    @vector_function(1)
    def __call__(self, base_value):
        assert base_value >= 0, 'Only non-negative arguments are allowed'
        return Polynomial.__call__(self, base_value)


if __name__ == '__main__':
    import doctest
    doctest.testmod()