#!/usr/bin/env python3

import asyncio, os
from modules.protoModule import ProtoModule
from comm.constants import *
from comm.mockMsg_pb2 import MockMsg

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)

FREQUENCY = 10

class MockGuiModule(ProtoModule):
    def __init__(self, loop):
        super().__init__(loop, ADDRESS, PORT,[MsgType.MOCK_MSG])
        self.value = -1
        self.sub_ticks = 0
        self.subbed = True

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        if msg_type == MsgType.MOCK_MSG:
            self.value = msg.mockValue

    def tick(self):
        # this function will get called in a loop with FREQUENCY frequency
        self.loop.call_later(1.0/FREQUENCY, self.tick)

        # for this mock module we will print out the current value
        print('Current value: {}'.format(self.value))

        # to demonstrate subscription and unsubscription,
        # we will periodically unsubscribe and resubscribe
        if self.sub_ticks > 100:
            if self.subbed:
                print('Unsubscribed!')
                self.unsubscribe([MsgType.MOCK_MSG])
            else:
                print('Subscribed!')
                self.subscribe([MsgType.MOCK_MSG])
            self.subbed = not self.subbed
            self.sub_ticks = 0
        self.sub_ticks += 1


def main():
    loop = asyncio.get_event_loop()
    module = MockGuiModule(loop)
    module.run()

if __name__ == "__main__":
    main()
