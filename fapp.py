import json
import traceback
from os import environ

import requests
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner

LOGGLY_URL = 'http://logs-01.loggly.com/inputs/3e7211c1-708e-4ec2-9144-2d47a5d03a60/tag/http/'


class Component(ApplicationSession):

    def on_media_message(self, media_meta):
        # check uuid and send rest to subscriber
        try:
            media_meta = json.loads(media_meta)
            requests.post(LOGGLY_URL, data=media_meta)
        except TypeError:
            requests.post(LOGGLY_URL, data='Unpacking media_meta failed')
            err = traceback.format_exc()
            requests.post(LOGGLY_URL, data=err)
            pass
        self.publish(u'ws.media.{uuid}'.format(uuid=media_meta.get('uuid')),
                     json.dumps(media_meta))

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")
        # listen for images
        yield self.subscribe(self.on_media_message, u'controller.media')


if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://127.0.0.1:8080/ws"),
        u"elhacko",
        debug_wamp=False,  # optional; log many WAMP details
        debug=False,  # optional; log even more details
    )
    runner.run(Component)
