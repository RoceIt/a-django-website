"""Test for setup.py pitfalls.

TestCases to make sure I don't stupid errors in setting up the settings
file.

Middleware_positions_ok: check the middleware positions
"""

from django import VERSION
from django.conf import settings
from django.test import TestCase

class MiddlewarePositionsOk(TestCase):
    """Check to position of the middleware in the MIDDLEWARE variable.

    When reading the docs I found out sometimes the places where you are
    allowed to put some middleware are restricted. Encountering one of
    these i'll try to make a test to report a misplacement.

    test_locale_middleware_ok: test for locale.LocaleMiddleware
    """
    def setUp(self):
        middelware = settings.MIDDLEWARE
        mw_name_module = {
            '1_10_local': 'django.middleware.locale.LocaleMiddleware',
            '1_10_common': 'django.middleware.common.CommonMiddleware',
            '1_10_session': 'django.contrib.sessions.'
                            'middleware.SessionMiddleware',
        }
        self.mw_idx = {}
        for name, module in mw_name_module.items():
            if module in middelware:
                self.mw_idx[name] = middelware.index(module)
            else:
                self.mw_idx[name] = None

    def test_locale_localmiddelware_ok(self):
        """Test the position for the local.LocalMiddelware.

        Included the the checks for placement directives from
          https://docs.djangoproject.com/en/1.10/topics/i18n/translation/
        """
        if VERSION[0] > 100 and VERSION[1] > 100:
            self.assertEqual('that', 'old')
        elif VERSION[0] >= 1 and VERSION[1] >= 5:
            if self.mw_idx['1_10_local']:
                self.assertTrue(
                    self.mw_idx['1_10_local'] < self.mw_idx['1_10_common'])
                self.assertTrue(
                    self.mw_idx['1_10_local'] > self.mw_idx['1_10_session'])
