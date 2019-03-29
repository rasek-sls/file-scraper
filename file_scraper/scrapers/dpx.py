"""DPX V2.0 scraper."""
from file_scraper.base import BaseScraper, Shell
from file_scraper.utils import metadata


class Dpx(BaseScraper):
    """DPX scraper."""

    _supported = {'image/x-dpx': ['2.0']}  # Supported mimetype and version
    _only_wellformed = True                # Only well-formed check

    def scrape_file(self):
        """Scrape DPX."""
        if not self._check_wellformed and self._only_wellformed:
            self.messages('Skipping scraper: Well-formed check not used.')
            self._collect_elements()
            return
        shell = Shell(['dpxv', self.filename])

        if shell.returncode != 0:
            raise DPXvError(shell.stderr)

        self.errors(shell.stderr)
        self.messages(shell.stdout)
        self._check_supported()
        self._collect_elements()

    @metadata()
    def _version(self):
        """Return version."""
        return '2.0'

    @metadata()
    def _stream_type(self):
        """Return file type."""
        return 'image'


class DPXvError(Exception):
    """DPX scraper error."""
    pass
