# Code Listing - #8
# unittest.mock.Mock などを活用する。

"""
Module test_textsearch - Unittest case with mocks for textsearch module
"""

from unittest.mock import Mock, MagicMock
import textsearcher
import operator


def test_search():
    """ Test search via a mock """

    # Mock the database object
    db = Mock()
    searcher = textsearcher.TextSearcher(db)
    # Verify connect has been called with no arguments
    # コードの意味：db.connect() が実行されたことを assert する。
    db.connect.assert_called_with()
    # Setup searcher
    searcher.setup(cache=True, max_items=100)
    # Verify configure called on db with correct parameter
    # コードの意味：db.configure() が実行されて、
    # かつ、呼び出し時に max_items=100 が実引数として渡されたことを assert する。
    searcher.db.configure.assert_called_with(max_items=100)

    canned_results = [('Python is wonderful', 0.4),
                      ('I like Python', 0.8),
                      ('Python is easy', 0.5),
                      ('Python can be learnt in an afternoon!', 0.3)]

    # 意味：db.query() 実行時に返り値が canned_results であるように仕向ける。
    db.query = MagicMock(return_value=canned_results)

    # Mock the results data
    keyword, num = 'python', 3
    data = searcher.get_results(keyword, num=num)

    # 意味： searcher.db.query() が実引数 keyword を伴って実行されたことを assert する。
    searcher.db.query.assert_called_with(keyword)

    # Verify data
    results = sorted(
        canned_results, key=operator.itemgetter(1), reverse=True)[:num]
    assert data == results
