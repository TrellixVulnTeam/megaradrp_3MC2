
import datetime

from numinadb.event import manage, on_event

from .model import MegaraFrame


@on_event('on_ingest_raw_fits')
def function(session, some, meta):
    newframe = MegaraFrame()
    newframe.name = meta['path']
    newframe.uuid = meta['uuid']
    newframe.start_time = meta['observation_date']
    newframe.ob_id = meta['blckuuid']
    # No way of knowing when the readout ends...
    newframe.completion_time = newframe.start_time + datetime.timedelta(seconds=meta['darktime'])
    newframe.exposure_time = meta['exptime']
    newframe.object = meta['object']
    newframe.insmode = meta.get('insmode', 'unknown')
    newframe.vph = meta.get('vph', 'unknown')
    # ob.frames.append(newframe)
    # ob.object = meta['object']
    session.add(newframe)


# manage('on_ingest_raw_fits', function)
