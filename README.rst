File Scraper
============

This software identifies files, collects metadata from them, and does a format well-formed check for a file.

Installation
------------

This software is tested with Python 2.7 with Centos 7.x / RHEL 7.x releases.

Install the required software with commands::

    sudo pip install virtualenv
    virtualenv .venv
    source ./.venv/bin/activate
    pip install -r requirements_dev.txt

This will install virtualenv virtual environment with the following packages, but this is NOT enough for the usage:

    * pytest, coverage, pytest-cov, Fido, file-magic, pymediainfo, ffmpeg-python, Pillow, python-wand, python-lxml, python-mimeparse

The following software is required for minimal usage without file format well-formed check. The bolded software are NOT included in the pip installation script:

    * For all files: opf-fido, file-magic, **file-5.30**
    * Additionally, for image files: Pillow, python-wand, **ImageMagick**
    * Additionally, for audio/video files: pymediainfo, **MediaInfo**

Additionally, the following software is required for complete well-formed check. The bolded software are NOT included in the pip installation script:

    * For text and xml files: python-lxml, python-mimeparse, **JHove**, **v.Nu**, **iso-schematron-xslt1**
    * For WAVE audio files: **JHove**
    * For image files: **JHove**, **dpx-validator**, **pngcheck**
    * For audio/video files (excluding WAVE audio): ffmpeg-python, **FFMpeg**
    * For other files: **JHove**, **LibreOffice**, **veraPDF**, **GhostScript**, **warc-tools >= 4.8.3**, **pspp**

See also:

    * https://github.com/Digital-Preservation-Finland/dpx-validator
    * https://github.com/Digital-Preservation-Finland/iso-schematron-xslt1

Developer Usage
---------------

Use the scraper in the following way::

    from file_scraper.scraper import Scraper
    scraper = Scraper(filename)
    scraper.scrape(check_wellformed=True/False)

The ``check_wellformed`` option is True by default and does full file format well-formed check for the file. To collect metadata without checking the well-formedness of the file, this argument must be ``False``.

As a result the collected metadata and results are in the following instance variables:

    * Path: ``scraper.filename``
    * File format: ``scraper.mimetype``
    * Format version: ``scraper.version``
    * Metadata of the streams: ``scraper.streams``
    * Detector and scraper class names, messages and errors: ``scraper.info``
    * Result of the well-formed check: ``scraper.well_formed``: True: File is well-formed; False: File is not well-formed; None: The file format well-formed check was not done.

The ``scraper.streams`` includes a following kind of dict::

    {0: <stream 0>, 1: <stream 1>, ...}

where ``<stream X>`` contains resulted metadata elements from stream X. In video containers the ``<stream 0>`` contains info about the container.
The following keys exist in all stream metadata::

    {'mimetype': <mimetype>,         # Mimetype of the stream
     'version': <version>,           # Format version of the stream
     'index': <index>,               # Stream index (is a copy of the corresponding key)
     'stream_type': <stream type>,   # Stream type: 'videocontainer', 'video', 'audio', 'image', 'text', 'binary'
     ...}                            # Other metadata keys, different keys in different stream types

The ``scraper.info`` includes a following kind of dict::

    {1: <scraper info 0>, 1: <scraper info 1>, ...}

where ``<scraper info X>`` contains name of the scraper, the resulted info messages and the resulted errors::

    {'class': <scraper name>,
     'messages': <messages from scraper>,
     'errors': <errors from scraper>}

The type of elements in the previous dictionaries is string, in exception of the 'index' elemenent, which is integer.

The following additional arguments for the Scraper are also possible:

    * For CSV file well-formed check:

        * Delimiter between elements: ``delimiter=<element delimiter>``
        * Record separator (line terminator): ``separator=<record separator>``
        * Header field names as list of strings: ``fields=[<field1>, <field2>, ...]``
        * NOTE: If these arguments are not given, the scraper tries to find out the delimiter and separator from the CSV, but may give false results.

    * For XML file well-formed check:

        * Schema: ``schema=<schema file>`` - If not given, the scraper tries to find out the schema from the XML file.
        * Use local schema catalogs: ``catalogs=True/False`` - True by default.
        * Environment for catalogs: ``catalog_path=<catalog path>``  - None by default. If None, then catalog is expected in /etc/xml/catalog
        * Disallow network use: ``no_network=True/False`` - True by default.

    * For XML Schematron well-formed check:

        * Schematron path: ``schematron=<schematron file>`` - If is given, only Schematron check is executed.
        * Verbose: ``verbose=True/False`` - False by default. If False, the e.g. recurring elements are suppressed from the output.
        * Cache: ``cache=True/False`` - True by default. The compiled files are taken from cache, if ``<schematron file>`` is not changed.
        * Hash of related abstract Schematron files: ``extra_hash=<hash>`` - ``None`` by default. The compiled XSLT files created from Schematron are cached,
          but if there exist abstract Schematron patterns in separate files, the hash of those files must be calculated and given
          to make sure that the cache is updated properly. If ``None`` then it is assumed that abstract patterns do not exists or those are up to date.

Additionally, the following returns a boolean value True, if the file is a text file, and False otherwise::

    scraper.is_textfile()

The following returns a checksum of the file with given algorithm (MD5 or SHA variant). The default algorithm is MD5::

    scraper.checksum(algorithm=<algorithm>)

Contributing
------------

All contribution is welcome. Please see `Technical Notes <./doc/contribute.rst>`_ for more technical information about file-scraper.


Misc notes
----------

    * Without the Warctools scraper tool, gzipped WARC and ARC files are identified as 'application/gzip'.
    * For image files with multiple images inside (i.e. TIFF and GIF), the mimetype and version key is filled only in the first image stream, where as these are ``None`` in the other streams.

Copyright
---------
Copyright (C) 2019 CSC - IT Center for Science Ltd.

This program is free software: you can redistribute it and/or modify it under the terms
of the GNU Lesser General Public License as published by the Free Software Foundation, either
version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>.
