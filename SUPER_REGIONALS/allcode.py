###########################################################################
# Total Points - 20
###########################################################################
# equipment inspection                                        - 20 points
###########################################################################
from hub import motion_sensor, port
import runloop, motor_pair, motor,runloop
import time
import sys

# vars and constants
WHEEL_CIRCUMFERENCE=17.5 # 27.6 is the circumference of ADB large wheel and 17.5 is the circumference of ADB small wheel
DEFAULT_SPEED=650 # Small motor (essential): -660 to 660 Medium motor: -1110 to 1110 Large motor: -1050 to 1050
rotation=0

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
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, rotation_in_degrees, 0, velocity = speed, stop=motor.HOLD)

async def driveInArc(distance,lv=DEFAULT_SPEED,rv=DEFAULT_SPEED):
    rotation_in_degrees = round( ( distance / WHEEL_CIRCUMFERENCE ) * 360 )
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, rotation_in_degrees, lv, rv, stop=motor.HOLD)

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
        if direction == 'lift' and degrees <= 350 and abs_value < degrees:
            await motor.run_to_absolute_position(EXTENSION_MOTOR_TOP, degrees, speed, direction=motor.CLOCKWISE, stop = motor.BRAKE)
        elif direction == 'drop' and abs_value > degrees:
            await motor.run_to_absolute_position(EXTENSION_MOTOR_TOP, degrees, speed, direction=motor.COUNTERCLOCKWISE, stop = motor.BRAKE)
        else:
            print ("EXTENSION_MOTOR_TOP - current position is %d..desired position is %d. desired position cannot be less than current position or greater than 350."% (abs_value, degrees))

    if (side == "bottom"):
        if motor.absolute_position(EXTENSION_MOTOR_BOTTOM) < 0:
            abs_value = motor.absolute_position(EXTENSION_MOTOR_BOTTOM) + 360
        else:
            abs_value = motor.absolute_position(EXTENSION_MOTOR_BOTTOM)
        if direction == 'lift' and abs_value < degrees:
            rotation=degrees//360
            degrees=degrees%360
            if rotation > 0:
                for i in range(rotation):
                    await motor.run_to_absolute_position(EXTENSION_MOTOR_BOTTOM, 360, speed, direction=motor.CLOCKWISE, stop = motor.BRAKE)
                await motor.run_to_absolute_position(EXTENSION_MOTOR_BOTTOM, degrees, speed, direction=motor.CLOCKWISE, stop = motor.BRAKE)
            else:
                await motor.run_to_absolute_position(EXTENSION_MOTOR_BOTTOM, degrees, speed, direction=motor.CLOCKWISE, stop = motor.BRAKE)

        if direction == 'drop' and abs_value > degrees:
            rotation=degrees//360
            degrees=degrees%360
            if rotation > 0:
                for i in range(rotation):
                    await motor.run_to_absolute_position(EXTENSION_MOTOR_BOTTOM, 360, speed, direction=motor.COUNTERCLOCKWISE, stop = motor.BRAKE)
                await motor.run_to_absolute_position(EXTENSION_MOTOR_BOTTOM, degrees, speed, direction=motor.COUNTERCLOCKWISE, stop = motor.BRAKE)
            else:
                await motor.run_to_absolute_position(EXTENSION_MOTOR_BOTTOM, degrees, speed, direction=motor.COUNTERCLOCKWISE, stop = motor.BRAKE)
        else:
            print ("EXTENSION_MOTOR_BOTTOM - current position is %d..desired position is %d. desired position cannot be less than current position or greater than 350."% (abs_value, degrees))

async def resetExtension(extension=EXTENSION_MOTOR_TOP):
    if motor.absolute_position(extension) < 0:
        abs_value = motor.absolute_position(extension) + 360
    else:
        abs_value = motor.absolute_position(extension)
    if abs_value in range(13,350):
        print (abs_value)
        await motor.run_to_absolute_position(extension,10,900,direction=motor.COUNTERCLOCKWISE,stop=motor.BRAKE)

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
    
    # Slot 0 - Reset extensions
    # await resetExtension()

    # Slot 1: shipping lanes and unidentfied creature
    # await resetExtension()
    # await drive(33)
    # await turnRight(16)
    # await moveMotor('lift','top',90,100)
    # await drive(2)
    # await moveMotor('lift','top',170)
    # await turnRight(40)
    # await drive(-15)
    # await moveMotor('drop','top',15)
    # await turnRight(75)
    # await drive(-25,900)
    # await driveInArc(50,900,1050)
    # await moveMotor('lift','top',320)

    # Slot 2: collecting items
    # await drive(70,950)
    # await turnLeft(87)
    # await drive(105,950)
    # await turnLeft(50)
    # await drive(60,950)

    # slot 3 - pick trident part(s) and get coral tree
    # await resetExtension()
    # await drive(5)
    # await moveMotor('lift','top',130)
    # await turnRight(50)
    # await drive(50)
    # await drive(5,200)
    # await moveMotor('lift','top',220,200)
    # await turnRight(140)
    # await drive(15)
    # await moveMotor('drop','top',60,200)
    # await moveMotor('lift','top',130)
    # await turnRight(105)
    # await drive(40)
    # await moveMotor('drop','top',20)
    # await turnLeft(80)
    # await drive(30)
    # await moveMotor('lift','top',230)
    
    # slot 5 - Scuba diver, sea bed and submersible
    # await drive(40)
    # await turnRight(25)
    # await drive(33)
    # await moveMotor('drop','top',175,100)
    # await drive(4)
    # await moveMotor('drop','top',180,100)
    # await turnRight(5)
    # await drive(-10,300)
    # await turnRight(28)
    # await moveMotor('drop','top',120,100)
    # await drive(43)
    # await moveMotor('lift','top',200,100)
    # await runloop.sleep_ms(1000)
    # await drive(-17)
    # await turnLeft(12)
    # await moveMotor('drop','top',100,100)
    # await drive(10,200)
    # await moveMotor('lift','top',250,100)
    # await turnRight(15)
    # await drive(-10)
    # await driveInArc(-105, 900, 750)
        
    # Slot 6 - boat to latch
    # await drive(70)
    # await driveInArc(-20,600,400)
    # await driveInArc(-15,300,900)
    # await drive(40)
    # await drive(-10)



###################################################################################
###################################################################################
# DO NOT CHANGE ANYTHING AFTER THIS LINE. WRITE MISSION CODE BEFORE THIS LINE
###################################################################################
###################################################################################
runloop.run(main())
sys.exit()
