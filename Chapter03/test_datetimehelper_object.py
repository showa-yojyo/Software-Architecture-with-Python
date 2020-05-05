# Code Listing - #6

""" Module test_datetimehelper_object - Simple test case with test class derived from object """

import datetimehelper

# このスーパークラス (object) は冗長なので書いてはいけないと別の文献で言っている。
class TestDateTimeHelper:

    def test_us_india_conversion(self):
        """ Test us=>india date format conversion """

        obj = datetimehelper.DateTimeHelper()
        assert obj.us_to_indian('1/1/1') == '01/01/2001'
