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
