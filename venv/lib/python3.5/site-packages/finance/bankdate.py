#############################################################################
# The finance package is open source under the `Python Software Foundation  #
# License <http://www.opensource.org/licenses/PythonSoftFoundation.php>`_   #
#############################################################################

'''Containing tools for handling dates and periods
'''

from datetime import date as _pythondate
from datetime import timedelta, datetime
from mathematical_meta_code import CummutativeAddition, \
                                   CummutativeMultiplication
import re


class BankDateError(Exception):
    '''A class to implement error messages from class BankDate.'''
    pass


class TimePeriod(CummutativeAddition, CummutativeMultiplication):
    '''A TimePeriod is a string containing an (positive or negative) integer
    called count and a character like d(days), m(months) or y(years) called
    unit.
    It is used for handling generic time periods.

    **How to use!**

    Instantiation:

    >>> x = TimePeriod('2y')

    How to get get the string representation and the values count and unit:

    >>> x, x.count, x.unit
    (2y, 2, 'y')

    *Operator overload*

    By using operator overload it is possible to do TimePeriod calculations
    quite easy.
    A TimePeriod can be added or subtracted an integer (same unit is assumed):

    >>> 5 + x, x - 5
    (7y, -3y)

    A period can be multiplied by an integer:

    >>> x * 5, 5 * TimePeriod('2y') + TimePeriod('2y')
    (10y, 12y)

    TimePeriods can be compared, if they have the same unit:

    >>> TimePeriod('2y') > TimePeriod('1y')
    True
    >>> TimePeriod('2y') < TimePeriod('1y')
    False
    >>> try:
    ...         TimePeriod('2m') < TimePeriod('1y')
    ... except Exception, errorText:
    ...         print errorText
    ...
    Non comparable units (m) vs (y)

    '''
    def __init__(self, period):
        '''A TimePeriod can be instantiated by a TimePeriod or a string of
        the form an integer followed by a "d" (days),  "w" (weeks),
        "m" (months) or "y" (years)
        '''
        self._count = None
        self._unit = None
        if isinstance(period,  TimePeriod):
            self._count = period.count
            self._unit = period.unit
        elif isinstance(period,  str):
            validate_period_ok = re.search('^(-?\d*)([d|w|m|y])$', period)
            if validate_period_ok:
                self._count, self._unit = validate_period_ok.groups()
                self._count = int(self._count)

    def __nonzero__(self):
        return 0 if self._count == None else 1

    def __str__(self):
        '''String representation'''
        return '%s%s' % (self._count,  self._unit)

    __repr__ = __str__

    def __abs__(self):
        result = self.__class__(self)
        result.count = abs(result.count)
        return result

    def __neg__(self):
        result = self.__class__(self)
        result.count = -result.count
        return result

    def __add__(self, added_value):
        '''A TimePeriod can be added an integer. Same unit is assumed
        '''
        result = self.__class__(self)
        if isinstance(added_value, int):
            result.count += added_value
            return result
        if isinstance(added_value, TimePeriod):
            result.count += added_value.count
            return result

    def __rsub__(self, added_value):
        '''An integer can be subtracted a TimePeriod. Same unit is assumed.
        '''
        return self.__add__(- added_value)

    def __mul__(self, value):
        '''TimePeriods can be multiplied with an integer.
        '''
        if isinstance(value, int):
            result = self.__class__(self)
            result.count *= value
            return result

    def __div__(self, value):
        '''TimePeriods can be multiplied with an integer.
        '''
        if isinstance(value, int):
            result = self.__class__.__init__(self)
            result.count *= value
            return result

    def __rdiv__(self, other_value):
        return

    def __cmp__(self, period):
        '''TimePeriods can be compared if they have the same unit.
        '''
        if isinstance(period,  TimePeriod):
            if self.unit == period.unit:
                if self.count == period.count:
                    return 0
                elif self.count < period.count:
                    return -1
                elif self.count > period.count:
                    return 1
            else:
                raise BankDateError(
                'Non comparable units (%s) vs (%s)'
                % (self.unit,  period.unit))
        else:
            raise BankDateError(
            'Can not compare a TimePeriod with %s of type %s'
            % (period,  type(period)))

    def _get_count(self):
        '''Integer part of TimePeriod.
        '''
        return self._count

    def _set_count(self, value):
        '''set value of poperty count, type integer.'''
        if isinstance(value, int):
            self._count = value
        else:
            raise BankDateError('Value must be an integer, not (%s) of type %s'
                                    % (value,  type(value)))

    count = property(_get_count, _set_count)

    def _get_unit(self):
        '''Unit part [y(ears), m(onths) or d(ays)] of TimePeriod.
        '''
        return self._unit

    unit = property(_get_unit)


class BankDate(_pythondate):
    '''A class to implement (non generic) banking day calculations.

    **How to use!**

    BankDate could instantiated by a string of type yyyy-mm-dd,
    a python date or a BankDate itself:

    >>> from datetime import date
    >>> td = BankDate('2009-09-25')
    >>> td
    2009-09-25
    >>> print BankDate(date(2009,9,25))
    2009-09-25
    >>> print BankDate(td)
    2009-09-25

    When instantiating default is today.

    A BankDate can be added a number of years, months or days:

    >>> print td.add_years(5)
    2014-09-25
    >>> print td.add_months(-3)
    2009-06-25
    >>> print td.add_days(14)
    2009-10-09

    The differences between 2 dates can also be found:

    >>> print td.nbr_of_years('2014-09-25')
    5
    >>> print td.nbr_of_months('2009-06-25')
    -3
    >>> print td.nbr_of_days('2009-10-09')
    14

    Finding next banking day / BankDate:

    >>> d = BankDate('2009-09-27')
    >>> print d.find_next_banking_day(1, ['2009-09-28'])
    2009-09-29

    Finding previous banking day / BankDate:

    >>> print d.find_next_banking_day(-1, ['2009-09-28'])
    2009-09-25

    It is also possible to adjust to nearest banking day:

    >>> d = BankDate('2009-10-31')
    >>> d.adjust_to_bankingday('Actual')
    2009-10-31
    >>> d.adjust_to_bankingday('Following')
    2009-11-02
    >>> d.adjust_to_bankingday('Previous')
    2009-10-30
    >>> d.adjust_to_bankingday('ModifiedFollowing')
    2009-10-30
    >>> BankDate('2009-11-02').adjust_to_bankingday('ModifiedPrevious')
    2009-11-02

    *Using operator overload:*

    By using operator overload it is more simple to handle calculations with
    BankDates and TimePeriods. The last represented by its string
    representation.

    >>> td = BankDate('2009-09-25')
    >>> print td + '5y', '5y' + td
    2014-09-25 2014-09-25
    >>> print td - '3m', '-3m' + td
    2009-06-25 2009-06-25
    >>> print td +'2w', '2w' + td
    2009-10-09 2009-10-09
    >>> print td +'14d', '14d' + td
    2009-10-09 2009-10-09
    >>> td - (td + '2d')
    -2

    It is possible to do more complicated updates at once:

    >>> t1, t2 = BankDate(date(2009,12,27)), BankDate('2009-09-27')
    >>> print t1 + '3m' + '2y'
    2012-03-27
    >>> print t2-t1, t1-t2
    -91 91

    BankDates can be compared:

    >>> td = BankDate('2009-09-28')
    >>> print td
    2009-09-28
    >>> td <= BankDate('2009-09-28')
    True
    >>> td == BankDate('2009-09-28')
    True
    >>> td == BankDate('2009-09-27')
    False

    A BankDate can be added years, months or days and *be updated to the new
    date*

    >>> d = BankDate('2009-09-30')
    >>> d+='3m'

    Checking modulo a year calculations
    >>> print d
    2009-12-30
    >>> [BankDate('2014-02-25') - '%dm' % i for i in range(0,4)]
    [2014-02-25, 2014-01-25, 2013-12-25, 2013-11-25]
    >>> [BankDate('2014-02-25') - '%dm' % i for i in range(13,16)]
    [2013-01-25, 2012-12-25, 2012-11-25]
    >>> [BankDate('2014-02-25') + '%dm' % i for i in range(21,24)]
    [2015-11-25, 2015-12-25, 2016-01-25]
    >>> [BankDate('2014-02-25') + '%dm' % i for i in range(8,12)]
    [2014-10-25, 2014-11-25, 2014-12-25, 2015-01-25]
    '''

    def __new__(self, bank_date=_pythondate.today()):
        day = None
        if isinstance(bank_date, str):
            try:
                day = datetime.strptime(bank_date, "%Y-%m-%d").date()
            except:
                pass
        elif isinstance(bank_date, _pythondate):
            day = bank_date
        elif isinstance(bank_date, BankDate):
            day = bank_date.date()
        if day:
            return super(BankDate, self).__new__(self,
                                                 day.year,
                                                 day.month,
                                                 day.day
                                                 )
        else:
            return None

    def __str__(self):
        return '%4d-%02d-%02d' % (self.year, self.month, self.day)

    __repr__ = __str__

    def __add__(self, period):
        '''A TimePeriod can be added to a BankDate
        '''
        period = TimePeriod(period)
        if period:
            if period.unit == 'y':
                return self.__class__(self).add_years(period.count)
            elif period.unit == 'm':
                return self.__class__(self).add_months(period.count)
            elif period.unit == 'w':
                return self.__class__(self).add_days(7 * period.count)
            elif period.unit == 'd':
                return self.__class__(self).add_days(period.count)

    def __radd__(self, period):
        '''A BankDate can be added to a TimePeriod
        '''
        return self.__add__(period)

    def __iadd__(self, period):
        '''A TimePeriod can be added to a BankDate
        '''
        return self.__add__(period)

    def __sub__(self, value):
        '''A BankDate can be subtracted either a TimePeriod or a BankDate
        giving a BankDate or the number of days between the 2 BankDates
        '''
        period = TimePeriod(value)
        if period:
            return self.__class__(self).__add__(-period)
        else:
            return -self.nbr_of_days(value)

    def __rsub__(self, date):
        '''A TimePeriod or a BankDate can be subtracted a BankDate giving a
        BankDate or the number of days between the 2 BankDates
        '''
        return self.__sub__(date)

    @staticmethod
    def ultimo(nbr_month):
        '''Return last day of month for a given number of month.

        :param nbr_month: Number of month
        :type nbr_month: int
        '''
        if isinstance(nbr_month, int):
            ultimo_month = {2: 28, 4: 30, 6: 30, 9: 30, 11: 30}
            if nbr_month in ultimo_month:
                return ultimo_month[nbr_month]
            else:
                return 31

    def is_ultimo(self):
        '''Identifies if BankDate is ultimo'''
        return BankDate.ultimo(self.month) == self.day

    def add_months(self, nbr_months):
        '''Adds nbr_months months to the BankDate.

        :param nbr_months: Number of months to be added
        :type nbr_months: int
        '''
        if isinstance(nbr_months, int):
            totalmonths = self.month + nbr_months
            year = self.year + totalmonths // 12
            if not totalmonths % 12:
                year -= 1
            month = totalmonths % 12 or 12
            day = min(self.day, BankDate.ultimo(month))
            return BankDate(_pythondate(year, month, day))

    def add_years(self, nbr_years):
        '''Adds nbr_years years to the BankDate.

        :param nbr_years: Number of years to be added
        :type nbr_years: int

         '''
        if isinstance(nbr_years, int):
            result = _pythondate(self.year + nbr_years, self.month, self.day)
            return BankDate(result)

    def add_days(self, nbr_days):
        '''Adds nbr_days days to the BankDate.

        :param nbr_days: Number of days to be added
        :type nbr_days: int
         '''
        if isinstance(nbr_days, int):
            result = _pythondate(self.year, self.month, self.day) + timedelta(nbr_days)
            return BankDate(result)

    def find_next_banking_day(self, nextday=1, holidaylist=()):
        '''A workingday can not be saturday or sunday.

        :param nextday: Tells wether to use previous (-1) or following
                        (+1) workingday
        :type nextday: -1, +1
        :param holidaylist: A list of holiday BankDates
        :type holidaylist: A list of BankDates or strings in format
                            'yyyy-mm-dd'
        :return: Next or previous working day given a holidaylist.
            Return itself if not in weekend or a holiday
        '''
        if nextday not in (-1, 1):
            raise BankDateError(
            'The nextday must be  in (-1, 1), not %s of type %s'
            % (nextday, type(nextday)))
        lst = [BankDate(d).__str__() for d in holidaylist]
        date = self
        for i in range(30):
            if date.isoweekday() < 6 and str(date) not in lst:
                break
            date = date.add_days(nextday)
        return date

    def adjust_to_bankingday(self, daterolling='Actual', holidaylist=()):
        '''Adjust to banking day according to date rolloing rule and list of
        holidays.

        Reference: http://en.wikipedia.org/wiki/Date_rolling

        :param daterolling: Name of date rolling. Default is Actual
        :type daterolling: 'Actual', 'Following', 'Previous',
            'ModifiedFollowing', 'ModifiedPrevious'
        :param holidaylist: A list of holiday BankDates
        :type holidaylist: A list of BankDates or strings in format
                            'yyyy-mm-dd'
        :return: Adjusted banking day
        '''

        def actual_daterolling(holidaylist):
            '''Implement date rolling method Actual, ie no change
            '''
            return self

        def following_daterolling(holidaylist):
            '''Implement date rolling method Following
            '''
            return self.find_next_banking_day(1, holidaylist)

        def previous_daterolling(holidaylist):
            '''Implement date rolling method Previous
            '''
            return self.find_next_banking_day(-1, holidaylist)

        def modified_following_daterolling(holidaylist):
            '''Implement date rolling method Modified Following
            '''
            next_bd = self.find_next_banking_day(1, holidaylist)
            if self.month == next_bd.month:
                return next_bd
            else:
                return self.find_next_banking_day(-1, holidaylist)

        def modified_previous_daterolling(holidaylist):
            '''Implement date rolling method Modified Previous
            '''
            next_bd = self.find_next_banking_day(-1, holidaylist)
            if self.month == next_bd.month:
                return next_bd
            else:
                return self.find_next_banking_day(1, holidaylist)

        daterolling_dict = {
            'Actual':             actual_daterolling,
            'Following':          following_daterolling,
            'Previous':           previous_daterolling,
            'ModifiedFollowing':  modified_following_daterolling,
            'ModifiedPrevious':   modified_previous_daterolling,
            }
        if daterolling in daterolling_dict.keys():
            return daterolling_dict[daterolling](holidaylist)
        else:
            raise BankDateError(
            'The daterolling must be one of %s, not %s of type %s' \
            % (daterolling_dict.keys(), daterolling, type(daterolling)))

    def weekday(self, as_string=False):
        '''
        :param as_string: Return weekday as a number or a string
        :type as_string: Boolean
        :Return: day as a string or a day number of week, 0 = Monday etc
        '''
        if as_string:
            return self.strftime('%a')
        else:
            return self.weekday()

    def first_day_in_month(self):
        ''':Return: first day in month for this BankDate as BankDate
        '''
        day = self.day
        return self + '%sd' % (1 - day)

    def next_imm_date(self, future=True):
        '''An IMM date is the 3. wednesday in the months march, june,
        september and december

        reference: http://en.wikipedia.org/wiki/IMM_dates

        :Return: Next IMM date for BankDate as BankDate
        '''
        month = self.month
        if future:
            add_month = 3 - (month % 3)
        else:
            add_month = - ((month % 3) or 3)
        # First day in imm month
        out_date = self.first_day_in_month() + '%sm' % add_month
        add_day = 13 + (9 - out_date.weekday()) % 6
        out_date += '%sd' % add_day
        return out_date

    def nbr_of_months(self, date):
        '''
        :param date: date
        :type date: BankDate
        :return: The number of months between this bankingday and a date
        '''
        date = BankDate(date)
        if self.__str__() < date.__str__():
            date_min, date_max = self, date
            sign = +1
        else:
            date_min, date_max = date, self
            sign = -1
        nbr_month = (date_max.year - date_min.year) * 12 \
                    + date_max.month - date_min.month
        if date_max.day >= date_min.day:
            return sign * nbr_month
        else:
            return sign * (nbr_month - 1)

    def nbr_of_years(self, date):
        '''
        :param date: date
        :type date: BankDate
        :return: The number of years between this bankingday and a date
        '''
        nom = self.nbr_of_months(date)
        if nom > 0:
            return int(nom / 12)
        else:
            return - int(-nom / 12)

    def nbr_of_days(self, value):
        '''
        :param date: date
        :type date: BankDate
        :return: The number of days between this bankingday and a date
        '''
        bankdate = BankDate(value)
        if bankdate:
            # Subtraction is defined for _pythondate
            return -super(BankDate, self).__sub__(bankdate).days


def daterange_iter(
        enddate_or_integer,
        start_date=BankDate(),
        step='1y',
        keep_start_date=True,
        daterolling='Actual',
        holidaylist=()
        ):
    '''
    :param enddate_or_integer: Either end_date or number of dates in daterange
    :type enddate_or_integer: A date or integer
    :param start_date: start_date for daterange iterations.
        Default is current date
    :type start_date: A date
    :param step: The time period between 2 adjacent dates
    :type step: A TimePeriod
    :param keep_start_date: Should start_date be in daterange or not
    :type keep_start_date: Boolean
    :param daterolling: Name of date rolling. Default is Actual
    :type daterolling: 'Actual', 'Following', 'Previous',
        'ModifiedFollowing', 'ModifiedPrevious'
    :type holidaylist: A list of BankDates or strings in format 'yyyy-mm-dd'


    **if enddate_or_integer is an integer:**

    :return: A list of dates starting from start_date and enddate_or_integer
            steps forward

    **if enddate_or_integer is a date:**

    :return: A list of dates starting from enddate_or_integer and steps
            backward until start_date

    **How to use!**

    The next 5 dates (period a year) from 2009-11-23. start_date is included.

    >>> for d in daterange_iter(5, '2009-11-23'):
    ...     print d
    ...
    2014-11-23
    2013-11-23
    2012-11-23
    2011-11-23
    2010-11-23
    2009-11-23

    Taking date rolling and holidays into account.

    >>> for d in daterange_iter(5, '2009-11-23', daterolling='Following', holidaylist=['2011-11-23']):
    ...     print d, d.weekday(True)
    ...
    2014-11-24 Mon
    2013-11-25 Mon
    2012-11-23 Fri
    2011-11-24 Thu
    2010-11-23 Tue
    2009-11-23 Mon

    Countdown (period a year) from the future 2014-11-23. start_date is
    included.

    >>> for d in daterange_iter(-5, '2014-11-23'):
    ...     print d
    ...
    2014-11-23
    2013-11-23
    2012-11-23
    2011-11-23
    2010-11-23
    2009-11-23

    Countdown (period a year) from the future 2014-11-23. start_date is not
    included, ie. the smallest date.

    >>> for d in daterange_iter(-5, '2014-11-23', keep_start_date = False):
    ...     print d
    ...
    2014-11-23
    2013-11-23
    2012-11-23
    2011-11-23
    2010-11-23

    Countdown (period minus a year) from the future 2014-11-23.
    start_date is included.

    >>> for d in daterange_iter(5, '2014-11-23', '-1y'):
    ...     print d
    ...
    2014-11-23
    2013-11-23
    2012-11-23
    2011-11-23
    2010-11-23
    2009-11-23

    Both countdowns repeal each other.

    >>> for d in daterange_iter(-5, '2009-11-23', '-1y'):
    ...     print d
    ...
    2014-11-23
    2013-11-23
    2012-11-23
    2011-11-23
    2010-11-23
    2009-11-23

daterange_iter handles almost ultimo dates:

    >>> for d in daterange_iter(-12, '2013-05-30', daterolling='ModifiedFollowing', step='3m'):
    ...     print d, d.weekday(True)
    ...
    2013-05-30 Thu
    2013-02-28 Thu
    2012-11-30 Fri
    2012-08-30 Thu
    2012-05-30 Wed
    2012-02-28 Tue
    2011-11-30 Wed
    2011-08-30 Tue
    2011-05-30 Mon
    2011-02-28 Mon
    2010-11-30 Tue
    2010-08-30 Mon
    2010-05-31 Mon

And daterange_iter handles ultimo dates:

    >>> for d in daterange_iter(-12, '2013-05-31', daterolling='ModifiedFollowing', step='3m'):
    ...     print d, d.weekday(True)
    ...
    2013-05-31 Fri
    2013-02-28 Thu
    2012-11-30 Fri
    2012-08-31 Fri
    2012-05-31 Thu
    2012-02-28 Tue
    2011-11-30 Wed
    2011-08-31 Wed
    2011-05-31 Tue
    2011-02-28 Mon
    2010-11-30 Tue
    2010-08-31 Tue
    2010-05-31 Mon
    '''
    s_date = BankDate(start_date)
    step = TimePeriod(step)
    if isinstance(enddate_or_integer,  int):
        e_date = s_date + enddate_or_integer * step
    else:
        e_date = BankDate(enddate_or_integer)
    if e_date < s_date:
        s_date, e_date = e_date, s_date
    step.count = -abs(step.count)
    nbr_periods = 0
    tmp_date = e_date
    while tmp_date > s_date:
        yield tmp_date.adjust_to_bankingday(daterolling, holidaylist)
        nbr_periods += 1
        tmp_date = e_date + nbr_periods * step
    if keep_start_date:
        yield s_date.adjust_to_bankingday(daterolling, holidaylist)


def daterange(
        enddate_or_integer,
        start_date=BankDate(),
        step='1y',
        keep_start_date=True,
        daterolling='Actual',
        holidaylist=()
        ):
    '''Daterange returns a sorted list of BankDates.

    :param enddate_or_integer: Either end_date or number of dates in daterange
    :type enddate_or_integer: A date or integer
    :param start_date: start_date for daterange iterations.
        Default is current date
    :type start_date: A date
    :param step: The time period between 2 adjacent dates
    :type step: A TimePeriod
    :param keep_start_date: Should start_date be in daterange or not
    :type keep_start_date: Boolean
    :param daterolling: Name of date rolling. Default is Actual
    :type daterolling: 'Actual', 'Following', 'Previous',
        'ModifiedFollowing', 'ModifiedPrevious'
    :type holidaylist: A list of BankDates or strings in format 'yyyy-mm-dd'


    **if enddate_or_integer is an integer:**

    :return: A list of dates starting from start_date and enddate_or_integer
                steps forward

    **if enddate_or_integer is a date:**

    :return: A list of dates starting from enddate_or_integer and steps
                backward until start_date

    **How to use!**

    Get the next 5 dates from 2009-11-23 with a time step of 1 year.
    start_date is included.

    >>> daterange(5, '2009-11-23')
    [2009-11-23, 2010-11-23, 2011-11-23, 2012-11-23, 2013-11-23, 2014-11-23]

    Get the dates between 2009-11-23 and 2012-11-30 with a time step of 3
    months.
    Start_date is not included.

    >>> daterange('2010-11-30', '2009-11-23', '3m', False)
    [2009-11-30, 2010-02-28, 2010-05-30, 2010-08-30, 2010-11-30]

    Get the dates between 2009-11-23 and 2012-11-30 with a time step of 1 year.
    start_date is included.

    >>> daterange('2012-11-30', '2009-11-23')
    [2009-11-23, 2009-11-30, 2010-11-30, 2011-11-30, 2012-11-30]

    Get the dates between 2009-11-23 and 2012-11-30 with a time step of 1 year.
    start_date is not included.

    >>> daterange('2012-11-30', '2009-11-23', '1y', False)
    [2009-11-30, 2010-11-30, 2011-11-30, 2012-11-30]

    '''
    return sorted(daterange_iter(enddate_or_integer, start_date, step,
                    keep_start_date, daterolling, holidaylist))


def period_count(end_date, start_date=BankDate(), period='1y'):
    '''
    :param enddate_or_integer: Either end_date or number of dates in daterange
    :type enddate_or_integer: A date or integer
    :param start_date: start_date for daterange iterations.
        Default is current date
    :type start_date: A date
    :param step: The time period between 2 adjacent dates
    :type step: A TimePeriod
    :return: number (integer) of steps from end_date down to start_date

    **How to use!**

    >>> period_count('2012-11-30', '2009-11-23', '1y')
    4
    '''
    return len(list(daterange_iter(end_date,  start_date, period,  False)))

if __name__ == '__main__':
    import doctest
    doctest.testmod()