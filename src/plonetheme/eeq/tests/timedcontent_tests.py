from datetime import datetime, timedelta

import unittest


class TestTimedContent(unittest.TestCase):
    """Tests for the isExpired logic in timedcontent.py"""

    def _date(self, year, month, day):
        return datetime(year, month, day, 0, 0, 0)

    def is_expired_actual(self, pub_date, exp_date, now):
        """Logic for determining expired state with actual dates"""
        if pub_date < exp_date:
            return not (pub_date <= now < exp_date)
        else:
            return exp_date <= now < pub_date

    def is_expired_annual(self, pub_date, exp_date, now):
        """Logic for determining expired state on an annual basis"""
        if exp_date < pub_date:
            # error condition that should be avoided
            return True
        pub_DoY = int(pub_date.strftime('%-j'))
        exp_DoY = int(exp_date.strftime('%-j'))
        now_DoY = int(now.strftime('%-j'))
        if pub_date.year == exp_date.year:
            return not (pub_DoY <= now_DoY < exp_DoY)
        else:
            return exp_DoY <= now_DoY < pub_DoY

    def test_actual__normal__before(self):
        """Now ---- Publication ---- Expiration"""
        now = self._date(2018, 2, 1)
        pub_date = self._date(2018, 4, 1)
        exp_date = self._date(2018, 8, 1)
        self.assertTrue(self.is_expired_actual(pub_date, exp_date, now))

    def test_actual__normal__pub(self):
        """Now/Publication ---- Expiration"""
        now = self._date(2018, 4, 1)
        pub_date = self._date(2018, 4, 1)
        exp_date = self._date(2018, 8, 1)
        self.assertFalse(self.is_expired_actual(pub_date, exp_date, now))

    def test_actual__normal__in(self):
        """Publication ---- Now ---- Expiration"""
        pub_date = self._date(2018, 4, 1)
        now = self._date(2018, 6, 1)
        exp_date = self._date(2018, 8, 1)
        self.assertFalse(self.is_expired_actual(pub_date, exp_date, now))

    def test_actual__normal__exp(self):
        """Publication ---- Now/Expiration"""
        pub_date = self._date(2018, 4, 1)
        now = self._date(2018, 8, 1)
        exp_date = self._date(2018, 8, 1)
        ### FAILING
        self.assertTrue(self.is_expired_actual(pub_date, exp_date, now))

    def test_actual__normal__just_exp(self):
        """Publication ---- Expiration - Now"""
        pub_date = self._date(2018, 4, 1)
        exp_date = self._date(2018, 8, 1)
        now = datetime(2018, 8, 1, 1, 0, 0)
        self.assertTrue(self.is_expired_actual(pub_date, exp_date, now))

    def test_actual__normal__after(self):
        """Publication ---- Expiration ---- Now"""
        pub_date = self._date(2018, 4, 1)
        exp_date = self._date(2018, 8, 1)
        now = self._date(2018, 9, 1)
        self.assertTrue(self.is_expired_actual(pub_date, exp_date, now))



    def test_actual__reversed__before(self):
        """Now ---- Expiration ---- Publication"""
        now = self._date(2018, 2, 1)
        exp_date = self._date(2018, 4, 1)
        pub_date = self._date(2018, 8, 1)
        self.assertFalse(self.is_expired_actual(pub_date, exp_date, now))

    def test_actual__reversed__exp(self):
        """Now/Expiration ---- Publication"""
        now = self._date(2018, 4, 1)
        exp_date = self._date(2018, 4, 1)
        pub_date = self._date(2018, 8, 1)
        self.assertTrue(self.is_expired_actual(pub_date, exp_date, now))

    def test_actual__reversed__in(self):
        """Expiration ---- Now ---- Publication"""
        exp_date = self._date(2018, 4, 1)
        now = self._date(2018, 6, 1)
        pub_date = self._date(2018, 8, 1)
        self.assertTrue(self.is_expired_actual(pub_date, exp_date, now))

    def test_actual__reversed__pub(self):
        """Expiration ---- Now/Publication"""
        exp_date = self._date(2018, 4, 1)
        now = self._date(2018, 8, 1)
        pub_date = self._date(2018, 8, 1)
        self.assertFalse(self.is_expired_actual(pub_date, exp_date, now))
        ### FAILED ^^^

    def test_actual__reversed__just_pub(self):
        """Expiration ---- Publication - Now"""
        exp_date = self._date(2018, 4, 1)
        pub_date = self._date(2018, 8, 1)
        now = datetime(2018, 8, 1, 1, 0, 0)
        self.assertFalse(self.is_expired_actual(pub_date, exp_date, now))

    def test_actual__reversed__after(self):
        """Expiration ---- Publication ---- Now"""
        exp_date = self._date(2018, 4, 1)
        pub_date = self._date(2018, 8, 1)
        now = self._date(2018, 9, 1)
        self.assertFalse(self.is_expired_actual(pub_date, exp_date, now))



    def test_annual__cross_year__before(self):
        """Now ---- Publication ---- Expiration"""
        now = self._date(2020, 2, 1)
        pub_date = self._date(2018, 8, 1)
        exp_date = self._date(2019, 4, 1)
        self.assertFalse(self.is_expired_annual(pub_date, exp_date, now))

    def test_annual__cross_year__exp(self):
        """Publication ---- Now/Expiration"""
        now = self._date(2020, 4, 1)
        pub_date = self._date(2018, 8, 1)
        exp_date = self._date(2019, 4, 1)
        self.assertTrue(self.is_expired_annual(pub_date, exp_date, now))

    def test_annual__cross_year__in_exp(self):
        """Publication ---- Now ---- Expiration"""
        now = self._date(2020, 6, 1)
        pub_date = self._date(2018, 8, 1)
        exp_date = self._date(2019, 4, 1)
        self.assertTrue(self.is_expired_annual(pub_date, exp_date, now))

    def test_annual__cross_year__pub(self):
        """Now/Publication ---- Expiration"""
        now = self._date(2020, 8, 1)
        pub_date = self._date(2018, 8, 1)
        exp_date = self._date(2019, 4, 1)
        self.assertFalse(self.is_expired_annual(pub_date, exp_date, now))

    def test_annual__cross_year__just_pub(self):
        """Publication - Now ---- Expiration"""
        pub_date = self._date(2018, 8, 1)
        now = datetime(2020, 8, 1, 1, 0, 0)
        exp_date = self._date(2019, 4, 1)
        self.assertFalse(self.is_expired_annual(pub_date, exp_date, now))

    def test_annual__cross_year__after(self):
        """Publication ---- Now ---- Expiration"""
        pub_date = self._date(2018, 8, 1)
        now = self._date(2020, 9, 1)
        exp_date = self._date(2019, 4, 1)
        self.assertFalse(self.is_expired_annual(pub_date, exp_date, now))



    def test_annual__same_year__before(self):
        """Now ---- Publication ---- Expiration"""
        now = self._date(2020, 2, 1)
        pub_date = self._date(2018, 4, 1)
        exp_date = self._date(2018, 8, 1)
        self.assertTrue(self.is_expired_annual(pub_date, exp_date, now))

    def test_annual__same_year__pub(self):
        """Now/Publication ---- Expiration"""
        now = self._date(2020, 4, 1)
        pub_date = self._date(2018, 4, 1)
        exp_date = self._date(2018, 8, 1)
        self.assertFalse(self.is_expired_annual(pub_date, exp_date, now))

    def test_annual__same_year__in(self):
        """Publication ---- Now ---- Expiration"""
        pub_date = self._date(2018, 4, 1)
        now = self._date(2020, 6, 1)
        exp_date = self._date(2018, 8, 1)
        self.assertFalse(self.is_expired_annual(pub_date, exp_date, now))

    def test_annual__same_year__exp(self):
        """Publication ---- Now/Expiration"""
        pub_date = self._date(2018, 4, 1)
        now = self._date(2020, 8, 1)
        exp_date = self._date(2018, 8, 1)
        self.assertTrue(self.is_expired_annual(pub_date, exp_date, now))

    def test_annual__same_year__just_exp(self):
        """Publication ---- Expiration - Now"""
        pub_date = self._date(2018, 4, 1)
        exp_date = self._date(2018, 8, 1)
        now =  datetime(2020, 8, 1, 1, 0, 0)
        self.assertTrue(self.is_expired_annual(pub_date, exp_date, now))

    def test_annual__same_year__after(self):
        """Publication ---- Expiration ---- Now"""
        pub_date = self._date(2018, 4, 1)
        exp_date = self._date(2018, 8, 1)
        now = self._date(2020, 9, 1)
        self.assertTrue(self.is_expired_annual(pub_date, exp_date, now))


if __name__ == '__main__':
    unittest.main()
