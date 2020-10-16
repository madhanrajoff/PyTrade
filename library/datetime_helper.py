import datetime as dt
import dateutil.relativedelta as r_delta
import dateutil.parser as dtp
import pytz
import unittest


class DatetimeHelper:

    @classmethod
    def now_utc(cls, tz=pytz.utc):
        now = dt.datetime.utcnow()
        now = now.replace(tzinfo=tz)
        return now

    @classmethod
    def now_new_york(cls, tz=pytz.timezone("America/New_York")):
        now = dt.datetime.utcnow()
        now = now.replace(tzinfo=tz)
        return now

    @classmethod
    def market_open_at(cls):
        open_at = cls.now_new_york()
        open_at = open_at.replace(hour=9, minute=30, second=0, microsecond=0)
        return open_at

    @classmethod
    def market_close_at(cls):
        close_at = cls.now_new_york()
        close_at = close_at.replace(hour=16, minute=00, second=0, microsecond=0)
        return close_at

    @classmethod
    def is_market_opened(cls):
        return cls.market_open_at() < cls.now_new_york() < cls.market_close_at()

    @classmethod
    def to_str(cls, datetime):
        if datetime is None:
            return None
        # order is important - a datetime is a date but a date is not a datetime
        if isinstance(datetime, dt.datetime):
            dt_str = datetime.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(datetime, dt.date):
            dt_str = datetime.strftime("%Y-%m-%d")
        else:
            raise DTHelperError(F"datetime argument is of type {str(type(datetime))}, not date or datetime")
        return dt_str

    @classmethod
    def to_json(cls, value):
        if value is None:
            return None
        # order is important - a datetime is a date but a date is not a datetime
        if isinstance(value, dt.datetime):
            dtj = value.isoformat()
        elif isinstance(value, dt.date):
            dtj = value.isoformat()
        elif isinstance(value, dt.time):
            dtj = value.isoformat()
        else:
            raise DTHelperError(F"Argument is of type {str(type(value))}, not date, time or datetime")
        return dtj

    @classmethod
    def dt_from_string(cls, dt_str: str, tz=pytz.utc):
        if dt_str is None:
            return None
        datetime = dtp.parse(dt_str)
        udatetime = cls.add_tz(datetime, tz=tz)
        return udatetime

    @classmethod
    def from_timestamp(cls, timestamp, tz=None):
        if timestamp is None:
            return None
        dtv = dt.datetime.utcfromtimestamp(timestamp)
        if tz:
            dtv = cls.add_tz(dtv, tz=tz)
        return dtv

    @classmethod
    def from_qb_timestamp(cls, timestamp: str):
        if timestamp is None:
            return None
        assert isinstance(timestamp, str), F"String expected; not: {str(timestamp)}"

        datetime = dt.datetime.utcfromtimestamp(int(timestamp) / float(1000))
        return datetime

    @classmethod
    def add_tz(cls, datetime: dt.datetime, tz=pytz.utc):
        udatetime = datetime.replace(tzinfo=tz)
        return udatetime

    @classmethod
    def utc2local(cls, datetime, local_tz=pytz.timezone("US/Pacific")):
        local_dt = datetime.astimezone(local_tz).strftime("%m-%d-%Y %I:%M %p%z")
        return local_dt

    @classmethod
    def date_from_timestamp(cls, timestamp: int, tz=pytz.utc):
        dtv = cls.from_timestamp(timestamp, tz=tz)
        return cls.date_from_dt(dtv)

    @classmethod
    def date_from_dt(cls, datetime: dt.datetime):
        return datetime.date() if datetime else None

    @classmethod
    def dt_from_date(cls, datev: dt.date):
        if datev is None:
            return None
        dtv = dt.datetime(datev.year, datev.month, datev.day)
        return dtv

    @classmethod
    def date_difference(cls, dt1, dt2):
        dt_diff: dt.timedelta = dt1 - dt2
        days_diff = dt_diff.days
        return abs(days_diff)

    # Function to turn a datetime object into unix
    @classmethod
    def unix_time_millis(cls, datetime: dt.datetime, tz=pytz.utc):
        epoch = dt.datetime.utcfromtimestamp(0).replace(tzinfo=tz)
        return int((datetime - epoch).total_seconds() * 1000.0)

    @classmethod
    def month_delta(cls, datetime: dt.datetime, months=1):
        return datetime - r_delta.relativedelta(months=months)

    @classmethod
    def day_delta(cls, datetime: dt.datetime, days=1):
        return datetime - r_delta.relativedelta(days=days)


class DTHelperTests(unittest.TestCase):

    def test_to_str(self):
        dtv = DatetimeHelper.dt_from_string("10/30/2019 15:30")
        sdt = DatetimeHelper.to_str(dtv)
        dav = dtv.date()
        sda = DatetimeHelper.to_str(dav)

        self.assertEqual(sdt, "2019-10-30 15:30:00")
        self.assertEqual(sda, "2019-10-30")

    def test_days_diff(self):
        dtv1 = DatetimeHelper.dt_from_string("10/15/2019 15:30")
        dtv2 = DatetimeHelper.dt_from_string("10/30/2019 15:30")
        days_diff = DatetimeHelper.date_difference(dtv1, dtv2)

        self.assertEqual(0, 0)
