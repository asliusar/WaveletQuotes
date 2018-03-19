#############################################################################
# The finance package is open source under the `Python Software Foundation  #
# License <http://www.opensource.org/licenses/PythonSoftFoundation.php>`_   #
#############################################################################

# http://effbot.org/pylib/decimal.htm#quick-start-tutorial

import decimal
from decimal import Decimal as _Decimal, getcontext as _getcontext


class Nbr(_Decimal):
    '''The decimal representation in decimalpy. The Decimal is ok in most
    senses.

    But from this projects view it would be better if other number types
    like integer and float could be at one side of a mathematical operator
    and Nbr at the other side would lead to Nbr using the string
    representation of the integer or float

    >>> 4.7, 4.7 - Nbr(1) + 4.7
    (4.7, Nbr('8.4'))

    >>> - Nbr(1), abs(Nbr(-2))
    (Nbr('-1'), Nbr('2'))

    **Usage**

    >>> Nbr(4.7), Nbr('4.7'),  Nbr('4.7').round(3)
    (Nbr('4.7'), Nbr('4.7'), Nbr('4.700'))

    Division. If denominator is zero, Nbr('NaN') is
    returned

    >>> Nbr('5') / Nbr('3')
    Nbr('1.666666666666666666666666667')
    >>> Nbr('5') / Nbr('0')
    Nbr('Infinity')
    >>> Nbr(5) / 0
    Nbr('Infinity')
    >>> 5 / Nbr(0)
    Nbr('Infinity')
    >>> from decimal import Decimal
    >>> Decimal('5') / Nbr(0)
    Nbr('Infinity')

    Calculate :math:`2^3`:
    >>> Nbr('2') ** 3
    Nbr('8')

    Calculate :math:`2^3 + 3`:
    >>> Nbr('2') ** 3 + 3
    Nbr('11')

    Calculate :math:`4 \cdot 2^3 - 3`:
    >>> 4 * Nbr('2') ** 3 - 3
    Nbr('29')

    >>> Nbr.exp(Nbr('1'))
    Nbr('2.718281828459045235360287471')

    >>> Nbr('5') ** 0
    Nbr('1')

    >>> Nbr('0') ** 2.4
    Nbr('0')

    >>> Nbr(None), Nbr('test')
    (Nbr('NaN'), Nbr('NaN'))
    '''

    def __new__(self, value=0):
        try:
            return super(Nbr, self).__new__(self, str(value))
        except:
            return super(Nbr, self).__new__(self, 'NaN')

    def __repr__(self):
        return "Nbr('%s')" % _Decimal.__str__(self)

    # Overwrite the original __repr__ and hence also __str__ etc
    _Decimal.__repr__ = __repr__

    def __add__(self, other, context=None):
        """Returns self + other.

        -INF + INF (or the reverse) cause InvalidOperation errors.
        """
        other = _convert_other(other)
        if other is NotImplemented:
            return other

        if context is None:
            context = _getcontext()

        if self._is_special or other._is_special:
            ans = self._check_nans(other, context)
            if ans:
                return ans

            if self._isinfinity():
                # If both INF, same sign => same as both, opposite => error.
                if self._sign != other._sign and other._isinfinity():
                    return context._raise_error(InvalidOperation, '-INF + INF')
                return _Decimal(self)
            if other._isinfinity():
                return _Decimal(other)  # Can't both be infinity here

        exp = min(self._exp, other._exp)
        negativezero = 0
        if context.rounding == 'ROUND_FLOOR' and self._sign != other._sign:
            # If the answer is 0, the sign should be negative, in this case.
            negativezero = 1

        if not self and not other:
            sign = min(self._sign, other._sign)
            if negativezero:
                sign = 1
            ans = _dec_from_triple(sign, '0', exp)
            ans = ans._fix(context)
            return ans
        if not self:
            exp = max(exp, other._exp - context.prec-1)
            ans = other._rescale(exp, context.rounding)
            ans = ans._fix(context)
            return ans
        if not other:
            exp = max(exp, self._exp - context.prec-1)
            ans = self._rescale(exp, context.rounding)
            ans = ans._fix(context)
            return ans

        op1 = decimal._WorkRep(self)
        op2 = decimal._WorkRep(other)
        op1, op2 = decimal._normalize(op1, op2, context.prec)

        result = decimal._WorkRep()
        if op1.sign != op2.sign:
            # Equal and opposite
            if op1.int == op2.int:
                ans = decimal._dec_from_triple(negativezero, '0', exp)
                ans = ans._fix(context)
                return ans
            if op1.int < op2.int:
                op1, op2 = op2, op1
                # OK, now abs(op1) > abs(op2)
            if op1.sign == 1:
                result.sign = 1
                op1.sign, op2.sign = op2.sign, op1.sign
            else:
                result.sign = 0
                # So we know the sign, and op1 > 0.
        elif op1.sign == 1:
            result.sign = 1
            op1.sign, op2.sign = (0, 0)
        else:
            result.sign = 0
        # Now, op1 > abs(op2) > 0

        if op2.sign == 0:
            result.int = op1.int + op2.int
        else:
            result.int = op1.int - op2.int

        result.exp = op1.exp
        ans = _Decimal(result)
        ans = ans._fix(context)
        return Nbr(ans)

    _Decimal.__add__ = __add__

    def round(self,
              nbr_of_decimals=7,
              rounding_method='ROUND_HALF_UP'
              ):
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
            if not self._isnan():
                rounding = _getcontext().rounding
                if _getcontext().prec <= nbr_of_decimals:
                    precision = _getcontext().prec
                    _getcontext().prec = nbr_of_decimals + 2
                else:
                    precision = None
                _getcontext().rounding = rounding_method
                value = Nbr(self.quantize(Nbr('.1') ** nbr_of_decimals))
                _getcontext().rounding = rounding
                if precision != None:
                    _getcontext().prec = precision
                return value

    def as_currency(self, currency='', places=2):
        '''Function to format a decimal value according to locale settings and the
        values of currency and places.

        :param currency: suffix to be added output representing the unit of value
        :type currency: alphabetic string of length max 3
        :param places: Decimal of decimals to be shown
        :type places: a positive integer
        :return: A string showing the formatted decimal value according to locale
                 settings and the values of currency and places

        **How to use:**

        >>> Nbr(1234567.4499999).as_currency()
        '1.234.567,45'
        >>> Nbr(1234567.4499999).as_currency('DKK')
        '1.234.567,45 DKK'

        source: `Python Format Specification Mini-Language
        <http://docs.python.org/dev/library/string.html#formatspec>`_
        '''
        import locale
        locale.setlocale(locale.LC_ALL, "")
        assert (isinstance(currency, str)
                  and len(currency) < 4
                  and currency.isalpha()) if currency else True, \
                  'currency must be an alphabetic string of length max 3'
        assert isinstance(places, int) and places > 0, \
                  'places must be an positive integer'
        return '{:n} {}'.format(self.round(places), currency) if currency \
                else '{:n}'.format(self.round(places))


def _convert_other(other, raiseit=False, allow_float=True):
    """Convert other to Decimal.

    This function is modified such that all operations with a float is
    acceptable using the string value of the float as argument for Decimal.
    """
    if isinstance(other, Nbr):
        return other
    if isinstance(other, (int, long, _Decimal)):
        return Nbr(other)
    if allow_float and isinstance(other, float):
        return Nbr(str(other))

    if raiseit:
        raise TypeError("Unable to convert %s to Decimal" % other)
    return NotImplemented

# Overwrite decimals _convert_other with the above
decimal._convert_other = _convert_other


# Accept division by zero, ie get infinity values
_getcontext().traps[decimal.DivisionByZero] = 0


def precision_decorator(actual_function):
    '''Increases current precision with 2 decimals.
    Resets current precision after function call
    '''
    def actual_call(*arg):
        _getcontext().prec += 2
        value = actual_function(*arg)
        _getcontext().prec -= 2
        return +value

    actual_call.__name__ = actual_function.__name__
    actual_call.__doc__ = actual_function.__doc__
    actual_call.__module__ = actual_function.__module__
    return actual_call

if __name__ == '__main__':
    import doctest
    doctest.testmod()