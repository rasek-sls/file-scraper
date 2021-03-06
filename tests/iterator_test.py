"""
Test for file_scraper.scrapers.

This module tests that:
    - iter_scrapers(mimetype, version) returns the correct scrapers.
    - iter_detectors() returns the correct detectors.
"""

import pytest

from file_scraper.iterator import iter_scrapers, iter_detectors


@pytest.mark.parametrize(
    ["mimetype", "version", "scraper_classes"],
    [
        ("application/x-spss-por", None, ["Pspp"]),
        ("application/warc", None, ["WarcWarctools"]),
        ("text/csv", None, ["Csv", "TextFileMagic"]),
        ("text/plain", None, ["TextFileMagic"]),
        ("video/mpeg", None, ["MpegMediainfo", "FFMpegWellformed"]),
        ("video/mp4", None, ["MpegMediainfo", "FFMpegWellformed"]),
        ("video/MP2T", None, ["MpegMediainfo", "FFMpegWellformed"]),
        ("video/x-matroska", None, ["MkvMediainfo", "FFMpegWellformed"]),
        ("video/dv", None, ["MovMediainfo", "FFMpegWellformed"]),
        ("video/quicktime", None, ["MovMediainfo", "FFMpegWellformed"]),
        ("application/pdf", "1.2", ["PdfFileMagic", "PdfJHove"]),
        ("application/pdf", "1.3", ["PdfFileMagic", "PdfJHove"]),
        ("application/pdf", "1.4", ["PdfFileMagic", "PdfJHove"]),
        ("application/pdf", "1.5", ["PdfFileMagic", "PdfJHove"]),
        ("application/pdf", "1.6", ["PdfFileMagic", "PdfJHove"]),
        ("application/pdf", "A-1a", ["PdfFileMagic", "PdfJHove", "VeraPdf"]),
        ("application/pdf", "A-1b", ["PdfFileMagic", "PdfJHove", "VeraPdf"]),
        ("application/pdf", "A-2a",
         ["PdfFileMagic", "GhostScript", "VeraPdf"]),
        ("application/pdf", "A-2b",
         ["PdfFileMagic", "GhostScript", "VeraPdf"]),
        ("application/pdf", "A-2u",
         ["PdfFileMagic", "GhostScript", "VeraPdf"]),
        ("application/pdf", "A-3a",
         ["PdfFileMagic", "GhostScript", "VeraPdf"]),
        ("application/pdf", "A-3b",
         ["PdfFileMagic", "GhostScript", "VeraPdf"]),
        ("application/pdf", "A-3u",
         ["PdfFileMagic", "GhostScript", "VeraPdf"]),
        ("application/pdf", "1.7", ["PdfFileMagic", "GhostScript"]),
        ("image/tiff", None,
         ["TiffJHove", "TiffFileMagic", "TiffPil", "TiffWand"]),
        ("image/jpeg", None,
         ["JpegJHove", "JpegFileMagic", "JpegPil", "ImageWand"]),
        ("image/gif", None, ["GifJHove", "ImagePil", "ImageWand"]),
        ("text/html", "4.01", ["HtmlJHove", "HtmlFileMagic"]),
        ("text/html", "5.0", ["Vnu", "XmlEncoding", "HtmlFileMagic"]),
        ("image/png", None,
         ["Pngcheck", "PngFileMagic", "ImagePil", "ImageWand"]),
        ("application/warc", None, ["WarcWarctools"]),
        ("application/x-internet-archive", None,
         ["ArcFileMagic", "ArcWarctools"]),
        ("text/xml", "1.0", ["Xmllint", "XmlEncoding", "XmlFileMagic"]),
        ("application/xhtml+xml", "1.0", ["HtmlJHove", "XhtmlFileMagic"]),
        ("audio/x-wav", None, ["WavJHove", "WavMediainfo"]),
        ("application/vnd.oasis.opendocument.text", None,
         ["Office", "OfficeFileMagic"]),
        ("application/vnd.oasis.opendocument.spreadsheet", None,
         ["Office", "OfficeFileMagic"]),
        ("application/vnd.oasis.opendocument.presentation", None,
         ["Office", "OfficeFileMagic"]),
        ("application/vnd.oasis.opendocument.graphics", None,
         ["Office", "OfficeFileMagic"]),
        ("application/vnd.oasis.opendocument.formula", None,
         ["Office", "OfficeFileMagic"]),
        ("application/msword", None, ["Office", "OfficeFileMagic"]),
        ("application/vnd.ms-excel", None, ["Office", "OfficeFileMagic"]),
        ("application/vnd.ms-powerpoint", None, ["Office", "OfficeFileMagic"]),
        ("application/vnd.openxmlformats-officedocument.wordprocessingml."
         "document", None, ["Office", "OfficeFileMagic"]),
        ("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
         None, ["Office", "OfficeFileMagic"]),
        ("application/vnd.openxmlformats-officedocument.presentationml."
         "presentation", None, ["Office", "OfficeFileMagic"]),
        ("test/unknown", None, ["ScraperNotFound"])
    ])
def test_iter_scrapers(mimetype, version, scraper_classes):
    """Test scraper discovery."""
    scrapers = iter_scrapers(mimetype, version)
    assert set([x.__name__ for x in scrapers]) == set(scraper_classes)


def test_iter_detectors():
    """Test detector discovery."""
    detectors = iter_detectors()
    assert set([x.__name__ for x in detectors]) == set(["FidoDetector",
                                                        "MagicDetector"])
