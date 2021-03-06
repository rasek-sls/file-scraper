"""FFMpeg wellformed scraper."""
from file_scraper.base import BaseScraper, Shell
from file_scraper.utils import metadata, ensure_str


class FFMpegWellformed(BaseScraper):
    """FFMpeg Wellformed scraper."""

    # Supported mimetypes
    _supported = {'video/mpeg': ['1', '2'], 'video/mp4': [''],
                  'audio/mpeg': ['1', '2'], 'audio/mp4': [''],
                  'video/MP1S': [''], 'video/MP2P': [''],
                  'video/MP2T': [''], 'video/x-matroska': [''],
                  'video/quicktime': [''], 'video/dv': ['']}
    _only_wellformed = True  # Only well-formed check
    _allow_versions = True   # Allow any version

    def scrape_file(self):
        """Scrape A/V files."""
        if not self._check_wellformed and self._only_wellformed:
            self.messages('Skipping scraper: Well-formed check not used.')
            self._collect_elements()
            return
        shell = Shell(['ffmpeg', '-v', 'error', '-i', self.filename, '-f',
                       'null', '-'])

        if shell.returncode == 0:
            self.messages('The file was analyzed successfully.')

        self.errors(ensure_str(shell.stderr))
        self.messages(ensure_str(shell.stdout))
        self._check_supported()
        self._collect_elements()

    @metadata()
    def _version(self):
        """Return version."""
        return None

    @metadata()
    def _stream_type(self):
        """Return file type."""
        return None
