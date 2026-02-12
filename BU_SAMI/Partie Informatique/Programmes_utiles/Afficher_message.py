from ev3dev2.display import Display
from ev3dev2.button import Button
import time

lcd=Display()
lcd.clear()
lcd.draw.text((25,50),"Bonjour Robot !")

# Create a button
button=Button()

# Check if ’ enter ’ button is pressed
while not button.enter:
    lcd.update()
    time.sleep(0.01)






