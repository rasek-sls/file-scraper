"""Metadata scraper for image file formats."""
from file_scraper.pil_base import Pil
from file_scraper.utils import metadata


class TiffPil(Pil):
    """Collect TIFF image metadata."""

    _supported = {'image/tiff': ['6.0']}  # Supported mimetype
    _allow_versions = True                # Allow any version

    @metadata()
    def _width(self):
        """We will get width from another scraper."""
        return None

    @metadata()
    def _height(self):
        """We will get height from another scraper."""
        return None

    @metadata()
    def _colorspace(self):
        """We will get colorspace from another scraper."""
        return None

    @metadata()
    def _samples_per_pixel(self):
        """Return samples per pixel."""
        if self._pil is None:
            return None
        tag_info = self._pil.tag_v2
        if tag_info and 277 in tag_info.keys():
            return str(tag_info[277])
        return super(TiffPil, self)._samples_per_pixel()


class ImagePil(Pil):
    """Collect image image metadata."""

    # Supported mimetypes
    _supported = {'image/png': ['1.2'],
                  'image/jp2': [''],
                  'image/gif': ['1987a', '1989a']}
    _allow_versions = True  # Allow any version

    @metadata()
    def _width(self):
        """Return None: we will get width from another scraper."""
        return None

    @metadata()
    def _height(self):
        """Return None: we will get height from another scraper."""
        return None

    @metadata()
    def _colorspace(self):
        """Return None: we will get colorspace from another scraper."""
        return None


class JpegPil(Pil):
    """Collect JPEG image metadata."""

    _supported = {'image/jpeg': ['1.00', '1.01', '1.02', '2.0', '2.1',
                                 '2.2', '2.2.1']}  # Supported mimetypes
    _allow_versions = True  # Allow any version

    @metadata()
    def _width(self):
        """Return none: we will get width from another scraper."""
        return None

    @metadata()
    def _height(self):
        """Return None: We will get height from another scraper."""
        return None

    @metadata()
    def _colorspace(self):
        """Return None: We will get colorspace from another scraper."""
        return None

    @metadata()
    def _samples_per_pixel(self):
        """Return samples per pixel."""
        if self._pil is None:
            return None
        exif_info = self._pil._getexif()  # pylint: disable=protected-access
        if exif_info and 277 in exif_info.keys():
            return str(exif_info[277])
        return super(JpegPil, self)._samples_per_pixel()
