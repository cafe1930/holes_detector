import serial
from time import sleep, time


def main_destroyer(points_lst: list, port_name=''):
    '''
    @param: port_name = either '/dev/tty.*' (for Ubuntu/Linux) or 'COM*' (for Windows)
    '''

    try:
        # connecting to Arduino
        prt = serial.Serial(port_name, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                                           stopbits=serial.STOPBITS_ONE, timeout=1, write_timeout=20)
        prt.write(bytearray(str(24) + '\n', encoding="utf-8"))  # reseting
        sleep(2)  # necessary time for initialization
        prt.write(bytearray('$X\n', encoding="utf-8"))
        for dx, dy in points_lst:
            # building bytearray
            # send: G1 X"dx" Y"dy" Z"270" - for positioning
            if dx >= 0 and dy >= 0:
                bytes_to_arduino = "G1G53X" + str(dx) + "Y" + str(dy) + "Z270 F3000\n"  # "G91G0X", G1 - linear motion, G53 - with absolute coordinates, F3000 - speed
                prt.write(bytearray(bytes_to_arduino, encoding="utf-8"))  # sending position
                sleep(10)  # waiting for positioning for 10 sec
                prt.write(bytearray("M3 S1\n", encoding="utf-8"))  # M3 S1 - enabling spindle with speed 1
                sleep(2.5)  # waiting for speed controller calibration

                prt.write(bytearray("S16\n", encoding="utf-8"))  # starting speed = 16, max speed = 21
                sleep(2)

                ground_zeros = time()
                dt = 0
                while dt < 2:
                    prt.write(bytearray("S" + str(int(16 + dt * (22 - 16) / 2)) + "\n", encoding="utf-8"))  # starting speed = 16, max speed = 21
                    sleep(0.3)
                    dt = time() - ground_zeros

                # prt.write(bytearray("M3 S21\n", encoding="utf-8"))  # speed 21
                sleep(8)  # waiting for ending of bombing for 8 sec with speed 21
                prt.write(bytearray("M5 S0\n", encoding="utf-8"))  # M5 S0 - disabling spindle
                sleep(0.1) # waiting for 0.1 sec, cooldown
                prt.write(bytearray("G1G53X0Y0Z0 F3000\n", encoding="utf-8"))  # homing
                sleep(10)  # waiting for homing for 10 sec
                prt.write(bytearray(str(24) + '\n', encoding="utf-8"))
                sleep(2)  # necessary time for initialization
        prt.close()  # closing the connection with Arduino
    except serial.SerialException as ex:
        print(ex)

if __name__ == '__main__':
    main_destroyer([[330, 110], [200, 45]], 'COM5')
