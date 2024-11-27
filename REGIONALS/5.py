###########################################################################
# Total Points - 110
###########################################################################
# 00 - Collect unidentified creature       - 20 points
# 13 - Shipping Lanes                      - 30 points
# 11 - Sonar Discovery                     - 30 points
# 12 - Feed the whale                      - 50 points
###########################################################################

from hub import motion_sensor, port
import runloop, motor_pair, motor,runloop

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
async def moveMotor(side, degrees, speed=DEFAULT_SPEED):
    if (side == "top"):
        await motor.run_for_degrees(EXTENSION_MOTOR_TOP, degrees, speed, stop = motor.HOLD)
    if (side == "bottom"):
        await motor.run_for_degrees(EXTENSION_MOTOR_BOTTOM, degrees, speed, stop = motor.HOLD)

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
    await turnLeft(90)
    await drive(-70)
    await turnRight(45)
    await drive(-20)
    await drive(30)
    await turnLeft(45)
    await drive(50)
    await turnRight(90)
    await drive(-10)

###################################################################################
###################################################################################
# DO NOT CHANGE ANYTHING AFTER THIS LINE. WRITE MISSION CODE BEFORE THIS LINE
###################################################################################
###################################################################################

runloop.run(main())
