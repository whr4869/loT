#include <PID_v1.h>  // 引入PID_v1库，用于PID控制
#include <Servo.h>   // 引入Servo库，用于控制舵机

/*************************电机对象*********************************/
#define servoNum 4                        
#define angleTolerance 2                
int servoPin[servoNum] = { 3, 5, 6, 9 };  
double newOutVal[servoNum];
double oldOutVal[servoNum];
bool servoRunFlag = false;
Servo myservo[servoNum];  
/****************************************************************/

/*************************PID调节*********************************/
#define pidComputeTime 50  

unsigned long pidComputeLastTime = 0;
// 指定链接和初始调节参数
double Kp = 0.95, Ki = 0.5, Kd = 0.2;
/****************************************************************/


#define jySerial Serial  
bool flag = false;       

struct SAngle {
  short Euler[3];
};

struct SAngle jyEuler;         // 声明了一个名为 jyEuler 的结构体变量，类型为 SAngle。用于存储欧拉角信息。
float Angle[3] = { 0, 0, 0 };  // 定义了一个长度为 3 的浮点数类型数组 Angle，并初始化为 {0, 0, 0}。用于存储角度信息。
unsigned long printTime = 0;   // 定义了一个无符号长整型变量 printTime，并将其初始化为 0。用于记录时间戳或计时器的值。

void setup() {
  delay(100);
  Serial.begin(9600);    
  jySerial.begin(9600);  
  for (int i = 0; i < servoNum; i++) {
    myservo[i].attach(servoPin[i]);  
    delay(2);                       
    myservo[i].write(0);             
    delay(2);                        
  }
  Serial.println("System Start");  // 通过串口打印输出消息 "System Start"，用于指示系统已启动。
}
void loop() {
  while (jySerial.available() > 0) {  // 当串口有可用数据时
    char jydata = jySerial.read();    // 从串口读取一个字符
    // Serial.print(jydata);  
    jySensorRead(jydata);  // 调用函数处理接收到的数据
    delay(1);              
    if (flag) {            // 如果标志位设置为真（满足某个条件）
      flag = false;        // 重置标志位为假
      break;               // 退出循环
    }
  }

  for (int id = 0; id < 3; id++) {                       // 循环从id=0到id=2
    Angle[id] = (float)jyEuler.Euler[id] / 32768 * 180;  // 使用欧拉角数据计算角度，并将结果存储在Angle数组中
  }

  if (millis() - printTime >= 20) {  //串口打印陀螺仪角度值
    printTime = millis();
    Serial.print("\t x:");
    Serial.print(Angle[0]);
    Serial.print("°,");
    Serial.print("\t | y:");
    Serial.print(Angle[1]);
    Serial.print("°");
    // Serial.print("\t | z:");
    // Serial.print(Angle[2]);
    // Serial.print("°,");
    Serial.println();
  }
  if (millis() - pidComputeLastTime > pidComputeTime) {  
    pidComputeLastTime = millis();                      
    if (Angle[0] >= 0) {                                
      computePid(abs(Angle[0]), 0, &newOutVal[0]);      
      // Serial.println((int)newOutVal[0]);  // 可选：串口打印输出
      if (abs(newOutVal[0] - oldOutVal[0]) > angleTolerance) {  
        myservo[0].write((int)newOutVal[0]);                    
        oldOutVal[0] = newOutVal[0];                            
      }
    } else {                                        // 如果角度小于0
      computePid(abs(Angle[0]), 0, &newOutVal[1]);  // 调用PID计算函数计算输出值
      // Serial.println((int)newOutVal[1]);  
      if (abs(newOutVal[1] - oldOutVal[1]) > angleTolerance) {  
        myservo[1].write((int)newOutVal[1]);                    // 更新舵机输出角度
        oldOutVal[1] = newOutVal[1];                            // 更新上次输出值为当前输出值
      }
    }

    if (Angle[1] >= 0) {                            // 如果角度大于等于0
      computePid(abs(Angle[1]), 0, &newOutVal[2]);  // 调用PID计算函数计算输出值
      // Serial.println((int)newOutVal[2]);  // 可选：串口打印输出
      if (abs(newOutVal[2] - oldOutVal[2]) > angleTolerance) {  // 如果输出值与上次输出值之差超过角度容差
        myservo[2].write((int)newOutVal[2]);                    // 更新舵机输出角度
        oldOutVal[2] = newOutVal[2];                            // 更新上次输出值为当前输出值
      }
    } else {                                        // 如果角度小于0
      computePid(abs(Angle[1]), 0, &newOutVal[3]);  // 调用PID计算函数计算输出值
      // Serial.println((int)newOutVal[3]);  // 可选：串口打印输出
      if (abs(newOutVal[3] - oldOutVal[3]) > angleTolerance) {  // 如果输出值与上次输出值之差超过角度容差
        myservo[3].write((int)newOutVal[3]);                    // 更新舵机输出角度
        oldOutVal[3] = newOutVal[3];                            // 更新上次输出值为当前输出值
      }
    }
  }
}

void jySensorRead(unsigned char ucData) {
  static unsigned char ucRxBuffer[250];  
  static unsigned char ucRxCnt = 0;      
  ucRxBuffer[ucRxCnt++] = ucData;        
  if (ucRxBuffer[0] != 0x55) {           
    ucRxCnt = 0;                         
    return;                              
  }
  if (ucRxCnt < 11) {  
    return;            
  } else {
    switch (ucRxBuffer[1]) {  
      case 0x53:              
        {
          memcpy(&jyEuler, &ucRxBuffer[2], 8);  
          flag = true;                          
        }
        break;
    }
    ucRxCnt = 0;  
  }
}

void computePid(double Setpoint, double Input, double *Output) {
  double output = 0;                                         
  PID myPID(&Input, &output, &Setpoint, Kp, Ki, Kd, DIRECT);  
  myPID.SetMode(AUTOMATIC);                                   

  myPID.Compute();   
  *Output = output;  
}
