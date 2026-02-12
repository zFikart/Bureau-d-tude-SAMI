from ev3dev2.motor import OUTPUT_B, LargeMotor, OUTPUT_C

mB = LargeMotor(OUTPUT_B)
mA = LargeMotor(OUTPUT_C)
for m in [mA, mB]:
    m.run_timed(speed_sp =300, time_sp = 2000)