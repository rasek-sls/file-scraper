"""Module for pngcheck scraper."""

from file_scraper.base import BaseScraper, Shell
from file_scraper.utils import metadata, ensure_str


class Pngcheck(BaseScraper):
    """
    Pngcheck scraper.

    .. seealso:: http://www.libpng.org/pub/png/apps/pngcheck.html
    """

    _supported = {'image/png': ['1.2']}  # Supported mimetype
    _only_wellformed = True              # Only well-formed check
    _allow_versions = True               # Allow any version

    def scrape_file(self):
        """Scrape file."""
        if not self._check_wellformed and self._only_wellformed:
            self.messages('Skipping scraper: Well-formed check not used.')
            self._collect_elements()
            return
        shell = Shell(['pngcheck', self.filename])

        if shell.returncode != 0:
            self.errors("Failed: returncode %s" % shell.returncode)
            self.errors(ensure_str(shell.stderr))

        self.messages(ensure_str(shell.stdout))
        self._check_supported()
        self._collect_elements()

    @metadata()
    def _stream_type(self):
        """Return file type."""
        return 'image'
