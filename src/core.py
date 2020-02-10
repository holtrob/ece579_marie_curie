import maestro
import servo

def main():
    controller = maestro.Controller()

    servo_name = 'jaw_u_d'
    jaw_u_d_servo = servo.Servo(servo_name, controller)
    print(jaw_u_d_servo)

    jaw_u_d_servo.set_sem_pos('open')

if __name__ == '__main__':
    main()
    