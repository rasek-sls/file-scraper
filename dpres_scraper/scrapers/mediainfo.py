"""Metadata scraper for AV files"""
from dpres_scraper.mediainfo_base import Mediainfo


class VideoMediainfo(Mediainfo):
    """Scraper for various video formats
    """

    _supported = {'video/quicktime': [], 'video/x-ms-asf': [],
                  'video/avi': []}

    def _s_mimetype(self):
        """Return mimetype
        """
        mime_dict = {'DV': 'video/dv',
                     'PCM': 'audio/x-wav',
                     'AIFF': 'audio/x-aiff',
                     'AIFC': 'audio/x-aiff',
                     'AAC': 'audio/mp4',
                     'AVC': 'video/mp4',
                     'MPEG Video': 'video/mpeg',
                     'MPEG Audio': 'audio/mpeg',
                     'FLAC': 'audio/flac',
                     'WMA': 'audio/x-ms-wma',
                     'WMV': 'audio/x-ms-wmv',
                     'FFV1': 'video/x-ffv'}
        if self._s_codec_name() in mime_dict:
            return mime_dict[self._s_codec_name()]
        else:
            return self.mimetype


class DataMediainfo(Mediainfo):
    """Find out, if unknown format is audio/video.
    """
    _supported = {'application/octet-stream': []}

    def _s_mimetype(self):
        """Return mimetype
        """
        mime_dict = {'DV': 'video/dv',
                     'PCM': 'audio/x-wav',
                     'QuickTime': 'video/quicktime'}
        if self._s_codec_name() in mime_dict:
            return mime_dict[self._s_codec_name()]
        else:
            return self.mimetype


class MpegMediainfo(Mediainfo):
    """Scraper class for collecting MPEG video metadata
    """

    _supported = {'video/mpeg': [], 'video/mp4': [],
                  'audio/mpeg': [], 'audio/mp4': []}

    # pylint: disable=no-self-use
    def _s_signal_format(self):
        """Returns signal format
        """
        if self._s_stream_type() not in [None, 'video']:
            return None
        return '(:unap)'

    def _s_codec_quality(self):
        """Returns codec quality
        """
        if self._s_stream_type() not in [None, 'video', 'audio']:
            return None
        if self._mediainfo_stream.compression_mode is not None:
            return self._mediainfo_stream.compression_mode.lower()
        return 'lossy'

    def _s_data_rate_mode(self):
        """Returns data rate mode. Must be resolved
        """
        if self._s_stream_type() not in ['video', 'audio']:
            return None
        if self._mediainfo_stream.bit_rate_mode == 'CBR':
            return 'Fixed'
        return 'Variable'

    def _s_mimetype(self):
        """Returns mimetype for stream
        """
        mime_dict = {'AAC': 'audio/mp4',
                     'AVC': 'video/mp4',
                     'MPEG-4': 'video/mp4',
                     'MPEG Video': 'video/mpeg',
                     'MPEG Audio': 'audio/mpeg'}
        if self._s_codec_name() in mime_dict:
            return mime_dict[self._s_codec_name()]
        else:
            return self.mimetype

    def _s_version(self):
        """Returns stream version
        """
        if self._mediainfo_stream.format_version is not None:
            return self._mediainfo_stream.format_version[-1]
        else:
            return ''