#############################################################################
# The finance package is open source under the `Python Software Foundation  #
# License <http://www.opensource.org/licenses/PythonSoftFoundation.php>`_   #
#############################################################################

'''A dateflow is vectorlike structure indexed by bankdates. Is used to
 handling agreements.

'''
# -*- coding: utf-8 -*-

from bankdate import BankDate, daterange_iter, period_count
from decimalpy.math_types import SortedKeysDecimalValuedDict


class DateFlowError(Exception):
    '''A class to implement error messages from class DateFlow.'''
    pass


class DateFlow(SortedKeysDecimalValuedDict):
    '''A DateFlow is a subclass SortedKeysDecimalValuedDict, where the keys
    are an list of bankdates and the values are of type decimal.
    Operator overload is used to simplify operations on DateFlows.

    *Operator overload principles*

        * DateFlows can be added or subtracted to each other
        * DateFlows can also be added, subtracted, multiplied or divided with
            a number (float or int)
        * DateFlows can be ordered according to their date span

    **How to use!**

    The class DateFlow can be instantiated by a yyyy-mm-dd string,
    a Python date or a bankdate and possible a float or integer value.
    Default value is 0

    >>> from datetime import date
    >>> t1, t2, t3 = '2009-09-27', date(2009,12,27), BankDate('2009-09-27')
    >>> c1, c2 = DateFlow({t1 : 100}), DateFlow({t2 : 200})
    >>> c3 = DateFlow({t3 : 300})
    >>> print c1
    Data for the DateFlow:
    * key: 2009-09-27, value: 100
    >>> print c2
    Data for the DateFlow:
    * key: 2009-12-27, value: 200
    >>> print c3
    Data for the DateFlow:
    * key: 2009-09-27, value: 300

    2 or more DateFlows can be added.
    A DateFlow can also be added and multiplied with a number.

    >>> print c1 + 2 * c2 + 1000
    Data for the DateFlow:
    * key: 2009-09-27, value: 1100
    * key: 2009-12-27, value: 1400

    When added DateFlows have dates in common the values are added on these
    dates.

    >>> cf = c1 + 2 * c2 +  c3 * 3  + 1000
    >>> print cf
    Data for the DateFlow:
    * key: 2009-09-27, value: 2000
    * key: 2009-12-27, value: 1400

    It is possible to get the accumulated cashflow.

    >>> cf.accumulated_dateflow()
    Data for the DateFlow:
    * key: 2009-09-27, value: 2000
    * key: 2009-12-27, value: 3400

    A DateFlow is a subclass of a dictionary and it can used accordingly.

    >>> print cf['2009-12-27']
    1400
    >>> sorted(cf.keys())
    [2009-09-27, 2009-12-27]

    The method find_nearest_bankdate find the nearest bankdate equal to or
    below the input. Before if the second parameter before is True (default)
    otherwise the nearest date after).

    >>> cf.find_nearest_bankdate('2009-08-06')

    >>> cf.find_nearest_bankdate('2009-11-06')
    2009-09-27
    >>> cf.find_nearest_bankdate('2009-09-27')
    2009-09-27
    >>> cf.find_nearest_bankdate('2010-11-06')
    2009-12-27

    last_key returns the biggest bankdate in the cashflow

    >>> end_date = (c1 + 2 * c2 +  c3 * 3  + 1000).last_key()
    >>> print end_date
    2009-12-27
    >>> print end_date - BankDate('2009-09-27')
    91

    A zero element for a DateFlow is similar to an empty dictionary.

    >>> DateFlow({})
    Data for the DateFlow:
    *

    A dictionary (of proper format) or a DateFlow can be used as initiation.

    >>> y = DateFlow({'2009-09-11':100})
    >>> DateFlow(y)
    Data for the DateFlow:
    * key: 2009-09-11, value: 100

    DateFlows can be sliced by dates as well.
    Key must be a bankdate or a slice object.

    *Example*

    Look at an annuity starting 2010-04-26 running with 10 payments.

    >>> x=dateflow_generator(0.1, 10, '2010-04-26')
    >>> x
    Data for the DateFlow:
    * key: 2010-04-26, value: 0.0
    * key: 2011-04-26, value: 16.2745394883
    * key: 2012-04-26, value: 16.2745394883
    * key: 2013-04-26, value: 16.2745394883
    * key: 2014-04-26, value: 16.2745394883
    * key: 2015-04-26, value: 16.2745394883
    * key: 2016-04-26, value: 16.2745394883
    * key: 2017-04-26, value: 16.2745394883
    * key: 2018-04-26, value: 16.2745394883
    * key: 2019-04-26, value: 16.2745394883
    * key: 2020-04-26, value: 16.2745394883

    The payments from 2018-04-22 and out is:

    >>> x['2018-04-22':]
    Data for the DateFlow:
    * key: 2018-04-26, value: 16.2745394883
    * key: 2019-04-26, value: 16.2745394883
    * key: 2020-04-26, value: 16.2745394883

    The payments between 2013-01-01 and 2017-01-01 is:

    >>> x['2013-01-01':'2017-01-01']
    Data for the DateFlow:
    * key: 2013-04-26, value: 16.2745394883
    * key: 2014-04-26, value: 16.2745394883
    * key: 2015-04-26, value: 16.2745394883
    * key: 2016-04-26, value: 16.2745394883

    There are no payments between 2022-01-01 and 2032-01-01:

    >>> x['2022-01-01':'2032-01-01']
    Data for the DateFlow:
    *
    >>>
    '''
    @staticmethod
    def __validate_key__(key):
        return BankDate(key)

    def accumulated_dateflow(self):
        ''':return: The accumulated DateFlow
        '''
        selfcopy = self.__class__(self)
        accumulated = 0
        for day in selfcopy.keys():
            selfcopy[day] += accumulated
            accumulated = selfcopy[day]
        return selfcopy

    def find_nearest_bankdate(self, keyvalue, before=True):
        '''
        :param keyvalue: A date
        :type keyvalue: A bankdate, a string in format yyyy-mm-dd or a date
        :param before: if True return nearest date before keyvalue
                       otherwise the nearest after
        :type before: boolean
        :Return: The nearest date in DateFlow (before if before is True
                 otherwise the nearest after) keyvalue.
        '''
        if self.keys() and keyvalue:
            keyvalue = BankDate(keyvalue)
            if keyvalue in self.keys():
                return keyvalue
            else:
                lst = self.keys()
                lst.append(keyvalue)
                lst.sort()
                index = lst.index(keyvalue)
                if 0 < index < len(lst) - 1:
                    if before:
                        return lst[index - 1]
                    else:
                        return lst[index + 1]
                elif index == 0:
                    if before:
                        return
                    else:
                        return lst[1]
                else:
                    if before:
                        return lst[-2]
                    else:
                        return


def dateflow_generator(
                rate,
                enddate_or_integer=1,
                start_date=BankDate(),
                step='1y',
                cashflowtype='Annuity',
                profile='payment'
                ):
    '''A generator of standard DateFlows.

    Steps step backwards from end_date. If enddate_or_integer is an integer

    end_date is calculated as start_date + enddate_or_integer * step

    The dateflow_generator is build upon the datarangeiter.

    :param rate: Fixed rate pr period.
    :type rate: float or decimal
    :param enddate_or_integer: Either end_date or number of dates in daterange
    :type enddate_or_integer: A date or integer
    :param start_date: start_date for daterange iterations.
        Default is current date
    :type start_date: A date
    :param step: The time period between 2 adjacent dates
    :type step: A timeperiod
    :param keepstart_date: Should start_date be in daterange or not
    :type keepstart_date: Boolean
    :param cashflowtype: Name of cashflow type. Default is 'annuity'
    :type cashflowtype: ('annuity', 'bullit, 'series')
    :param profile: Name of cashflow profile. Default is 'payment'
    :type profile: ('payment', 'nominal', 'rate')
    :param keepstart_date: Should start_date be in the list. Default is True
    :type keepstart_date: boolean

    Create payments of an annuity with nominal 100, a rate of 10% and 5 yearly
    payments starting from 2009-11-24.

    Default:
        step = '1y',  cashflowtype = 'Annuity', profile = 'payment'

    >>> dateflow_generator(0.1, 5, '2009-11-24')
    Data for the DateFlow:
    * key: 2009-11-24, value: 0.0
    * key: 2010-11-24, value: 26.3797480795
    * key: 2011-11-24, value: 26.3797480795
    * key: 2012-11-24, value: 26.3797480795
    * key: 2013-11-24, value: 26.3797480795
    * key: 2014-11-24, value: 26.3797480795

    DateFlow can also be generated from the future and back:

    >>> dateflow_generator(0.1, -5, '2014-11-24')
    Data for the DateFlow:
    * key: 2009-11-24, value: 0.0
    * key: 2010-11-24, value: 26.3797480795
    * key: 2011-11-24, value: 26.3797480795
    * key: 2012-11-24, value: 26.3797480795
    * key: 2013-11-24, value: 26.3797480795
    * key: 2014-11-24, value: 26.3797480795

    Several DateFlows can be uptained.
    Below are the nominals of an annuity (default):

    >>> dateflow_generator(0.1, 5, '2009-11-24', profile = 'nominal')
    Data for the DateFlow:
    * key: 2009-11-24, value: 100.0
    * key: 2010-11-24, value: 83.6202519205
    * key: 2011-11-24, value: 65.6025290331
    * key: 2012-11-24, value: 45.7830338569
    * key: 2013-11-24, value: 23.9815891632
    * key: 2014-11-24, value: 0.0

    And the rates of of an annuity (default):

    >>> dateflow_generator(0.1, 5, '2009-11-24', profile = 'rate')
    Data for the DateFlow:
    * key: 2009-11-24, value: 0.0
    * key: 2010-11-24, value: 10.0
    * key: 2011-11-24, value: 8.36202519205
    * key: 2012-11-24, value: 6.56025290331
    * key: 2013-11-24, value: 4.57830338569
    * key: 2014-11-24, value: 2.39815891632

    Create the payments of a bullit with nominal 100, a rate of 10% and 5 yearly
    payments starting from 2009-11-24.

    Default:
        step = '1y', profile = 'payment', keepstart_date = False.

    >>> dateflow_generator(0.1, 5, '2009-11-24', cashflowtype= 'bullit')
    Data for the DateFlow:
    * key: 2009-11-24, value: 0.0
    * key: 2010-11-24, value: 10.0
    * key: 2011-11-24, value: 10.0
    * key: 2012-11-24, value: 10.0
    * key: 2013-11-24, value: 10.0
    * key: 2014-11-24, value: 110.0

    Create the payments a series with nominal 100, a rate of 10% and 5 yearly
    payments starting from 2009-11-24.

    Default:
        step = '1y', profile = 'payment', keepstart_date = False.

    >>> dateflow_generator(0.1, 5, BankDate('2009-11-24'), cashflowtype= 'series')
    Data for the DateFlow:
    * key: 2009-11-24, value: 0.0
    * key: 2010-11-24, value: 30.0
    * key: 2011-11-24, value: 28.0
    * key: 2012-11-24, value: 26.0
    * key: 2013-11-24, value: 24.0
    * key: 2014-11-24, value: 22.0

    [Christensen]_ table 2.3 page 30, payments:

    >>> dateflow_generator(0.035, '2004-07-01', '2001-01-01', '6m', 'annuity', 'payment')
    Data for the DateFlow:
    * key: 2001-01-01, value: 0.0
    * key: 2001-07-01, value: 16.3544493783
    * key: 2002-01-01, value: 16.3544493783
    * key: 2002-07-01, value: 16.3544493783
    * key: 2003-01-01, value: 16.3544493783
    * key: 2003-07-01, value: 16.3544493783
    * key: 2004-01-01, value: 16.3544493783
    * key: 2004-07-01, value: 16.3544493783

    [Christensen]_ table 2.3 page 30, rates:

    >>> dateflow_generator(0.035, '2004-07-01', '2001-01-01', '6m', 'annuity', 'rate')
    Data for the DateFlow:
    * key: 2001-01-01, value: 0.0
    * key: 2001-07-01, value: 3.5
    * key: 2002-01-01, value: 3.05009427176
    * key: 2002-07-01, value: 2.58444184303
    * key: 2003-01-01, value: 2.10249157929
    * key: 2003-07-01, value: 1.60367305633
    * key: 2004-01-01, value: 1.08739588506
    * key: 2004-07-01, value: 0.553049012794

    [Christensen]_ table 2.3 page 30, nominals:

    >>> dateflow_generator(0.035, '2004-07-01', '2001-01-01', '6m', 'annuity', 'nominal')
    Data for the DateFlow:
    * key: 2001-01-01, value: 100.0
    * key: 2001-07-01, value: 87.1455506217
    * key: 2002-01-01, value: 73.8411955151
    * key: 2002-07-01, value: 60.0711879798
    * key: 2003-01-01, value: 45.8192301808
    * key: 2003-07-01, value: 31.0684538588
    * key: 2004-01-01, value: 15.8014003655
    * key: 2004-07-01, value: 0.0

    '''
    def annuity_generator(
        rate,
        nbr_of_payments = 1,
        start_date = BankDate(),
        step = '1y'
        ):
        '''annuity'''
        discount = 1 / (1 + rate)
        if nbr_of_payments > 0:
            payment = 100 * rate / (1.0 - discount ** nbr_of_payments)
        else:
            payment = 100 * (1.0 / discount - 1) \
                        / (1.0 - discount ** -nbr_of_payments)
        accumulated_discount = 1.0
        nominal = 0.0
        for payday in daterange_iter(nbr_of_payments, start_date, step, False):
            accumulated_discount *= discount
            yield {
                'payday': payday,
                'nominal': nominal,
                'payment': payment,
                'rate': payment * (1 - accumulated_discount)
                }
            nominal += payment * accumulated_discount
        if nbr_of_payments > 0:
            yield {
                'payday': start_date,
                'nominal': nominal,
                'payment': 0.0,
                'rate': 0.0
                }
        else:
            yield {
                'payday': payday - step,
                'nominal': 100.0,
                'payment': 0.0,
                'rate': 0.0
                }

    def bullit_generator(
        rate,
        nbr_of_payments = 1,
        start_date = BankDate(),
        step = '1y'
        ):
        '''A bullit'''
        discount = 1 / (1 + rate)
        payment = 100 / discount
        nominal = 0.0
        rate = payment - 100
        for payday in daterange_iter(nbr_of_payments, start_date, step, False):
            yield {
                'payday': payday,
                'nominal': nominal,
                'payment': payment,
                'rate': rate
                }
            if not nominal :
                nominal,  payment = 100.0,  rate
        if nbr_of_payments > 0:
            yield {
                'payday': start_date,
                'nominal': nominal,
                'payment': 0.0,
                'rate': 0.0
                }
        else:
            yield {
                'payday': payday - step,
                'nominal': 100.0,
                'payment': 0.0,
                'rate': 0.0
                }

    def series_generator(
        rate,
        nbr_of_payments = 1,
        start_date = BankDate(),
        step = '1y'
        ):
        '''Series'''
        discount = 1 / (1 + rate)
        nominal = 0.0
        nominal_step = 100.0 / abs(nbr_of_payments)
        for payday in daterange_iter(nbr_of_payments, start_date, step, False):
            rate = (nominal + nominal_step) *  (1 / discount - 1)
            yield {
                'payday': payday,
                'nominal': nominal,
                'payment': nominal_step + rate,
                'rate': rate
                }
            nominal += nominal_step
        if nbr_of_payments > 0:
            yield {
                'payday': start_date,
                'nominal': nominal,
                'payment': 0.0,
                'rate': 0.0
                }
        else:
            yield {
                'payday': payday - step,
                'nominal': 100.0,
                'payment': 0.0,
                'rate': 0.0
                }

    # Main dateflow_generator
    if not 0 < rate < 1:
        raise DateFlowError, 'Rate (%s) must be a float between 0 and 1' \
            % rate
    cashflowdict = {
        'annuity': annuity_generator,
        'bullit': bullit_generator,
        'series': series_generator
        }
    if cashflowtype.lower() in cashflowdict.keys():
        if isinstance(enddate_or_integer,  int):
            nbr_of_payments = enddate_or_integer
        else:
            nbr_of_payments = period_count(enddate_or_integer, start_date, step)
        generator = cashflowdict[cashflowtype.lower()] \
                    (rate, nbr_of_payments, start_date, step)
    else:
        raise DateFlowError, \
        'Cashflowtype (%s) must be one of %s' \
        % (cashflowtype.lower(), cashflowdict.keys())
    profilelst = ('nominal', 'payment', 'rate')
    if profile.lower() in profilelst:
        return sum(DateFlow({row['payday']: row[profile.lower()]})
                for row in generator)
    else:
        raise DateFlowError, \
        'Profile (%s) must be one of %s' % (profile.lower(), profilelst)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
