## Reculer_01

## Reculer de 20 cm et afficher "Je recule"
# Dans cet exercice, vous allez écrire une méthode pour reculer le robot de 20 cm et qu’il affiche sur l’écran "Je recule". Vous programmez deux solutions : une solution avec les objets moteurs et une autre avec la classe MoveDifferential

import time

from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C

# Speed as a percentage of the motor’s maximum rated speed - SpeedPercent(percent)
from ev3dev2.motor import SpeedPercent
from ev3dev2.button import Button

# .SpeedRPM(200), 5) rotates the motor at 200 RPM (rotations-per-minute) for five seconds.

lmotor, rmotor = [LargeMotor(address) for address in (OUTPUT_B ,OUTPUT_C)]
# button = Button()

start = time.time()
lmotor.run_timed(speed_sp = 1000, time_sp = 5000)
rmotor.run_timed(speed_sp = 1000, time_sp = 5000)

# if button.enter:
# mdiff.on_for_distance(SpeedPercent(100), 5000)
# start = time.time()

nb_sec = time.time() - start
print(nb_sec)


# .160
# .15numeropc