#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for File (libmagick) scraper.

This module tests that:
    - For valid files, OfficeFileMagic, PngFileMagic, JpegFileMagic,
      Jp2FileMagic, TiffFileMagic, TextFileMagic, XmlFileMagic, XhtmlFilemagic,
      HtmlFileMagic, PdfFileMagic and ArcFileMagic are able to correctly
      determine the following features of their corresponding file types:
        - MIME type
        - version
        - streams
        - well-formedness
    - In addition to this, the scraper messages contain 'successfully' and no
      errors are recorded.

    - For empty files, all these scrapers report MIME type as inode/x-empty.

    - For office files (odt, doc, docx, odp, ppt, pptx, ods, xls, xlsx, odg and
      odf) with missing bytes:
        - MIME type is application/octet-stream
        - version is None
        - streams are scraped correctly
        - scraper errors contain 'do not match'
        - file is not well-formed
    - For XHTML files with missing closing tag:
        - MIME type, version and streams are scraped correctly
        - there are no scraper errors
        - scraper messages contain 'successfully'
        - file is well-formed
    - For HTML files without doctype the same things are checked as with XHTML
      files but version must be None
    - For pdf and arc files the same things are checked as with XHTML files

    - For image files (png, jpeg, jp2, tif) with errors:
        - MIME type is application/octet-stream
        - version and streams are scraped correctly
        - scraper errors contain 'do not match'
        - file is not well-formed

    - For text files actually containing binary data:
        - version is None
        - MIME type is application/octet-stream
        - scraper errors contains 'do not match'
        - file is not well-formed

    - Running scraper without full scraping results in well_formed being None
      and scraper messages containing 'Skipping scraper'

    - The following MIME type and version pairs are supported when full
      scraping is performed:
        - application/vnd.oasis.opendocument.text, 1.1
        - application/msword, 11.0
        - application/vnd.openxmlformats-officedocument.wordprocessingml.document, 15.0
        - application/vnd.oasis.opendocument.presentation, 1.1
        - application/vnd.ms-powerpoint, 11.0
        - application/vnd.openxmlformats-officedocument.presentationml.presentation, 15.0
        - application/vnd.oasis.opendocument.spreadsheet, 1.1
        - application/vnd.ms-excel, 8.0
        - application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,
          15.0
        - application/vnd.oasis.opendocument.graphics, 1.1
        - application/vnd.oasis.opendocument.formula, 1.0
        - image/png, 1.2
        - image/jpeg, 1.01
        - image/jp2, ''
        - image/tiff, 6.0
        - text/plain, ''
        - text/xml, 1.0
        - application/xhtml+xml, 1.0
        - text/html, 4.01
        - application/pdf, 1.4
        - application/x-internet-archive, 1.0
    - Any of these MIME types with version None is also supported,
      except text/html
    - Valid MIME type with made up version is supported, except
      text/html
    - Made up MIME type with any version is not supported
    - When full scraping is not done, none of these combinations are supported.
"""
import pytest
from file_scraper.scrapers.magic import (OfficeFileMagic, TextFileMagic,
                                         XmlFileMagic, HtmlFileMagic,
                                         PngFileMagic, JpegFileMagic,
                                         TiffFileMagic, Jp2FileMagic,
                                         XhtmlFileMagic, PdfFileMagic,
                                         ArcFileMagic)
from tests.common import parse_results


@pytest.mark.parametrize(
    ['filename', 'mimetype', 'class_'],
    [
        ("valid_1.1.odt",
         "application/vnd.oasis.opendocument.text", OfficeFileMagic),
        ("valid_11.0.doc",
         "application/msword", OfficeFileMagic),
        ("valid_15.0.docx",
         "application/vnd.openxmlformats-"
         "officedocument.wordprocessingml.document", OfficeFileMagic),
        ("valid_1.1.odp",
         "application/vnd.oasis.opendocument.presentation", OfficeFileMagic),
        ("valid_11.0.ppt",
         "application/vnd.ms-powerpoint", OfficeFileMagic),
        ("valid_15.0.pptx",
         "application/vnd.openxml"
         "formats-officedocument.presentationml.presentation",
         OfficeFileMagic),
        ("valid_1.1.ods",
         "application/vnd.oasis.opendocument.spreadsheet", OfficeFileMagic),
        ("valid_11.0.xls",
         "application/vnd.ms-excel", OfficeFileMagic),
        ("valid_15.0.xlsx",
         "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
         OfficeFileMagic),
        ("valid_1.1.odg",
         "application/vnd.oasis.opendocument.graphics", OfficeFileMagic),
        ("valid_1.0.odf",
         "application/vnd.oasis.opendocument.formula", OfficeFileMagic),
        ("valid_1.2.png", "image/png", PngFileMagic),
        ("valid_1.01.jpg", "image/jpeg", JpegFileMagic),
        ("valid.jp2", "image/jp2", Jp2FileMagic),
        ("valid_6.0.tif", "image/tiff", TiffFileMagic),
        ("valid__iso8859.txt", "text/plain", TextFileMagic),
        ("valid__utf8.txt", "text/plain", TextFileMagic),
        ("valid_1.0_well_formed.xml", "text/xml", XmlFileMagic),
        ("valid_1.0.xhtml", "application/xhtml+xml", XhtmlFileMagic),
        ("valid_4.01.html", "text/html", HtmlFileMagic),
        ("valid_5.0.html", "text/html", HtmlFileMagic),
        ("valid_1.4.pdf", "application/pdf", PdfFileMagic),
        ("valid_1.0.arc", "application/x-internet-archive", ArcFileMagic),
    ])
def test_scraper_valid(filename, mimetype, class_, evaluate_scraper):
    """Test scraper."""
    result_dict = {
        'purpose': 'Test valid file.',
        'stdout_part': 'successfully',
        'stderr_part': ''}
    correct = parse_results(filename, mimetype,
                            result_dict, True)
    scraper = class_(correct.filename, correct.mimetype,
                     True, correct.params)
    scraper.scrape_file()

    if class_ in [XhtmlFileMagic]:
        correct.streams[0]['stream_type'] = 'text'
    if class_ in [OfficeFileMagic, HtmlFileMagic]:
        correct.version = None
        correct.streams[0]['version'] = None
    if class_ in [TextFileMagic, HtmlFileMagic, XmlFileMagic, XhtmlFileMagic]:
        correct.streams[0]['charset'] = 'UTF-8'
    if filename == 'valid__iso8859.txt':
        correct.streams[0]['charset'] = 'ISO-8859-15'

    evaluate_scraper(scraper, correct)


@pytest.mark.parametrize(
    ['filename', 'mimetype'],
    [
        ("invalid_1.1_missing_data.odt",
         "application/vnd.oasis.opendocument.text"),
        ("invalid_11.0_missing_data.doc", "application/msword"),
        ("invalid_15.0_missing_data.docx",
         "application/vnd.openxmlformats-"
         "officedocument.wordprocessingml.document"),
        ("invalid_1.1_missing_data.odp",
         "application/vnd.oasis.opendocument.presentation"),
        ("invalid_11.0_missing_data.ppt", "application/vnd.ms-powerpoint"),
        ("invalid_15.0_missing_data.pptx", "application/vnd.openxml"
                                           "formats-officedocument.presentationml.presentation"),
        ("invalid_1.1_missing_data.ods",
         "application/vnd.oasis.opendocument.spreadsheet"),
        ("invalid_11.0_missing_data.xls", "application/vnd.ms-excel"),
        ("invalid_15.0_missing_data.xlsx",
         "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
        ("invalid_1.1_missing_data.odg",
         "application/vnd.oasis.opendocument.graphics"),
        ("invalid_1.0_missing_data.odf",
         "application/vnd.oasis.opendocument.formula"),
        ("invalid__empty.doc", "application/msword"),
    ])
def test_invalid_office(filename, mimetype, evaluate_scraper):
    """Test OfficeFileMagic scraper with invalid files."""
    result_dict = {
        'purpose': 'Test invalid file.',
        'stdout_part': '',
        'stderr_part': 'do not match'}
    correct = parse_results(filename, mimetype,
                            result_dict, True)
    scraper = OfficeFileMagic(correct.filename, correct.mimetype, True,
                              correct.params)
    scraper.scrape_file()

    if 'empty' in filename:
        correct.streams[0]['mimetype'] = 'inode/x-empty'
        correct.mimetype = 'inode/x-empty'
    else:
        correct.streams[0]['mimetype'] = 'application/octet-stream'
        correct.mimetype = 'application/octet-stream'

    correct.version = None
    correct.streams[0]['version'] = None

    evaluate_scraper(scraper, correct)


@pytest.mark.parametrize(
    ['filename', 'mimetype', 'class_'],
    [
        ("invalid_1.0_no_closing_tag.xml", "text/xml", XmlFileMagic),
        ("invalid_1.0_no_doctype.xhtml", "application/xhtml+xml",
         XhtmlFileMagic),
        ("invalid_4.01_nodoctype.html", "text/html", HtmlFileMagic),
        ("invalid_5.0_nodoctype.html", "text/html", HtmlFileMagic),
        ("invalid_1.4_removed_xref.pdf", "application/pdf", PdfFileMagic),
        ("invalid_1.0_missing_field.arc", "application/x-internet-archive",
         ArcFileMagic),
    ])
def test_invalid_markdown_pdf_arc(filename, mimetype, class_,
                                  evaluate_scraper):
    """Test scrapers for invalid XML, XHTML, HTML, pdf and arc files."""
    result_dict = {
        'purpose': 'Test invalid file.',
        'stdout_part': 'successfully',
        'stderr_part': ''}
    correct = parse_results(filename, mimetype, result_dict, True)
    scraper = class_(correct.filename, correct.mimetype, True, correct.params)
    scraper.scrape_file()

    correct.well_formed = True

    if 'empty' in filename:
        correct.streams[0]['mimetype'] = 'inode/x-empty'

    if class_ == HtmlFileMagic:
        correct.version = None
        correct.streams[0]['version'] = None
    if class_ in [XhtmlFileMagic]:
        correct.streams[0]['stream_type'] = 'text'
    if class_ in [HtmlFileMagic, XmlFileMagic, XhtmlFileMagic]:
        correct.streams[0]['charset'] = 'UTF-8'

    evaluate_scraper(scraper, correct)


@pytest.mark.parametrize(
    ['filename', 'mimetype', 'class_'],
    [
        ("invalid_1.2_wrong_header.png", "image/png", PngFileMagic),
        ("invalid_1.01_no_start_marker.jpg", "image/jpeg", JpegFileMagic),
        ("invalid__data_missing.jp2", "image/jp2", Jp2FileMagic),
        ("invalid_6.0_wrong_byte_order.tif", "image/tiff", TiffFileMagic),
    ])
def test_invalid_images(filename, mimetype, class_, evaluate_scraper):
    """Test scrapes for invalid image files."""
    result_dict = {
        'purpose': 'Test invalid file.',
        'stdout_part': '',
        'stderr_part': 'do not match'}
    correct = parse_results(filename, mimetype, result_dict, True)
    scraper = class_(correct.filename, correct.mimetype, True, correct.params)
    scraper.scrape_file()

    if 'empty' in filename:
        correct.streams[0]['mimetype'] = 'inode/x-empty'
        correct.mimetype = 'inode/x-empty'
    else:
        correct.streams[0]['mimetype'] = 'application/octet-stream'
        correct.mimetype = 'application/octet-stream'

    correct.version = None
    correct.streams[0]['version'] = None

    evaluate_scraper(scraper, correct)


@pytest.mark.parametrize(
    ['filename', 'mimetype'],
    [
        ("invalid__binary_data.txt", "text/plain"),
        ("invalid__empty.txt", "text/plain"),
    ])
def test_invalid_text(filename, mimetype, evaluate_scraper):
    """Test TextFileMagic with invalid files."""
    result_dict = {
        'purpose': 'Test invalid file.',
        'stdout_part': '',
        'stderr_part': 'do not match'}
    correct = parse_results(filename, mimetype,
                            result_dict, True)
    scraper = TextFileMagic(correct.filename, correct.mimetype, True,
                            correct.params)
    scraper.scrape_file()

    if 'empty' in filename:
        correct.streams[0]['mimetype'] = 'inode/x-empty'
        correct.mimetype = 'inode/x-empty'
    else:
        correct.streams[0]['mimetype'] = 'application/octet-stream'
        correct.mimetype = 'application/octet-stream'

    correct.version = None
    correct.streams[0]['version'] = None
    correct.streams[0]['charset'] = None

    evaluate_scraper(scraper, correct)


def test_no_wellformed():
    """Test scraper without well-formed check."""
    scraper = JpegFileMagic('tests/data/image_jpeg/valid_1.01.jpg',
                            'image/jpeg', False)
    scraper.scrape_file()
    assert 'Skipping scraper' not in scraper.messages()
    assert scraper.well_formed is None


@pytest.mark.parametrize(
    ['mime', 'ver', 'class_'],
    [
        ('application/vnd.oasis.opendocument.text', '1.1', OfficeFileMagic),
        ('application/msword', '11.0', OfficeFileMagic),
        ('application/vnd.openxmlformats-officedocument.wordprocessingml'
         '.document', '15.0', OfficeFileMagic),
        ('application/vnd.oasis.opendocument.presentation', '1.1',
         OfficeFileMagic),
        ('application/vnd.ms-powerpoint', '11.0', OfficeFileMagic),
        ('application/vnd.openxmlformats-officedocument.presentationml'
         '.presentation', '15.0', OfficeFileMagic),
        ('application/vnd.oasis.opendocument.spreadsheet', '1.1',
         OfficeFileMagic),
        ('application/vnd.ms-excel', '8.0', OfficeFileMagic),
        ('application/vnd.openxmlformats-officedocument.spreadsheetml'
         '.sheet', '15.0', OfficeFileMagic),
        ('application/vnd.oasis.opendocument.graphics', '1.1',
         OfficeFileMagic),
        ('application/vnd.oasis.opendocument.formula', '1.0', OfficeFileMagic),
        ('image/png', '1.2', PngFileMagic),
        ('image/jpeg', '1.01', JpegFileMagic),
        ('image/jp2', '', Jp2FileMagic),
        ('image/tiff', '6.0', TiffFileMagic),
        ('text/plain', '', TextFileMagic),
        ('text/xml', '1.0', XmlFileMagic),
        ('application/xhtml+xml', '1.0', XhtmlFileMagic),
        ('application/pdf', '1.4', PdfFileMagic),
        ('application/x-internet-archive', '1.0', ArcFileMagic),
    ]
)
def test_is_supported_allow(mime, ver, class_):
    """Test is_supported method."""
    assert class_.is_supported(mime, ver, True)
    assert class_.is_supported(mime, None, True)
    assert class_.is_supported(mime, ver, False)
    assert class_.is_supported(mime, 'foo', True)
    assert not class_.is_supported('foo', ver, True)


@pytest.mark.parametrize(
    ['mime', 'ver', 'class_'],
    [
        ('text/html', '4.01', HtmlFileMagic),
    ]
)
def test_is_supported_deny(mime, ver, class_):
    """Test is_supported method."""
    assert class_.is_supported(mime, ver, True)
    assert not class_.is_supported(mime, None, True)
    assert class_.is_supported(mime, ver, False)
    assert not class_.is_supported(mime, 'foo', True)
    assert not class_.is_supported('foo', ver, True)
