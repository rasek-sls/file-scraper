"""
Test CheckTextFile, which determines whether file is a text file or not.

This module tests that:
    - Following files are correctly identified as text files and their MIME
      type, version, streams and well-formedness are determined correctly:
        - plain text with either UTF-8 or Latin-1 encoding
        - xml document
        - html document
    - Empty file, pdf and gif files are identified as not text files.
"""
import pytest

from file_scraper.scrapers.textfile import CheckTextFile
from tests.common import parse_results

VALID_MSG = 'is a text file'
INVALID_MSG = 'is not a text file'


@pytest.mark.parametrize(
    ["filename", "mimetype", "is_textfile"],
    [
        ("valid__utf8.txt", "text/plain", True),
        ("valid__iso8859.txt", "text/plain", True),
        ("valid_1.0_well_formed.xml", "text/xml", True),
        ("valid_4.01.html", "text/html", True),
        ("invalid_4.01_illegal_tags.html", "text/html", True),
        ("valid_1.4.pdf", "application/pdf", False),
        ("valid_1987a.gif", "image/gif", False),
        ("invalid_1987a_broken_header.gif", "image/gif", False),
        ("invalid__empty.txt", "text/plain", False)
    ]
)
def test_existing_files(filename, mimetype, is_textfile, evaluate_scraper):
    """Test detecting whether file is a textfile."""
    correct = parse_results(filename, mimetype,
                            {}, True)
    scraper = CheckTextFile(correct.filename, correct.mimetype, True)
    scraper.scrape_file()

    correct.version = None
    correct.streams[0]['version'] = None
    correct.streams[0]['stream_type'] = None
    correct.well_formed = is_textfile
    if correct.well_formed:
        correct.stdout_part = VALID_MSG
        correct.stderr_part = ''
    else:
        correct.stdout_part = ''
        correct.stderr_part = INVALID_MSG

    evaluate_scraper(scraper, correct)