###########################################################################
# Total Points - 180
###########################################################################
# 06 - Raise the Mast                    - 30 points
# 03 - Flip coral reef                - 20 points
# 01 - Flip coral buds                - 20 points
# 02 - Release shark                    - 20 points
# 04 - deliver Scuba Diver            - 40 points
# 03 - deliver reef segments                  - 15 points
# 15 - drop all samples and deliver boat      - 30
# # 08 - Artificial habitat       - 30 points
# collect Krill                 -  0 points
# collect part of trident       - 20 points
#go to the right side of the map with krills
###########################################################################
from hub import motion_sensor, port
import runloop, motor_pair, motor,runloop
import time
import sys
# vars and constants
WHEEL_CIRCUMFERENCE=17.5 # 27.6 is the circumference of ADB large wheel and 17.5 is the circumference of ADB small wheel
DEFAULT_SPEED=650 # Small motor (essential): -660 to 660 Medium motor: -1110 to 1110 Large motor: -1050 to 1050
# ports
MOVEMENT_MOTOR_RIGHT=port.F #red
MOVEMENT_MOTOR_LEFT=port.B #yellow
COLOR_SENSOR_RIGHT=port.D # no color
COLOR_SENSOR_LEFT=port.C # red and yellow
EXTENSION_MOTOR_TOP=port.E #blue
EXTENSION_MOTOR_BOTTOM=port.A #green

# prep the hub
motion_sensor.reset_yaw(0)
motor_pair.unpair(motor_pair.PAIR_1)
motor_pair.pair(motor_pair.PAIR_1,MOVEMENT_MOTOR_LEFT,MOVEMENT_MOTOR_RIGHT)

# drive with a certain speed
async def drive(distance, speed=DEFAULT_SPEED):
    rotation_in_degrees = round( ( distance / WHEEL_CIRCUMFERENCE ) * 360 )
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, rotation_in_degrees, 0, velocity = speed, stop=motor.SMART_COAST)

# drive in an arc with variying motor speeds for left and right
async def driveInArc(distance,lv=DEFAULT_SPEED,rv=DEFAULT_SPEED):
    rotation_in_degrees = round( ( distance / WHEEL_CIRCUMFERENCE ) * 360 )
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, rotation_in_degrees, lv, rv, stop=motor.SMART_COAST)

# turn left
async def turnLeft(angle):
    while motion_sensor.tilt_angles()[0]<(angle*10): #while the angle sensor is less than desired angle
        motor_pair.move(motor_pair.PAIR_1,-100) #both motors will run -100 degrees
    motor_pair.stop(motor_pair.PAIR_1) #stop the motors after that while loop
    motion_sensor.reset_yaw(0) #reset yaw value

# turn right
async def turnRight(angle):
    while motion_sensor.tilt_angles()[0]>(angle*-10): #getting yaw value from tuple
        motor_pair.move(motor_pair.PAIR_1,100) #move to right
    motor_pair.stop(motor_pair.PAIR_1) #stop the motors after that while loop
    motion_sensor.reset_yaw(0) #reset yaw value

# move a give ( top or bottom ) extension motor
async def moveMotor(direction,side,degrees, speed=DEFAULT_SPEED):
    if (side == "top"):
        if motor.absolute_position(EXTENSION_MOTOR_TOP) < 0:
            abs_value = motor.absolute_position(EXTENSION_MOTOR_TOP) + 360
        else:
            abs_value = motor.absolute_position(EXTENSION_MOTOR_TOP)
        if direction == 'lift' and degrees <= 330 and abs_value < degrees:
            await motor.run_to_absolute_position(EXTENSION_MOTOR_TOP, degrees, speed, direction=motor.CLOCKWISE, stop = motor.BRAKE)
        elif direction == 'drop' and abs_value > degrees:
            await motor.run_to_absolute_position(EXTENSION_MOTOR_TOP, degrees, speed, direction=motor.COUNTERCLOCKWISE, stop = motor.BRAKE)
        else:
            print ("EXTENSION_MOTOR_TOP - current position is %d..desired position is %d. desired position cannot be less than current position or greater than 330."% (abs_value, degrees))

    if (side == "bottom"):
        if motor.absolute_position(EXTENSION_MOTOR_BOTTOM) < 0:
            abs_value = motor.absolute_position(EXTENSION_MOTOR_BOTTOM) + 360
        else:
            abs_value = motor.absolute_position(EXTENSION_MOTOR_BOTTOM)
        if direction == 'lift' and degrees <= 330 and abs_value < degrees:
            await motor.run_to_absolute_position(EXTENSION_MOTOR_BOTTOM, degrees, speed, direction=motor.CLOCKWISE, stop = motor.BRAKE)
        elif direction == 'drop' and abs_value > degrees:
            await motor.run_to_absolute_position(EXTENSION_MOTOR_BOTTOM, degrees, speed, direction=motor.COUNTERCLOCKWISE, stop = motor.BRAKE)
        else:
            print ("EXTENSION_MOTOR_BOTTOM - current position is %d..desired position is %d. desired position cannot be less than current position or greater than 330."% (abs_value, degrees))

async def resetExtension(extension=EXTENSION_MOTOR_TOP):
    if motor.absolute_position(extension) < 0:
        abs_value = motor.absolute_position(extension) + 360
    else:
        abs_value = motor.absolute_position(extension)
    if abs_value in range(4,330):
        print (abs_value)
        await motor.run_to_absolute_position(extension,3,720,direction=motor.COUNTERCLOCKWISE,stop=motor.BRAKE)

# main code
async def main():
    '''
    await drive(50) # drives forward 50 cms straight with DEFAULT_SPEED
    await drive(-50) # drives backward 50 cms straight with DEFAULT_SPEED
    await driveInArc(50,100,300) # drives in an arc for 50 cm forward with the left motor moving at speed 100 and the right motor moving at speed 300
    await driveInArc(-50,100,300) # drives in an arc for 50 cm backward with the left motor moving at speed 100 and the right motor moving at speed 300
    await turnLeft(50) # turns left 50 degrees with DEFAULT_SPEED
    await turnRight(50) # turns right 50 degrees with DEFAULT_SPEED
    await moveMotor("top",120) # moves the top extension 120 degrees with DEFAULT_SPEED
    await moveMotor("top",-120) # moves the top extension -120 degrees with DEFAULT_SPEED
    await moveMotor("bottom",120) # moves the bottom extension 120 degrees with DEFAULT_SPEED
    await moveMotor("bottom",-120) # moves the bottom extension -120 degrees with DEFAULT_SPEED
    '''
###################################################################################
###################################################################################
# DO NOT CHANGE ANYTHING BEFORE THIS LINE. WRITE MISSION CODE AFTER THIS LINE
###################################################################################
###################################################################################
    # reset extension
    await resetExtension()
    # Raise the mast
    await drive(18)
    await turnRight(73)
    await drive(39,900)
    await drive(10,200)

    # # Flip coral buds
    await drive(-20)
    await turnLeft(53)
    await moveMotor('lift','top',170)
    await drive(34)
    await moveMotor('drop','top',0,1110)
    await drive(-10)

    # # Coral Nursery
    await moveMotor('lift','top',158)
    await turnRight(75)
    await drive(-18,700)
    await drive(10)

    # # Release shark
    await turnRight(42)
    await drive(-28,1050)
    await drive (5)

    # retrying flip coral buds
    await turnLeft(75)
    await drive(7)
    await moveMotor('drop','top',0,1110)

    # Scuba diver delivery
    await moveMotor('lift','top',170)
    await turnRight(100)
    await moveMotor('lift','top',180)
    await turnRight (75)
    await drive(3)
    await moveMotor('lift','top',230,40)
    await drive(-5)
    await turnLeft (160)
    await moveMotor('drop','top',200,100)
    await turnLeft (15)
    await drive(-3)
    await turnLeft(55)
    await drive(-80)

    # Droping samples in boat
    await moveMotor('lift','top',250)
    await runloop.sleep_ms(1500)
    await drive(15)
    await moveMotor('drop','top',100,300)
    await drive(-10)
    await moveMotor('lift','top',300)
    
    # push coral samples 
    await runloop.sleep_ms(800)
    await drive(10,100)
    await drive(-15)
    await runloop.sleep_ms(1500)
    await drive(65)

###################################################################################
###################################################################################
# DO NOT CHANGE ANYTHING AFTER THIS LINE. WRITE MISSION CODE BEFORE THIS LINE
###################################################################################
###################################################################################

runloop.run(main())
sys.exit()
