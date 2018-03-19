#############################################################################
# The finance package is open source under the `Python Software Foundation  #
# License <http://www.opensource.org/licenses/PythonSoftFoundation.php>`_   #
#############################################################################

'''A timeflow is a transformation of the dateflow where dates is converted to
times in order to do fixed income mathematics.
'''

from abc import ABCMeta, abstractmethod
from calendar import isleap
from bankdate import BankDate
from dateflow import DateFlow
from decimalpy import Vector, vector_function, to_decimal, Solver


class DateToTimeError(Exception):
    '''A class to implement error messages from class DateToTime.'''
    pass


class DateToTime(object):
    ''' A class to implement different daycount methods and the related time
    convertions.

    **References:**
        * http://www.eclipsesoftware.biz/DayCountConventions.html
        * http://en.wikipedia.org/wiki/Day_count_convention

    :param daycount_method: Name of day count method. Default is act/365
    :type daycount_method: ('act/365', 'act/360', '360/360', 'act/actISDA')
    :param valuation_date: A BankDate which is the base for time convertions
          Default is current date as a BankDate.
    :return: A date converted to a time (of type Decimal) in years

    **When called as a function:**

    :param date: A BankDate
    :return: the date, the following date according to settings and the time in
        years as a float according to settings

    **How to use!**

    >>> dtt = DateToTime(valuation_date = '2009-11-08')
    >>> print dtt # To see (default) settings
    Time Convertion:
    Daycount method = act/365
    Valuation date  = 2009-11-08

    >>> bd = BankDate('2009-11-08')
    >>> dtt(bd + "365d")
    Decimal('1')

    >>> dtt360 = DateToTime('360/360', bd)
    >>> print dtt360
    Time Convertion:
    Daycount method = 360/360
    Valuation date  = 2009-11-08

    >>> dtt360(bd + "12m")
    Decimal('1')

    >>> dtt360(bd + "15m")
    Decimal('1.25')

    >>> dtt360 = DateToTime('360/360', bd)
    >>> print dtt360
    Time Convertion:
    Daycount method = 360/360
    Valuation date  = 2009-11-08

    >>> d = bd + "7d"
    >>> dtt360(d.adjust_to_bankingday('Following'))
    Decimal('0.02222222222222222222222222222')

    >>> dtt360([bd + "12m", bd + '15m'])
    Vector([1, 1.25])
    '''
    def __init__(self,
                 daycount_method='act/365',
                 valuation_date=BankDate()):
        self.set_daycount_method(daycount_method)
        self.set_valuation_date(valuation_date)

    def _act_act_isda_fraction(self, date):
        '''Implement daycount method Act/Act ISDA
        '''
        date = BankDate(date)
        if date and date > self._valuation_date:
            date_year = date.year
            days_in_year = to_decimal(366 if isleap(date.year) else 365)
            days_in_valuation_year = to_decimal(366
                            if isleap(self._valuation_date.year)
                            else 365)
            if self._valuation_date.year == date.year:
                return self._valuation_date.nbr_of_days(date) \
                        / days_in_valuation_year
            else:
                mid_day = BankDate('%s-01-01' % date_year)
                return self._valuation_date.nbr_of_days(mid_day) \
                / days_in_valuation_year \
                + mid_day.nbr_of_days(date) / days_in_year
        else:
            return to_decimal(0)

    def _act_365_fraction(self, date):
        '''Implement daycount method Act/365
        '''
        date = BankDate(date)
        if date and date > self._valuation_date:
            return self._valuation_date.nbr_of_days(date) / to_decimal(365)
        else:
            return to_decimal(0)

    def _act_360_fraction(self, date):
        '''Implement daycount method Act/360
        '''
        date = BankDate(date)
        if date and date > self._valuation_date:
            return self._valuation_date.nbr_of_days(date) / to_decimal(360)
        else:
            return to_decimal(0)

    def _360_360_fraction(self, date):
        '''Implement daycount method 360/360
        '''
        day1 = BankDate(date)
        day2 = self._valuation_date
        if day1 and day1 > day2:
            number_of_days = 360 * (day1.year - day2.year) \
                + 30 * (day1.month - day2.month) \
                + (day1.day - day2.day)
            number_of_days = number_of_days % 360
            return to_decimal(number_of_days) / to_decimal(360)
        else:
            return to_decimal(0)

    def __str__(self):
        '''Nice printout of settings for Time Convertion
        '''
        return 'Time Convertion:\nDaycount method = %-s\n' \
                'Valuation date  = %-s' \
        % (self._daycount_methodname, self._valuation_date)

    __repr__ = __str__

    @vector_function(1)
    def __call__(self, date):
        '''Returns the adjusted input date converted to time according to time
        convertion settings.
        Input is date as BankDate
        '''
        bdate = BankDate(date)
        nbr_years = self._valuation_date.nbr_of_years(bdate)
        newdate = bdate.add_years(-nbr_years)
        return nbr_years + self._daycount_method(newdate)

    def set_daycount_method(self, daycount_method):
        '''Reset or set Daycount method

        :param daycount_method: Name of day count method. Default is act/365
        :type daycount_method: 'act/365', 'act/360', '360/360', 'act/actISDA'
        '''
        daycount_method_dict = {
            'act/365':        self._act_365_fraction,
            'act/360':        self._act_360_fraction,
            '360/360':        self._360_360_fraction,
            'act/actISDA':    self._act_act_isda_fraction
            }
        if daycount_method in daycount_method_dict.keys():
            self._daycount_methodname = daycount_method
            self._daycount_method = daycount_method_dict[daycount_method]
        else:
            raise DateToTimeError(
            'The daycount method must be one of %s, not %s of type %s'
            % (daycount_method_dict.keys(),
                daycount_method,
                type(daycount_method))
                )

    def set_valuation_date(self, valuation_date):
        '''Reset or set valuation day
        '''
        self._valuation_date = BankDate(valuation_date)

    def get_valuation_date(self):
        '''Get valuation day
        '''
        return self._valuation_date

    valuation_date = property(get_valuation_date, set_valuation_date)


class ClassicRiskMeasures:

    __metaclass__ = ABCMeta

    basispoint = to_decimal('0.0001')

    @abstractmethod
    def npv_value(self, spread):
        '''npv_value has to be defined before using ClassicRiskMeasures
        '''
        raise NotImplementedError

    @abstractmethod
    def npv_d1(self, spread):
        '''npv_d1 has to be defined before using ClassicRiskMeasures
        '''
        raise NotImplementedError

    @abstractmethod
    def npv_d2(self, spread):
        '''npv_d2 has to be defined before using ClassicRiskMeasures
        '''
        raise NotImplementedError

    @vector_function(1, True)
    def modified_duration(self, spread):
        '''
        :param spread: A rate based generel spread.
        :type spread: A float between 0 and 1
        :return: modified_duration for the DateFlow and time valuation
                    parameters given at instantiation

        *Formula for modified_duration:*

        .. math::
             modified \\textunderscore duration &= \\frac {1}
             {NPV \\left( spread \\right)} \\cdot
             \\frac {\\partial NPV \\left( spread \\right)}{\\partial spread}\\\\
                  &= \\frac{1}{NPV \\left( spread \\right)} \\cdot
                  npv \\textunderscore d1

        .. note::
            Actually when no discountcurve is used the spread can be used to
            implement the discountcurve with constant discountfactor for each
            future period of fixed length.
        '''
        if self.__nonzero__():
            npv = self.npv_value(spread)
            if spread and npv:
                return - self.npv_d1(spread) / npv

    @vector_function(1, True)
    def macauley_duration(self, spread):
        '''
        :param spread: A rate based generel spread. Default is 0.0 ie no spread
        :type spread: A float between 0 and 1
        :return: macauley_duration for the DateFlow and time valuation
                    parameters given at instantiation

        *Formula for macauley_duration:*

        .. math::
             macauley \\textunderscore duration &= \\frac{1}
             {NPV \\left( spread \\right) \\cdot \\left( 1 + spread \\right)}
             \\cdot \\frac {\\partial NPV \\left( spread \\right)}
             {\\partial spread}\\\\
                  &= \\frac {1}{NPV \\left( spread \\right) \\cdot
                  \\left( 1 + spread \\right)} \\cdot npv \\textunderscore d1

        .. note::
            Actually when no discountcurve is used the spread can be used to
            implement the discountcurve with constant discountfactor for each
            future period of fixed length.

        '''
        if self.__nonzero__():
            npv = self.npv_value(spread)
            if spread and npv:
                return - self.npv_d1(spread) / npv * (1 + spread)

    @vector_function(1, True)
    def modified_convexity(self, spread):
        '''
        :param spread: A rate based generel spread. Default is 0.0 ie no spread
        :type spread: A float between 0 and 1
        :return: modified_convexity for the DateFlow and time valuation
            parameters given at instantiation

        *Formula for macauley_convexity:*

        .. math::
             macauley \\textunderscore convexity &= \\frac {1}
             {NPV \\left( spread \\right)} \\cdot \\frac
             {\\partial ^{2} NPV \\left( spread \\right)}
             {\\partial spread ^{2}}\\\\
                  &= \\frac {1}{NPV \\left( spread \\right)}\\cdot npv\\_d2

        .. note::
            Actually when no discountcurve is used the spread can be used to
            implement the discountcurve with constant discountfactor for each
            future period of fixed length.
        '''
        if self.__nonzero__():
            spread = to_decimal(spread)
            npv = self.npv_value(spread)
            if spread and npv:
                return self.npv_d2(spread) / npv

    @vector_function(1, True)
    def macauley_convexity(self, spread):
        '''
        :param spread: A rate based generel spread.
        :type spread: A float between 0 and 1
        :return: macauley_convexity for the DateFlow and time valuation
            parameters given at instantiation

        *Formula for macauley_convexity:*

        .. math::
             macauley \\textunderscore convexity &= \\frac {1}
             {NPV \\left( spread \\right) \\cdot \\left( 1 + spread \\right)^{2}}
             \\cdot \\frac {\\partial ^{2} NPV \\left( spread \\right)}
             {\\partial spread ^{2}}\\\\
                &= \\frac {1}{NPV \\left( spread \\right) \\cdot
                \\left( 1 + spread \\right) ^{2}} \\cdot npv \\textunderscore d2

        .. note::
            Actually when no discountcurve is used the spread can be used to
            implement the discountcurve with constant discountfactor for each
            future period of fixed length.
        '''
        if self.__nonzero__():
            npv = self.npv_value(spread)
            if spread and npv:
                return self.npv_d2(spread) / npv * (1 + spread) ** 2

    @vector_function(1, True)
    def pv01(self, spread):
        '''
        :param spread: A rate based generel spread.
        :type spread: A float between 0 and 1
        :return: pv01 for the DateFlow and time valuation parameters given at
            instantiation

        *Formula for pv01:*

        .. math::
             pv01 &= \\frac {\\partial NPV \\left( spread \\right)}
             {\\partial spread}\\cdot0.0001\\\\
                &= npv \\textunderscore d1 \\left( spread \\right) \\cdot 0.0001

        This definition has the advantage that it can handle DateFlows with NPV
        near zero.

        .. note::
            Actually when no discountcurve is used the spread can be used to
            implement the discountcurve with constant discountfactor for each
            future period of fixed length.
        '''
        if self.__nonzero__():
            if spread:
                return - ClassicRiskMeasures.basispoint * self.npv_d1(spread)

    @vector_function(1, True)
    def pvbp(self, spread):
        '''
        :param spread: A rate based generel spread.
        :type spread: A float between 0 and 1
        :return: pvbp for the DateFlow and time valuation parameters given at
            instantiation

        *Formula for pvbp:*

        .. math::
             pvbp = NPV \\left( spread \\right)
             - NPV \\left( spread + 0.0001 \\right)

        This definition has the advantage that it can handle DateFlows with NPV
        near zero.

        .. note::
            Actually when no discountcurve is used the spread can be used to
            implement the discountcurve with constant discountfactor for each
            future period of fixed length.
        '''
        if self.__nonzero__():
            if spread:
                return self.npv_value(spread) \
                    - self.npv_value(spread + ClassicRiskMeasures.basispoint)


class TimeFlow(ClassicRiskMeasures):
    '''Timeflow combines the logic of DateToTime and yieldcurves to transform
    a dateflow though discounting into something that have eg a present
    value, derivatives and a spread.
    DateToTime transform dates to time and yieldcurves weigths the payments.


    **Usage**

    A DateToTime is needed to define the conversion from date to time.

    >>> from finance.timeflow import DateToTime
    >>> dtt = DateToTime(valuation_date = '2009-11-22')

    Instantiate with DateToTime object alone:

    >>> from finance import TimeFlow
    >>> tf = TimeFlow(dtt)
    >>> tf
    <instance TimeFlow>
    Time Convertion:
    Daycount method = act/365
    Valuation date  = 2009-11-22

    Specify a DateFlow to use:

    >>> from finance import DateFlow
    >>> df = DateFlow({BankDate('2010-11-12') : 453})

    The DateFlow can be added like:

    >>> tf.dateflow = df
    >>> tf
    <instance TimeFlow>
    Time Convertion:
    Daycount method = act/365
    Valuation date  = 2009-11-22

    Or the DateFlow can be added at instatiation like:

    >>> tf = TimeFlow(dtt, dateflow=df)
    >>> print tf
    <instance TimeFlow>
    Time Convertion:
    Daycount method = act/365
    Valuation date  = 2009-11-22
    Date        Time      Value
    2009-11-22, 0.0000,   0.00
    2010-11-12, 0.9726, 453.00

    Let's have amore interesting example. Let's look at a bullit cashflow
    defined to start at 2009-11-24, having 5 rate payments of 10% and with a
    repayment of the nominal at the last rate payment.

    First use the dateflow_generator to generate the bullit cashflow:

    >>> from finance import dateflow_generator
    >>> df = dateflow_generator(0.1, 5, '2009-11-24', cashflowtype='bullit')

    Then add it to the TimeFlow tf:

    >>> tf.dateflow = df

    Let's see the cashflow as a timeflow:

    >>> print tf
    <instance TimeFlow>
    Time Convertion:
    Daycount method = act/365
    Valuation date  = 2009-11-22
    Date        Time      Value
    2009-11-22, 0.0000,     0.00
    2009-11-24, 0.0055,     0.00
    2010-11-24, 1.0055,    10.00
    2011-11-24, 2.0055,    10.00
    2012-11-24, 3.0055,    10.00
    2013-11-24, 4.0055,    10.00
    2014-11-24, 5.0055,   110.00

    And now do some interest rate calculations:

    >>> tf.npv_value(0)  # The sum of the cashflow
    Decimal('150.0000000000000000000000000')

    >>> tf.npv_value(0.1)  # The sum of the cashflow with discount rate 10%
    Decimal('99.94778887869488654978784607')

    >>> tf.npv_spread(100)  # The Par rate
    Decimal('0.09986242567998284995258866564')

    Now set valuation date equal to the start of the cashflow:

    >>> tf.valuation_date = '2009-11-24'
    >>> print tf
    <instance TimeFlow>
    Time Convertion:
    Daycount method = act/365
    Valuation date  = 2009-11-24
    Date        Time      Value
    2009-11-24, 0.0000,     0.00
    2010-11-24, 1.0000,    10.00
    2011-11-24, 2.0000,    10.00
    2012-11-24, 3.0000,    10.00
    2013-11-24, 4.0000,    10.00
    2014-11-24, 5.0000,   110.00

    Now the present value is 100:

    >>> tf.npv_value(0.1)  # The sum of the cashflow with discount rate 10%
    Decimal('100.0000000000000000000000000')

    And the spread becomes 10%:

    >>> tf.npv_spread(100)  # The Par rate should now be 10% or 0.1
    Decimal('0.1000000000000000000000000002')

    and the first and second derivative when the spread is 10%, respectively:

    >>> tf.npv_d1(0.1)
    Decimal('-379.0786769408448255521542866')
    >>> tf.npv_d2(0.1)
    Decimal('1936.834238279122197880851971')

    There are the following standard interest rate risk calculation:

    >>> tf.modified_duration(0.1)
    Decimal('3.790786769408448255521542866')
    >>> tf.macauley_duration(0.1)
    Decimal('4.169865446349293081073697153')
    >>> tf.modified_convexity(0.1)
    Decimal('19.36834238279122197880851971')
    >>> tf.macauley_convexity(0.1)
    Decimal('23.43569428317737859435830885')

    Value of a basis point, PVBP and PV01, refers to the average amount by
    which the MarkToMarket value of any instrument changes when the entire
    yield curve is shifted up and down by 0.01% (a basispoint).
    It is an absolute measure of pure price change.

    pv01 and pvbp are methods in the object TimeFlow.

    Below pv01 and pvbp are calculated at flat yieldcurve at 10% (0.1).

    >>> tf.pv01(0.1)
    Decimal('0.03790786769408448255521542866')
    >>> tf.pvbp(0.1)
    Decimal('0.03789818550933853843871350')

    They are eg described in [Sadr]_

    It is possible to do decimal vector calculations here, eg:

    >>> from decimalpy import round_decimal
    >>> rates = [0.05, 0.075, 0.1, 0.125, 0.15]
    >>> [str(round_decimal(npv, 2)) for npv in tf.npv_value(rates)]
    ['121.65', '110.11', '100.00', '91.10', '83.24']

    or:

    >>> [str(round_decimal(spread, 4)) for spread in tf.npv_spread([90, 100, 110])]
    ['0.1283', '0.1000', '0.0753']

    or:

    >>> [str(round_decimal(npv, 4)) for npv in tf.modified_duration(rates)]
    ['4.0510', '3.9183', '3.7908', '3.6683', '3.5504']

    So scenarios and grafs becomes quite easy.
    '''
    def __init__(self, date_to_time, discount=None, dateflow=None):
        '''
        :param used_discountcurve: Used  discountcurve. Default is None
            ie. no discounting
        :type used_discountcurve: A discountcurve or None

        '''
        self._set_date_to_time(date_to_time)
        self._set_discount(discount)
        self._set_dateflow(dateflow)

    def __nonzero__(self):
        return 1 if self._date_to_time else 0

    def __str__(self):
        max_value = max(len(str(value)) for value in self.discounted_values())
        data = zip(self.future_dateflow().keys(),
                   self.future_times(),
                   self.discounted_values()
                   )
        header = '\n%-10s  %-8s  %-s\n' % ('Date', 'Time', 'Value')
        layout = '%-10s, %3.4f, %' + str(max_value + 3) + '.2f'
        cashflow = header + '\n'.join([layout % row for row in data])
        return self.__repr__() + cashflow

    def __repr__(self):
        return '<instance %s>\n%s' % (self.__class__.__name__,
                           self._date_to_time.__repr__())

    def _get_date_to_time(self):
        return self._date_to_time

    def _set_date_to_time(self, date_to_time):
        if isinstance(date_to_time, DateToTime):
            self._date_to_time = date_to_time
        else:
            self._date_to_time = None

    def date_to_time_from_parameters(self, daycount_method, valuation_date):
        date_to_time = DateToTime(daycount_method, valuation_date)
        if date_to_time:
            self._date_to_time = date_to_time
        else:
            self._date_to_time = None

    date_to_time = property(_get_date_to_time, _set_date_to_time)

    def _get_discount(self):
        return self._discount

    def _set_discount(self, discount):
        if discount:
            self._discount = discount
        else:
            self._discount = None

    discount = property(_get_discount, _set_discount)

    def _get_dateflow(self):
        return self._dateflow

    def _set_dateflow(self, dateflow):
        if dateflow and isinstance(dateflow, DateFlow):
            self._dateflow = dateflow
        else:
            self._dateflow = DateFlow({})

    dateflow = property(_get_dateflow, _set_dateflow)

    def _get_valuation_date(self):
        return self._date_to_time.valuation_date

    def _set_valuation_date(self, date):
        self._date_to_time.valuation_date = date

    valuation_date = property(_get_valuation_date, _set_valuation_date)

    def future_dateflow(self):
        future_dateflow = self.dateflow[self.valuation_date:]
        future_dateflow[self.valuation_date] = 0
        return future_dateflow

    def future_times(self):
        return Vector(self.date_to_time(self.future_dateflow().keys()))

    def discounted_values(self):
        if self.discount:
            return self.discount(self.future_times()) \
                    * self.future_dateflow().values()
        else:
            return self.future_dateflow().values()

    @vector_function(1, True)
    def npv_value(self, spread):
        '''
        :param spread: A rate based generel spread.
        :type spread: A float between 0 and 1
        :param used_discountcurve: Used  discountcurve. Default is None
            ie. no discounting
        :type used_discountcurve: A discountcurve or None
        :return: npv_value for the DateFlow and time valuation parameters given
            at instantiation

        *Short hand notation for npv_value in the documentation:*

        .. math::
             NPV ( spread ) = npv \\textunderscore value ( spread )

        .. note::
            Actually when no discountcurve is used the spread can be used to
            implement the discountcurve with constant discountfactor for each
            future period of fixed length.
        '''
        # discounted_values is called as a function to get vector
        # multiplication
        spread = to_decimal(spread)
        return self.discounted_values()((1 + spread) ** -self.future_times())

    @vector_function(1, True)
    def npv_d1(self, spread):
        '''
        :param spread: A rate based generel spread.
        :type spread: A float between 0 and 1
        :return: First order derivative for the DateFlow and time valuation
            parameters given at instantiation

        *Formula for npv_d1:*

        .. math::
             npv \\textunderscore d1 =
             \\frac {\\partial NPV \\left( spread \\right)}
             {\\partial spread}
        '''
        # discounted_values is called as a function to get vector
        # multiplication
        spread = to_decimal(spread)
        return self.discounted_values()(-self.future_times()
                    * (1 + spread) ** (-self.future_times() - 1)
                    )

    @vector_function(1, True)
    def npv_d2(self, spread):
        '''
        :param spread: A rate based generel spread.
        :type spread: A float between 0 and 1
        :return: Second order derivative for the DateFlow and time valuation
            parameters given at instantiation

        *Formula for npv_d2:*

        .. math::
             npv \\textunderscore d2 = \\frac{\\partial ^{2} NPV
             \\left( spread \\right)}{\\partial spread ^{2}}
        '''
        spread = to_decimal(spread)
        discounts = -self.future_times() * (-self.future_times() - 1) \
                        * (1 + spread) ** (-self.future_times() - 2)
        # discounted_values is called as a function to get vector
        # multiplication
        return self.discounted_values()(discounts)

    @vector_function(1, True)
    def npv_spread(self, npv_0, precision=1e-16, max_iteration=30):
        '''
        :param npv_0: The present value of the cashflow
        :type  npv_0: Float or decimal
        :param max_iteration: The precision/tolerance for the result.
            Default is 1e-16
        :type max_iteration: Float or decimal
        :param max_iter: The maximal number of iterations. Default is 30
        :type max_iter: A positive integer
        :return: The par rate of the discounted cashflow
        '''
        npv_0 = to_decimal(npv_0)
        if npv_0:  # TODO: Valuate for a solution
            spread_func = Solver(self.npv_value,
                                        self.npv_d1,
                                        precision,
                                        max_iteration
                                        )
            return spread_func(npv_0)


if __name__ == '__main__':
    import doctest
    doctest.testmod()