from marie_servo_config import servo_channels, servo_positions
import maestro

controller = maestro.Controller()

servo_name = 'jaw_u_d'
servo_channel = servo_channels[servo_name]
print(f"Servo {servo_name} is on channel {servo_channel}")

controller.setTarget(servo_channels['jaw_u_d'], servo_positions['jaw_u_d']['open'])