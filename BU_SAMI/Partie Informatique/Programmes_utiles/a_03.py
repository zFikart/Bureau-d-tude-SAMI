from time import sleep

from ev3dev2.motor import OUTPUT_B, OUTPUT_C, MoveDifferential

from ev3dev2.wheel import EV3Tire
# - uses the standard wheels known as EV3Tire
from ev3dev2.motor import SpeedRPM
# Speed in rotations-per-minute.

wheel_class : classe de la roue "medium", "large"
# wheel_distance_mm : distance entre les roues en mm
wheel_class = "medium"
wheel_distance_mm = 10*10


mdiff  = MoveDifferential(OUTPUT_B, OUTPUT_C, wheel_class, wheel_distance_mm)

# Se deplace en ligne droite
distance_mm = 20*10 # en 20 cm = 20 * 10 mm
pourcentage = 50
# mdiff.on_for_distance(SpeedRPM(90), distance_mm)

# Rotate 90 degrees clockwise angle droit
# mdiff.turn_right(SpeedRPM(90), 90)
mdiff.on_for_distance(SpeedRPM(pourcentage), distance_mm)
sleep(1)


mdiff.on_arc_right(SpeedRPM(80), 150, 700)

mdiff.off()
