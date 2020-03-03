/* runt_rover.ino
   This program receives (over serial) the speed and direction of the left and
   right sides of the runt rover. This is given by the following form:
   <start marker><left speed integer><seperator><right speed integer><end marker>
   The left and right speeds are values [-100, 100] where a negative value
   specifies the reverse direction. The start marker is the '>' character. The
   seperator is a comma. The end marker is the '<' character.
*/

// PWM pins
#define LEFT_BACK_PIN 3
#define LEFT_MIDDLE_PIN 5
#define LEFT_FRONT_PIN 6
#define RIGHT_BACK_PIN 9
#define RIGHT_MIDDLE_PIN 10
#define RIGHT_FRONT_PIN 11

// Direction pins
#define LEFT_BACK_DIR_PIN 2
#define LEFT_MIDDLE_DIR_PIN 4
#define LEFT_FRONT_DIR_PIN 7
#define RIGHT_BACK_DIR_PIN 8
#define RIGHT_MIDDLE_DIR_PIN 12
#define RIGHT_FRONT_DIR_PIN 13

#define FORWARD LOW
#define REVERSE HIGH

#define LEFT_SPEED_INDEX 0
#define RIGHT_SPEED_INDEX 1

const int BAUD_RATE = 9600; // TODO: Set up baud rate to work with Pi

const int SPEED_MAX = 100;
const int SPEED_MIN = -100;
const char PACKET_START_MARKER = '<';
const char PACKET_SEPARATOR[2] = "|";
const char PACKET_END_MARKER = '>';
const char SPEED_PACKET_SEPARATOR[2] = ",";

int8_t speed_left;
int8_t speed_right;
int8_t speed_left_setpoint;
int8_t speed_right_setpoint;

const int SERIAL_BUFFER_SIZE = 9;
char serial_buffer[SERIAL_BUFFER_SIZE];
bool packet_available;

void setup()
{
  // Configure pins as output for motor drivers
  pinMode(LEFT_BACK_PIN, OUTPUT);
  pinMode(LEFT_MIDDLE_PIN, OUTPUT);
  pinMode(LEFT_FRONT_PIN, OUTPUT);
  pinMode(RIGHT_BACK_PIN, OUTPUT);
  pinMode(RIGHT_MIDDLE_PIN, OUTPUT);
  pinMode(RIGHT_FRONT_PIN, OUTPUT);

  // Configure direction pins
  pinMode(LEFT_BACK_DIR_PIN, OUTPUT);
  pinMode(LEFT_MIDDLE_DIR_PIN, OUTPUT);
  pinMode(LEFT_FRONT_DIR_PIN, OUTPUT);
  pinMode(RIGHT_BACK_DIR_PIN, OUTPUT);
  pinMode(RIGHT_MIDDLE_DIR_PIN, OUTPUT);
  pinMode(RIGHT_FRONT_DIR_PIN, OUTPUT);

  // Initialize global variables
  speed_left = 0;
  speed_right = 0;
  speed_left_setpoint = 0;
  speed_right_setpoint = 0;
  packet_available = false;

  // Begin serial
  Serial.begin(BAUD_RATE);
}

void loop()
{
  receive_data();
  if (packet_available)
  {
    parse_packet();
    packet_available = false;
  }
  update_speed();
  write_speed();
}

/* Check if there is data available to read over serial and add it to the serial
   buffer.
   Input: None
   Return: None
*/
void receive_data()
{
  static bool receive_in_progress = false;
  static byte index = 0;
  char received_char;

  while (Serial.available() && !packet_available)
  {
    received_char = Serial.read();
    if (!receive_in_progress)
    {
      if (received_char == PACKET_START_MARKER)
      {
        // Found start of new packet. Next call to receive_data() will start
        // looking for data.
        receive_in_progress = true;
      }
    }
    else // Receive in progress
    {
      if (received_char == PACKET_START_MARKER)
      {
          // Found start marker while already reading in a packet. Discard
          // current packet and look for new data that matches start marker.
          index = 0;
      }
      else if (received_char == PACKET_END_MARKER)
      {
        // End marker is found. Set packet_available to signal that packet is
        // available for parsing.
        serial_buffer[index] = '\0';
        index = 0;
        packet_available = true;
        receive_in_progress = false;
      }
      else
      {
        // Add data to buffer
        serial_buffer[index] = received_char;
        index++;
        if (index >= SERIAL_BUFFER_SIZE)
        {
          // Reached end of buffer without finding end marker. Discard
          // current data.
          index = 0;
          receive_in_progress = false;
        }
      }
    }
  }
}

/* Extract the speed setpoint values from the serial buffer and update
   speed_left and speed_right
   Input: None
   Return: None
*/
void parse_packet()
{
  char* strtok_ptr;
  int temp_speed_left_setpoint;
  int temp_speed_right_setpoint;
  char temp_chars[SERIAL_BUFFER_SIZE];
  int speed_values[2];
  int i;
  char mode;

//  copy serial buffer over to a new string
  strncpy(temp_chars, serial_buffer, SERIAL_BUFFER_SIZE);
//  split the packet(temp_chars) into 2 segments by the delimiter '|'
  strtok_ptr = strtok(temp_chars, PACKET_SEPARATOR);
//  copy over the first segment, which contains the mode, into a variable
  mode = *strtok_ptr;
//  point to the second segment containing the data of the packet
  strtok_ptr = strtok(NULL, PACKET_SEPARATOR);

//  switch case to go through the modes
  switch(mode){

//  this case asks for ID
    case 'I':
    
      Serial.write(">Motor driver<");
      break;

//    data contains the motor speeds. data packet is "(left Speed),(right Speed)"
    case 'S':

//      split the speed data into segments using the delimiter ','
      strtok_ptr = strtok(strtok_ptr, SPEED_PACKET_SEPARATOR);
      for (i = 0; i < 2; i++)
      {
          speed_values[i] = atoi(strtok_ptr);
          if (speed_values[i] < SPEED_MIN || speed_values[i] > SPEED_MAX)
          {
            // Receieved speed is not in range. Ignore this packet.
            return;
          }
          strtok_ptr = strtok(NULL, SPEED_PACKET_SEPARATOR);
      }
      speed_left_setpoint = speed_values[LEFT_SPEED_INDEX];
      speed_right_setpoint = speed_values[RIGHT_SPEED_INDEX];
      break;
   
  }

}

/* Increment/decrement speed_left and speed_right by 1 to move closer to the
   setpoint.
   Input: None
   Return: None
*/
void update_speed()
{
  if (speed_left < speed_left_setpoint)
  {
    speed_left++;
  }
  else if (speed_left > speed_left_setpoint)
  {
    speed_left--;
  }

  if (speed_right < speed_right_setpoint)
  {
    speed_right++;
  }
  else if (speed_right > speed_right_setpoint)
  {
    speed_right--;
  }
}

/* Write speed_left and speed_right to the appropriate pins.
   Input: None
   Return: None
*/
void write_speed()
{
  int write_direction_left;
  int write_direction_right;
  int write_speed_left;
  int write_speed_right;
  const int DUTY_CYCLE_MAX = 255;

  // TODO: Could change this to write direction separately, since direction
  //       won't need to be written as often

  // Extract direction info from speed values
  if (speed_left < 0)
  {
    write_direction_left = REVERSE;
  }
  else
  {
    write_direction_left = FORWARD;
  }

  if (speed_right < 0)
  {
    write_direction_right = REVERSE;
  }
  else
  {
    write_direction_right = FORWARD;
  }

  write_speed_left = map(abs(speed_left), 0, SPEED_MAX, 0, DUTY_CYCLE_MAX);
  write_speed_right = map(abs(speed_right), 0, SPEED_MAX, 0 , DUTY_CYCLE_MAX);

  // TODO: Implement this
  // Motors will just buzz if speed is too low
  //  if (speed_left >= 80)
  //  {
  //    writeSpeedLeft = speed_left;
  //  }
  //
  //  if (speed_right >= 80)
  //  {
  //    writeSpeedRight = speed_right;
  //  }

  // Write motor direction
  digitalWrite(LEFT_BACK_DIR_PIN, write_direction_left);
  digitalWrite(LEFT_MIDDLE_DIR_PIN, write_direction_left);
  digitalWrite(LEFT_FRONT_DIR_PIN, write_direction_left);
  digitalWrite(RIGHT_BACK_DIR_PIN, write_direction_right);
  digitalWrite(RIGHT_MIDDLE_DIR_PIN, write_direction_right);
  digitalWrite(RIGHT_FRONT_DIR_PIN, write_direction_right);

  // Write motor speed
  analogWrite(LEFT_BACK_PIN, write_speed_left);
  analogWrite(LEFT_MIDDLE_PIN, write_speed_left);
  analogWrite(LEFT_FRONT_PIN, write_speed_left);
  analogWrite(RIGHT_BACK_PIN, write_speed_right);
  analogWrite(RIGHT_MIDDLE_PIN, write_speed_right);
  analogWrite(RIGHT_FRONT_PIN, write_speed_right);
}
