from time import sleep

from ev3dev2.motor import OUTPUT_B, OUTPUT_C
import ev3dev2 as ev

left_motor = ev.motor.LargeMotor(OUTPUT_B)
right_motor = ev.motor.LargeMotor(OUTPUT_C)

speed_rot = 300
time_speed = 2000

def straight_line(speed_rot = speed_rot, time_speed = time_speed):
    """
    speed_sp rotations par minute
    time_sp en millisecondes ie ms
    """
    for m in [left_motor, right_motor]:
        m.run_timed(speed_sp = speed_rot, time_sp = time_speed)
    sleep(1)


def turn_left(speed_rot = speed_rot, time_speed = time_speed):
    left_motor.run_timed(speed_sp = 0, time_sp = time_speed)
    right_motor.run_timed(speed_sp = speed_rot, time_sp = time_speed)
    sleep(1)


def turn_right(speed_rot = speed_rot, time_speed = time_speed):
    left_motor.run_timed(speed_sp = speed_rot, time_sp = time_speed)
    right_motor.run_timed(speed_sp = 0, time_sp = time_speed)

    sleep(1)


straight_line()
turn_left()
# straight_line()



# Se deplace en ligne droite
distance_mm = 20*10 # en 20 cm = 20 * 10 mm
pourcentage = 50

sleep(1)




