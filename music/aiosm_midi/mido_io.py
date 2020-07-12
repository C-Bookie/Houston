
import mido

class MidoIO:
    def __init__(self, inport_names, outport_names):
        self.inports = [mido.open_input(inport_name) for inport_name in inport_names]
        self.outports = [mido.open_output(outport_name) for outport_name in outport_names]

    def midi_hex(self, hex):
        msg = mido.Message.from_hex(hex)
        for outport in self.outports:
            outport.send(msg)

    def close(self):
        for outport in self.outports:
            outport.close()
        for inport in self.inports:
            inport.close()
