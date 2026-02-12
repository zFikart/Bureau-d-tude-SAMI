## Reculer_01

## Reculer de 20 cm et afficher "Je recule"
# D

from time import sleep

from ev3dev2.motor import OUTPUT_B, OUTPUT_C, MoveDifferential

from ev3dev2.wheel import EV3Tire
# - uses the standard wheels known as EV3Tire
from ev3dev2.motor import SpeedRPM
# Speed in rotations-per-minute.

# test with a robot that:
# - uses the standard wheels known as EV3Tire
# - wheels are 16 studs apart

mdiff  = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3Tire, 16*8)

# Se deplace en ligne droite
distance_mm = 10*10 # en 20 cm = 20 * 10 mm
# mdiff.on_for_distance(SpeedRPM(90), distance_mm)

# Rotate 90 degrees clockwise angle droit
# mdiff.turn_right(SpeedRPM(40), 90)

for nbre_cote in range(4):
    mdiff.on_for_distance(SpeedRPM(90), distance_mm)
    sleep(1)
    mdiff.turn_right(SpeedRPM(80), 90)
    sleep(1)

