#!/usr/bin/python

import time
import smbus

# ===========================================================================
# Handler for MPU6050
# ===========================================================================
def u16toi16(val) :
    if(val >= 0x8000):
      return-((0xFFFF - val) +1)
    else :
      return val

class Regs :
    SampleRate = 0x19
    Config = 0x1A
    GyroConfig = 0x1B
    AccelConfig = 0x1C
    AccelX = 0x3B
    AccelY = 0x3D
    AccelZ = 0x3F
    Temp = 0x41
    GyroX = 0x43
    GyroY = 0x45
    GyroZ = 0x47
    PowerMgmt1 = 0x6B
    PowerMgmt2 = 0x6C

    @staticmethod
    def getAccelReg(axis) :
      return Regs.AccelX + (axis * 2)
      
class MPU6050 :

  def __init__(self, address=0x68, rate=10) :
    self.I2CAddress=address
    self.bus = smbus.SMBus(1)
    self.bus.write_byte_data(self.I2CAddress, Regs.PowerMgmt1, 0)
    self.bus.write_byte_data(self.I2CAddress, Regs.Config, 0x06)
    self.bus.write_byte_data(self.I2CAddress, Regs.SampleRate, 100)
    self.bus.write_byte_data(self.I2CAddress, Regs.GyroConfig, 0x01)
    self.bus.write_byte_data(self.I2CAddress, Regs.AccelConfig, 0x01)

  def getAccel(self, axis) :
    reg = Regs.getAccelReg(axis)
    v = self.bus.read_byte_data(self.I2CAddress, reg) << 8
    v = v + self.bus.read_byte_data(self.I2CAddress, reg+1)
    return u16toi16(v)

  def getGyro(self, axis) :
    z = self.bus.read_byte_data(self.I2CAddress, Regs.GyroZ) << 8
    z = z + self.bus.read_byte_data(self.I2CAddress, Regs.GyroZ+1)
    return u16toi16(z)

  def getTemp(self) :
    t = self.bus.read_byte_data(self.I2CAddress, Regs.Temp) << 8
    t = t + self.bus.read_byte_data(self.I2CAddress, Regs.Temp+1)
    tc = u16toi16(t)/340 + 37
    return (tc)


