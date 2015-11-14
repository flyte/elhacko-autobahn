import json
from os import environ

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):

    def on_media_message(self, media_meta):
        # TODO: loggly?
        # check uuid and send rest to subscriber
        try:
            media_meta = json.loads(media_meta)
        except TypeError:
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
