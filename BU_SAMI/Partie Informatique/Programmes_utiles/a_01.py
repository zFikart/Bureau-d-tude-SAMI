## Reculer_01

## Reculer de 20 cm et afficher "Je recule"
# D

from time import sleep

from ev3dev2.motor import OUTPUT_B, OUTPUT_C, MoveDifferential

# Speed as a percentage of the motor’s maximum rated speed - SpeedPercent(percent)
from ev3dev2.motor import SpeedPercent

from ev3dev2.button import Button

from ev3dev2.display import Display

# .SpeedRPM(200), 5) rotates the motor at 200 RPM (rotations-per-minute) for five seconds.
mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C)

# Speed as a percentage of the motor’s maximum rated speed.

mdiff.on_for_distance(SpeedPercent(90), 200)

# .160
# .15numeropc