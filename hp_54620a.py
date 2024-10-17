"""Module providing an interface to the HP 55620A 16 channel logic analyzer"""
from enum import Enum

# pylint: disable=R0904 #too many public methods
class HP54620A():
    """Class to represent the HP 54620A 16 channel logic analyzer"""
    def __init__(self, _gpib, addr):
        self.address = addr
        self.gpib = _gpib
        self.first_time = True
        self._delay = 0.4
        # self.gpib.write("++read_tmo_ms 1200")
        self._pre_command()

    class ChannelGroup(Enum):
        """Enum with the two channel group"""
        CHANNEL0_7  = 0
        CHANNEL8_15 = 1

    class ThresholdType(Enum):
        """Enum with the usable threshold type"""
        CMOS = 0
        ECL  = 1
        TTL  = 2
        USER = 3

    class Grid(Enum):
        """Enum with the usable grid"""
        OFF   = 0
        FRAME = 1
        FULL  = 2

    class Function(Enum):
        """Enum with the usable function"""
        DELAY     = 0
        DUTYCYCLE = 1
        FREQUENCY = 2
        PERIOD    = 3
        HOLD      = 4
        NWIDTH    = 5
        PWIDTH    = 6

    class TimeBaseMode(Enum):
        """Enum with the usable timebase mode"""
        MAIN    = 0
        DELAYED = 1

    class TimeBaseReference(Enum):
        """Enum with the usable timebase reference"""
        LEFT   = 0
        CENTER = 1
        RIGHT  = 2

    class TriggerType(Enum):
        """Enum with the usable trigger type"""
        EDGE     = 0
        PATTERN  = 1
        ADVANCED = 2

    class TriggerEdge(Enum):
        """Enum with the usable trigger edge"""
        RISING      = 0
        FALLING     = 1
        EITHER_EDGE = 2

    class TriggerMode(Enum):
        """Enum with the usable trigger mode"""
        NORMAL = 0
        AUTO   = 1

    class AcquireType(Enum):
        """Enum with the usable trigger edge"""
        AUTO   = 0
        NORMAL = 1
        GLITCH = 2

    def __str__(self):
        return "HP 54620A address: " + str(self.address)

    def _pre_command(self):
        """Command to be executed before every other command"""
        if self.gpib.address != self.address or self.first_time:
            self.first_time = False
            self.gpib.set_address(self.address)
            self.gpib.write("++eor 2")

    def get_idn(self):
        """Return the ID of the instrument"""
        return self.gpib.get_idn()

    def reset(self):
        """Reset the instrument to the default state"""
        self._pre_command()
        self.gpib.write("*RST")

    def set_threshold(self, ch, t_type, value=0):
        """Enable the filter"""
        self._pre_command()
        threshold_type_list = ["CMOS", "ECL", "TTL", "USER"]
        txt_value = ""
        if t_type == self.ThresholdType.USER:
            txt_value = ","+str(value)
        if ch == self.ChannelGroup.CHANNEL0_7:
            self.gpib.write(":LCH:THR LCHAN0_7,"+threshold_type_list[t_type.value]+txt_value)
        elif ch == self.ChannelGroup.CHANNEL8_15:
            self.gpib.write(":LCH:THR LCHAN8_15,"+threshold_type_list[t_type.value]+txt_value)

    def autoscale(self):
        """Autoscale the instrument"""
        self._pre_command()
        self.gpib.write(":AUT")

    def set_grid(self, grid):
        """Set the grid"""
        self._pre_command()
        if grid == self.Grid.OFF:
            self.gpib.write(":DISP:GRID OFF")
        elif grid == self.Grid.FRAME:
            self.gpib.write(":DISP:GRID FRAM")
        elif grid == self.Grid.FULL:
            self.gpib.write(":DISP:GRID FULL")

    #It's doing nothing?
    def set_inverse_display(self, on):
        """Invert the display"""
        self._pre_command()
        if on:
            self.gpib.write(":DISP:INV ON")
        else:
            self.gpib.write(":DISP:INV OFF")

    def display_label(self, on):
        """Display the label"""
        self._pre_command()
        if on:
            self.gpib.write(":DISP:LAB ON")
        else:
            self.gpib.write(":DISP:LAB OFF")

    def set_channel_label(self, ch, _label):
        """Set the channel label"""
        self._pre_command()
        self.gpib.write(f":LCH:LAB LCHAN{ch},\"{_label[:6]}\"")

    #Ancora da provare
    def measure(self, function):
        """Take a measurement"""
        self._pre_command()
        if function == self.Function.DELAY:
            self.gpib.write(":MEAS:DEL?")
        elif function == self.Function.DUTYCYCLE:
            self.gpib.write(":MEAS:DUTY?")
        elif function == self.Function.FREQUENCY:
            self.gpib.write(":MEAS:FREQ?")
        elif function == self.Function.PERIOD:
            self.gpib.write(":MEAS:PER?")
        elif function == self.Function.HOLD:
            self.gpib.write(":MEAS:HOLD?")
        elif function == self.Function.NWIDTH:
            self.gpib.write(":MEAS:NWID?")
        elif function == self.Function.PWIDTH:
            self.gpib.write(":MEAS:PWID?")

        try:
            return float(self.gpib.query("++read", sleep=self._delay).strip())
        except (ValueError, AttributeError):
            return False

    def show_measure(self, on):
        """Show the measurement on the CRT"""
        self._pre_command()
        if on:
            self.gpib.write(":MEAS:SHOW ON")
        else:
            self.gpib.write(":MEAS:SHOW OFF")

    def source_measure(self, ch):
        """Source of the measurement"""
        self._pre_command()
        self.gpib.write(f":MEAS:SOUR LCHAN{ch}")

    def run(self):
        """Set instrument in run mode"""
        self._pre_command()
        self.gpib.write(":RUN")

    def run_single(self):
        """Set instrument in single run mode"""
        self._pre_command()
        self.gpib.write(":RUNS")

    def stop(self):
        """Set instrument in stop mode"""
        self._pre_command()
        self.gpib.write(":STOP")

    # You can use suffix: S, MS, US, NS
    def set_timebase_delay(self, delay):
        """Set the timebase delay"""
        self._pre_command()
        self.gpib.write(f":TIM:DEL {delay}")

    # You can use suffix: S, MS, US, NS
    def set_timebase_range(self, _range):
        """Set the timebase range"""
        self._pre_command()
        self.gpib.write(f":TIM:RANG {_range}")

    def set_timebase_mode(self, mode):
        """Set the timebase mode"""
        self._pre_command()
        if mode == self.TimeBaseMode.MAIN:
            self.gpib.write("TIMebase:MODE NORM")
        elif mode == self.TimeBaseMode.DELAYED:
            self.gpib.write("TIMebase:MODE DEL")

    def set_timebase_reference(self, reference):
        """Set the timebase reference"""
        self._pre_command()
        if reference == self.TimeBaseReference.LEFT:
            self.gpib.write(":TIM:REF LEFT")
        elif reference == self.TimeBaseReference.CENTER:
            self.gpib.write(":TIM:REF CENT")
        elif reference == self.TimeBaseReference.RIGHT:
            self.gpib.write(":TIM:REF RIGH")

    def enable_vernier(self, on):
        """Enable the vernier"""
        self._pre_command()
        if on:
            self.gpib.write(":TIM:VERN ON")
        else:
            self.gpib.write(":TIM:VERN OFF")

    def set_trigger_type(self, trigger):
        """Set the trigger type"""
        self._pre_command()
        if trigger == self.TriggerType.EDGE:
            self.gpib.write(":TRIG:TYPE EDGE")
        elif trigger == self.TriggerType.PATTERN:
            self.gpib.write(":TRIG:TYPE PATTERN")
        elif trigger == self.TriggerType.ADVANCED:
            self.gpib.write(":TRIG:TYPE ADVANCED")

    def set_trigger_edge(self, ch, edge):
        """Set the thrigger edge of a channel"""
        self._pre_command()
        edge_list = ["RIS", "FALL", "EITH"]
        self.gpib.write(f":TRIG:EDGE LCHAN{ch},{edge_list[edge.value]}")

    def set_trigger_mode(self, mode):
        """Set the trigger type"""
        self._pre_command()
        if mode == self.TriggerMode.NORMAL:
            self.gpib.write(":TRIG:MODE NORM")
        elif mode == self.TriggerMode.AUTO:
            self.gpib.write(":TRIG:MODE AUTO")

    def set_acquire_type(self, mode):
        """Set the trigger type"""
        self._pre_command()
        if mode == self.AcquireType.AUTO:
            self.gpib.write(":ACQ:TYPE AUTO")
        elif mode == self.AcquireType.NORMAL:
            self.gpib.write(":ACQ:TYPE NORM")
        elif mode == self.AcquireType.GLITCH:
            self.gpib.write(":ACQ:TYPE GLIT")

    def get_waveform_preamble(self):
        """Set the trigger type"""
        self._pre_command()
        self.gpib.write("WAV:PRE?")
        tmp = self.gpib.query("++read").split(",")
        return {"format":      int(  tmp[0]),
                "type":        int(  tmp[1]),
                "points":      int(  tmp[2]),
                "count":       int(  tmp[3]),
                "X increment": float(tmp[4]),
                "X origin":    float(tmp[5]),
                "X reference": float(tmp[6]),
                "Y increment": float(tmp[7]),
                "Y origin":    float(tmp[8]),
                "Y reference": float(tmp[9])}

    def set_label_order(self, _label_order):
        """Set the order of the label on the CRT"""
        self._pre_command()
        self.gpib.write(":DISP:ORD "+",".join(map(str, _label_order)))

    def set_label_text(self, _label_text):
        """Set the text of the label, from channel 0 for every element of the list (max 16)"""
        self._pre_command()
        for _n, _label in enumerate(_label_text):
            self.set_channel_label(_n, _label)

    #Color 2 (full bright) doesn't work
    def set_pixel(self, x, y, color):
        """Set the pixel at <x>, <y> to the color <color>"""
        #x range: 0..500, y range: 0..275
        #Available color: 0 (OFF), 1 (half bright), 2 (full bright)
        self._pre_command()
        self.gpib.write(f":DISP:PIX {x},{y},{color}", sleep=0.015)

    def set_display_column(self, col):
        """Set the display column (Range: 0..62)"""
        self._pre_command()
        self.gpib.write(f":DISP:COL {col}")

    def set_display_row(self, row):
        """Set the display row (Range: 1..20)"""
        self._pre_command()
        self.gpib.write(f":DISP:ROW {row}")

    def set_display_normal(self):
        """Set the display to normal mode (Show the measured value)"""
        self._pre_command()
        self.gpib.write(":DISP:TEXT BLANK")

    def set_display_text(self, text):
        """Set a custom text on the display (Max 64 character)"""
        self._pre_command()
        self.gpib.write(f":DISP:LINE \"{text}\"")

    def local(self):
        """Go to local mode (Reenable the front panel control)"""
        self._pre_command()
        self.gpib.local()
