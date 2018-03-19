#############################################################################
# The finance package is open source under the `Python Software Foundation  #
# License <http://www.opensource.org/licenses/PythonSoftFoundation.php>`_   #
#############################################################################

'''
**Module implementing algebraic structures to use for constructing data types**

It turns out that it is smart to mimic mathematical structures and concepts
in scientific/financial programming. This is natural since operator overload
is avaiable in Python already.

Some of the concepts even are usuable across packages, eg. the cummutativeness
of addition and multiplication.

In these classes the necessary and suffient methods has to be defined. The
rest is automated.
'''

from abc import ABCMeta, abstractmethod


class CummutativeAddition:
    '''CummutativeAddition is a meta class for handling cummutative addition.

    **Usage**

    Define a class with the necessary and suffient methods:

    >>> class cummutative_addition(CummutativeAddition):
    ...     def __init__(self, value):
    ...         self.value = str(value)
    ...     def __neg__(self):
    ...         return 'neg(%s)' % self.value
    ...     def __abs__(self):
    ...         return 'abs(%s)' % self.value
    ...     def __add__(self, value):
    ...         return self.value + str(value)
    ...     def __rsub__(self, value):
    ...         return '%s + %s' % (str(value), -self)
    ...

    Let's instanciate the class:

    >>> test = cummutative_addition(5)

    Now cummulative addition is possible. First left addition as defined
    above:

    >>> test + 4
    '54'

    Right addition is the same as left, but is defined through the parent
    class:

    >>> 4+test # = test + 4 since the addition is cummutative
    '54'

    What is understood by the function abs and by the negative value has to
    be defined in each cummutative additive class:

    >>> abs(test)
    'abs(5)'
    >>> -test
    'neg(5)'

    Subtraction is also defined as addition where one or more elements are
    negative:

    >>> test-4
    '5-4'
    >>> 4-test
    '4 + neg(5)'
    >>> test += 1
    >>> test
    '51'

    If not all necessary methods are defined an error is raised. Below is
    such a class:

    >>> class not_all_methods_defined(CummutativeAddition):
    ...     def __init__(self, value):
    ...         self.value = str(value)
    ...     def __add__(self, value):
    ...         return self.value + str(value)
    ...     def __rsub__(self, value):
    ...         pass
    ...

    And the error the class raises:

    The abstractmethod decorated methods must be defined:
    >>> try:
    ...     test = not_all_methods_defined(5)
    ... except Exception, error_text:
    ...     print error_text
    ...
    Can't instantiate abstract class not_all_methods_defined with abstract methods __abs__, __neg__
    '''

    __metaclass__ = ABCMeta

    @abstractmethod
    def __neg__(self):
        raise NotImplementedError

    @abstractmethod
    def __abs__(self):
        raise NotImplementedError

    @abstractmethod
    def __add__(self, other_value):
        raise NotImplementedError

    @abstractmethod
    def __rsub__(self, other_value):
        '''__rsub__ has to be defined to handle right side subtraction since
        subtraction otherwise is specified at the left value.
        '''
        raise NotImplementedError

    def __radd__(self, other_value):
        return  self.__add__(other_value)

    def __sub__(self, other_value):
        return self.__add__(-other_value)

    def __iadd__(self, other_value):
        return  self.__add__(other_value)

    def __isub__(self, other_value):
        return self.__add__(-other_value)


class CummutativeMultiplication:
    '''Multiplication is a meta class for handling cummutative multiplication.

    **Usage**

    This is basically the same as cummutative addition.
    Let's look at a class:

    >>> class cummutative_multiplication(CummutativeMultiplication):
    ...     def __init__(self, value):
    ...         self.value = str(value)
    ...     def __mul__(self, value):
    ...         return '%s * %s' % (self.value, value)
    ...     def __div__(self, value):
    ...         return '%s / %s' % (self.value, value)
    ...     def __rdiv__(self, value):
    ...         return '%s / %s' % (value, self.value)
    ...

    Instantiation of that class:

    >>> test = cummutative_multiplication(5)

    Left multiplication as defined in the class:

    >>> test * 4
    '5 * 4'

    Right multiplication as inherited:

    >>> 4*test # = test * 4 since the multiplication is cummutative
    '5 * 4'

    Both left and right division has to be defined in the class:

    >>> test / 4
    '5 / 4'
    >>> 4/test # != test / 4 since the division is not cummutative
    '4 / 5'
    '''

    __metaclass__ = ABCMeta

    @abstractmethod
    def __mul__(self, other_value):
        raise NotImplementedError

    @abstractmethod
    def __div__(self, other_value):
        raise NotImplementedError

    @abstractmethod
    def __rdiv__(self, other_value):
        raise NotImplementedError

    def __rmul__(self, other_value):
        return self.__mul__(other_value)


class Power:
    '''Power is a meta class for handling the power of an object.

    **Usage**

    This is basically the same as cummutative additiion.
    Let's look at a class:

    >>> class power(Power):
    ...     def __init__(self, value):
    ...         self.value = str(value)
    ...     def __pow__(self, value):
    ...         return '%s ** %s' % (self.value, value)
    ...     def __rpow__(self, value):
    ...         return '%s ** %s' % (value, self.value)
    ...

    Instantiation of that class:

    >>> test = power(5)

    Left and right power has been defined in the class:

    >>> test ** 4
    '5 ** 4'
    >>> 4**test
    '4 ** 5'

    Self power is inherited:

    >>> test **= 3
    >>> print test
    5 ** 3
    '''

    __metaclass__ = ABCMeta

    @abstractmethod
    def __pow__(self, other_value):
        raise NotImplementedError

    @abstractmethod
    def __rpow__(self, other_value):
        raise NotImplementedError

    def __ipow__(self, other_value):
        return self.__pow__(other_value)


if __name__ == '__main__':
    import doctest
    doctest.testmod()