"""Stream dicts"""

MOV_CONTAINER = {
    'codec_creator_app': 'Lavf56.40.101',
    'codec_creator_app_version': '56.40.101',
    'codec_name': 'MPEG-4', 'index': 0, 'mimetype': 'video/quicktime',
    'stream_type': 'videocontainer', 'version': ''}

DV_VIDEO = {
    'bits_per_sample': '8', 'codec_creator_app': '(:unav)',
    'codec_creator_app_version': '(:unav)', 'codec_name': 'DV',
    'codec_quality': 'lossy', 'color': 'Color', 'dar': '1.778',
    'data_rate': '24.4416', 'data_rate_mode': 'Fixed', 'duration': 'PT0.08S',
    'frame_rate': '25', 'height': '576', 'index': 0, 'mimetype': 'video/dv',
    'par': '1.422', 'sampling': '4:2:0', 'signal_format': 'PAL',
    'sound': 'No', 'stream_type': 'video', 'version': '', 'width': '720'}

MOV_DV_VIDEO = dict(DV_VIDEO, **{
    'codec_creator_app': 'Lavf56.40.101',
    'codec_creator_app_version': '56.40.101', 'sound': 'Yes'})

MOV_TC = {
    'index': 3, 'mimetype': 'video/quicktime', 'stream_type': 'other',
    'version': None}


MKV_CONTAINER = {
    'codec_creator_app': 'Lavf56.40.101',
    'codec_creator_app_version': '56.40.101',
    'codec_name': 'Matroska', 'index': 0,
    'mimetype': 'video/x-matroska',
    'stream_type': 'videocontainer', 'version': '4'}

FFV_VIDEO = {
    'bits_per_sample': '8', 'codec_creator_app': 'Lavf56.40.101',
    'codec_creator_app_version': '56.40.101',
    'codec_name': 'FFV1', 'codec_quality': 'lossless',
    'color': 'Color', 'dar': '1.778', 'data_rate': '2.071061',
    'data_rate_mode': 'Variable', 'duration': 'PT1S',
    'frame_rate': '30', 'height': '180', 'index': 1,
    'mimetype': 'video/x-ffv', 'par': '1', 'sampling': '4:2:0',
    'signal_format': '(:unap)', 'sound': 'No', 'stream_type': 'video',
    'version': '3', 'width': '320'}
FFV_VIDEO_TRUNCATED = dict(FFV_VIDEO, **{
    'data_rate': '2.077741', 'version': '0'})

WAV_AUDIO = {
    'audio_data_encoding': 'PCM', 'bits_per_sample': '8',
    'codec_creator_app': 'Lavf56.40.101',
    'codec_creator_app_version': '56.40.101',
    'codec_name': 'PCM', 'codec_quality': 'lossless',
    'data_rate': '705.6', 'data_rate_mode': 'Fixed', 'duration': 'PT0.86S',
    'index': 0, 'mimetype': 'audio/x-wav', 'num_channels': '2',
    'sampling_frequency': '44.1', 'stream_type': 'audio', 'version': ''}

MPEG1_VIDEO = {
    'mimetype': 'video/mpeg', 'index': 0, 'par': '1', 'frame_rate': '30',
    'data_rate': '0.171304', 'bits_per_sample': '8',
    'data_rate_mode': 'Variable', 'color': 'Color',
    'codec_quality': 'lossy', 'signal_format': '(:unap)', 'dar': '1.778',
    'height': '180', 'sound': 'No', 'version': '1',
    'codec_name': 'MPEG Video',
    'codec_creator_app_version': '(:unav)',
    'duration': 'PT1S', 'sampling': '4:2:0', 'stream_type': 'video',
    'width': '320', 'codec_creator_app': '(:unav)'}

MPEG2_VIDEO = dict(MPEG1_VIDEO, **{
    'data_rate': '0.185784', 'version': '2'})

MPEG4_VIDEO = dict(MPEG1_VIDEO, **{
    'mimetype': 'video/mp4', 'index': 1, 'data_rate': '0.048704',
    'sound': 'Yes', 'version': '', 'codec_name': 'AVC',
    'codec_creator_app_version': '56.40.101',
    'codec_creator_app': 'Lavf56.40.101'})

MPEGTS_VIDEO = dict(MPEG1_VIDEO, **{
    'data_rate': '(:unav)', 'index': 1, 'sound': 'Yes', 'version': '2'})

MPEG1_AUDIO = {
    'mimetype': 'audio/mpeg', 'index': 0,
    'audio_data_encoding': 'MPEG Audio', 'bits_per_sample': '(:unav)',
    'data_rate_mode': 'Variable', 'codec_quality': 'lossy', 'version': '1',
    'stream_type': 'audio', 'sampling_frequency': '44.1',
    'num_channels': '2', 'codec_name': 'MPEG Audio',
    'codec_creator_app_version': '(:unav)', 'duration': '(:unav)',
    'data_rate': '(:unav)', 'codec_creator_app': '(:unav)'}

MPEG4_AUDIO = dict(MPEG1_AUDIO, **{
    'mimetype': 'audio/mp4', 'index': 2, 'audio_data_encoding': 'AAC',
    'data_rate_mode': 'Fixed', 'version': '', 'codec_name': 'AAC',
    'codec_creator_app_version': '56.40.101',
    'duration': 'PT0.86S', 'data_rate': '135.233',
    'codec_creator_app': 'Lavf56.40.101'})

MPEGTS_AUDIO = dict(MPEG1_AUDIO, **{
    'data_rate': '128', 'data_rate_mode': 'Fixed', 'duration': 'PT0.89S',
    'index': 2})

MPEG4_CONTAINER = {
    'mimetype': 'video/mp4', 'index': 0, 'stream_type': 'videocontainer',
    'version': '', 'codec_name': 'MPEG-4',
    'codec_creator_app_version': '56.40.101',
    'codec_creator_app': 'Lavf56.40.101'}

MPEGTS_CONTAINER = {
    'codec_creator_app': '(:unav)',
    'codec_creator_app_version': '(:unav)',
    'codec_name': 'MPEG-TS', 'index': 0, 'mimetype': 'video/MP2T',
    'stream_type': 'videocontainer', 'version': ''}

MPEGTS_OTHER = {
    'index': 3, 'mimetype': 'video/MP2T', 'stream_type': 'menu',
    'version': None}
