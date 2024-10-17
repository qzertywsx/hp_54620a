# hp_54620a
Python module for the HP 54620A logic analyzer

You must use my GPIB or GPIB_WIFI module to use this module.

## Supported command (Some description to update):
### `get_idn()`
Return the ID of the instrument

### `reset()`
Reset the instrument to the default state

### `set_threshold(ch, t_type, value=0)`
Enable the filter
<table>
  <tr><td>ch</td><td>Description</td></tr>
  <tr><td>HP54620A.ChannelGroup.CHANNEL0_7</td><td>Channel 0..7</td></tr>
  <tr><td>HP54620A.ChannelGroup.CHANNEL8_15</td><td>Channel 8..15</td></tr>
</table>

<table>
  <tr><td>t_type</td><td>Description</td></tr>
  <tr><td>HP54620A.ThresholdType.CMOS</td><td>Set threshold type to CMOS</td></tr>
  <tr><td>HP54620A.ThresholdType.ECL</td><td>Set threshold type to ECL</td></tr>
  <tr><td>HP54620A.ThresholdType.TTL</td><td>Set threshold type to TTL</td></tr>
  <tr><td>HP54620A.ThresholdType.USER</td><td>Set threshold type to USER</td></tr>
</table>

`value`:

Custom threshold in volt (from -6 V to 6 V)

`value` is not mandatory, is mandatory if you choose the `USER` threshold type.

### `autoscale()`
Autoscale the instrument

### `set_grid(grid)`
Set the grid
<table>
  <tr><td>grid</td><td>Description</td></tr>
  <tr><td>HP54620A.Grid.OFF</td><td>Set the grid type to OFF</td></tr>
  <tr><td>HP54620A.Grid.FRAME</td><td>Set the grid type to FRAME</td></tr>
  <tr><td>HP54620A.Grid.FULL</td><td>Set the grid type to FULL</td></tr>
</table>

### `set_inverse_display(on)`
Invert the display
#It's doing nothing?
<table>
  <tr><td>on</td><td>Description</td></tr>
  <tr><td>True</td><td>Invert the display</td></tr>
  <tr><td>False</td><td>Don't invert the display</td></tr>
</table>

### `display_label(on)`
Display the label
<table>
  <tr><td>on</td><td>Description</td></tr>
  <tr><td>True</td><td>Switch on the label</td></tr>
  <tr><td>False</td><td>Switch off the label</td></tr>
</table>

### `set_channel_label(ch, _label)`
Set the channel label

### `measure(function)`
Take a measurement

### `show_measure(on)`
Show the measurement on the CRT

### `source_measure(ch)`
Source of the measurement

### `run()`
Set instrument in run mode

### `run_single()`
Set instrument in single run mode

### `stop()`
Set instrument in stop mode

### `set_timebase_delay(delay)`
Set the timebase delay

You can use suffix` S, MS, US, NS

### `set_timebase_range(_range)`
Set the timebase range

You can use suffix` S, MS, US, NS

### `set_timebase_mode(mode)`
Set the timebase mode

### `set_timebase_reference(reference)`
Set the timebase reference

### `enable_vernier(on)`
Enable the vernier

### `set_trigger_type(trigger)`
Set the trigger type

### `set_trigger_edge(ch, edge)`
Set the thrigger edge of a channel

### `set_trigger_mode(mode)`
Set the trigger type

### `set_acquire_type(mode)`
Set the trigger type

### `get_waveform_preamble()`
Set the trigger type

### `set_label_order(_label_order)`
Set the order of the label on the CRT

### `set_label_text(_label_text)`
Set the text of the label, from channel 0 for every element of the list (max 16)

### `set_pixel(x, y, color)`
Set the pixel at <x>, <y> to the color <color>

x range: 0..500

y range: 0..275

Available color: 0 (OFF), 1 (half bright), 2 (full bright)

Color 2 (full bright) doesn't work

### `set_display_column(col)`
Set the display column (Range` 0..62)

### `set_display_row(row)`
Set the display row (Range` 1..20)

### `set_display_normal()`
Set the display to normal mode (Show the measured value)

### `set_display_text(text)`
Set a custom text on the display (Max 64 character)

### `local()`
Go to local mode (Reenable the front panel control)

## Usage:
```python
from gpib_all import AR488Wifi
from hp_54620a import HP54620A

gpib = AR488Wifi('192.168.178.36')
logic = HP54620A(gpib, 8)
print(logic)
logic.reset()
#Set the order of the input on the screen
label_order = [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
logic.set_label_order(label_order)
#Set the label of all the input
label = ["D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "WR", "A0", "RD", "BUG", "BUSY"]
logic.set_label_text(label)
logic.enable_vernier(True)
logic.set_timebase_reference(HP54620A.TimeBaseReference.LEFT)
logic.set_timebase_range("250ms")
logic.set_trigger_edge(8, HP54620A.TriggerEdge.RISING)
logic.set_acquire_type(HP54620A.AcquireType.NORMAL)
logic.source_measure(8)
print("Frequency:", logic.measure(HP54620A.Function.FREQUENCY), "Hz")
print("Duty cicle:", logic.measure(HP54620A.Function.DUTYCYCLE), "%")
```
## Result of executing the above code:
```
HP 54620A address: 8
Frequency: 403.226 Hz
Duty cicle: 82.54 %
```
