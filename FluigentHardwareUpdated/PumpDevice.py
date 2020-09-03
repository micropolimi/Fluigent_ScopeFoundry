from __future__ import print_function    # Used for "print" function compatibility between Python 2.x and 3.x versions
import platform                            # Library used for x64 or x86 detection
import time                                # Time library, use of sleep function
import ctypes                            # Used for variable definition types
from ctypes import *                  # Used to load dynamic linked libraries

#import PumpHardware

# Variable types definition 
mfcsHandle = c_ulonglong(0)    # mfcsHandle is the session handler used by all functions after initialization
mySerial = c_ushort(0)                # device serial number
C_error = c_char()                    # error returned code when calling dll functions
B_OK = bool(False)
purge_status = c_byte(0)

pressure_setpoint = c_float(20)    # Pressure set in mbar
pressure_read = c_float(0)
timeStamp = c_ushort(0)
P=10

# Load dll into memory
# If using 64bit python version please load mfcs_c_64.dll instead
lib_mfcs = ctypes.WinDLL('C:\LabPrograms\Python\FluigentHardwareUpdated\mfcs_c_64.dll')


class MFCSDevice(object):
    
    def __init__(self,hardware):
        self.hardware = hardware #to have a communication between hardware and device, I create this attribute
        #self.pump_model = self.get_serial()
        
    
    #def initialization(self):
        # Initialization function prototype
        # Functions can also be directly called using "lib_mfcs" 
        mfcsInit = lib_mfcs.mfcs_initialisation
        mfcsInit.restype = c_ulonglong
        mfcsInit.argtypes = [c_ushort]
        
        # Initialize the first MFCS in Windows enumeration list 
        self.mfcsHandle = mfcsInit(0)
        
        # Print status on MFCS initialization
        if (self.mfcsHandle != 0):
            print ('MFCS initialized')

        else:
            print ('Error on MFCS initialization. Please check that device is plugged in.')
        
        # Sends channel configuration
        C_error=lib_mfcs.mfcs_set_alpha(c_ulonglong(self.mfcsHandle),0,5)   
        
    def get_serial(self):
        
        serial_nr = lib_mfcs.mfcs_get_serial(c_ulonglong(self.mfcsHandle), byref(timeStamp))
        print(type(serial_nr))
        return timeStamp.value
        
        
    def set_pressure_channel_1(self,P):
        
        C_error = lib_mfcs.mfcs_set_auto(c_ulonglong(self.mfcsHandle),1,c_float(P))

    def set_pressure_channel_2(self,P):
        
        C_error = lib_mfcs.mfcs_set_auto(c_ulonglong(self.mfcsHandle),2,c_float(P))
    
    def set_pressure_channel_3(self,P):
        
        C_error = lib_mfcs.mfcs_set_auto(c_ulonglong(self.mfcsHandle),3,c_float(P))
     
    def set_pressure_channel_4(self,P):
        
        C_error = lib_mfcs.mfcs_set_auto(c_ulonglong(self.mfcsHandle),4,c_float(P))
            
    def read_pressure_channel_1(self):
        
        C_error = lib_mfcs.mfcs_read_chan(c_ulonglong(self.mfcsHandle),1,byref(pressure_read), byref(timeStamp))
        return pressure_read.value
    
    def read_pressure_channel_2(self):
        
        C_error = lib_mfcs.mfcs_read_chan(c_ulonglong(self.mfcsHandle),2,byref(pressure_read), byref(timeStamp))
        return pressure_read.value
    def read_pressure_channel_3(self):
        
        C_error = lib_mfcs.mfcs_read_chan(c_ulonglong(self.mfcsHandle),3,byref(pressure_read), byref(timeStamp))
        return pressure_read.value
    
    def read_pressure_channel_4(self):
        
        C_error = lib_mfcs.mfcs_read_chan(c_ulonglong(self.mfcsHandle),4,byref(pressure_read), byref(timeStamp))
        return pressure_read.value
        
    def setall_zeropressure(self,B): 
        
        # Set pressure to 0 mbar before exit
        # C_error=lib_mfcs.mfcs_set_alpha(c_ulonglong(self.mfcsHandle),0,5)   # Sends channel configuration
        C_error = lib_mfcs.mfcs_set_auto(c_ulonglong(self.mfcsHandle),0,c_float(0)) 
   
    
    def set_purge_on(self):
    
        C_error = lib_mfcs.mfcs_set_purge_on(c_ulonglong(self.mfcsHandle),"ON")

#BISOGNA DECIDERE SE FARLA NEL DEVICE O NELLHARDWARE
    
#     def save_pressures(self, flag):
#         
#         if flag:
#             
#             self.saved_pressures = []
#             
#             for i in range(1,3):
#                 C_error = lib_mfcs.mfcs_read_chan(c_ulonglong(self.mfcsHandle),i,byref(pressure_read), byref(timeStamp))
#                 self.saved_pressures.append(pressure_read.value)
#     
    
    def set_saved_pressures(self, flag):
        
        if flag:
            
            for i in range(1,3):
                C_error = lib_mfcs.mfcs_set_auto(c_ulonglong(self.mfcsHandle),i,c_float(self.saved_pressures[i-1]))
           
        
#     def save_pressure(self):
#         self.pressure = []
#  
#         for i in range(1,2):
#             C_error = lib_mfcs.mfcs_read_chan(c_ulonglong(self.mfcsHandle),i,byref(pressure_read), byref(timeStamp))
#             self.pressure.append(pressure_read.value)
#             print(self.pressure)
#             return self.pressure    
#     
#     def set_saved_pressure(self):
#         C_error = lib_mfcs.mfcs_set_auto(c_ulonglong(self.mfcsHandle),1,c_float(P))
#         #if self.hardware.read_pressure_1.hardware_read_func: #otherwise, if we have not defined yet the function, we have an error...
#         if hasattr(self.hardware, 'read_pressure_1'):    
#             time.sleep(0.5)
#             self.hardware.read_pressure_1.read_from_hardware()
#         self.pressure = []
# 
#         for i in range(1,4):
#             C_error = lib_mfcs.mfcs_read_chan(c_ulonglong(self.mfcsHandle),i,byref(pressure_read), byref(timeStamp))
#             self.pressure.append(pressure_read.value)
#             return self.pressure   


 
    def close(self):
        
        
        B_OK = lib_mfcs.mfcs_close(c_ulonglong(self.mfcsHandle))
        if (B_OK == True):
            print ('USB connection closed')
        if (B_OK == False):
            print ('Failed to close USB connection')
        
        
        
        
        

if __name__ == "__main__":
    
    MFCS = MFCSDevice(hardware=None)
    
    MFCS.set_pressure_1channel(5)
    #MFCS.setall_zeropressure()
    #MFCS.set_purge_on
    #read_pressure_channel()
    
          
    print("MODEL:", MFCS.get_serial())