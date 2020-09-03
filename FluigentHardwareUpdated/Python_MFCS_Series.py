#!/#!/usr/bin/env python

#******************************************************************************
#software          : Python_MFCS_Series
#version          : 18.0.0
#date               : 10-2018
#******************************************************************************

from __future__ import print_function    # Used for "print" function compatibility between Python 2.x and 3.x versions
import platform                            # Library used for x64 or x86 detection
import time                                # Time library, use of sleep function
import ctypes                            # Used for variable definition types
from ctypes import *                    # Used to load dynamic linked libraries


# This function uses "raw_input" for Python 2.x versions and "input" for Python 3.x versions
def myinput(prompt):
    try:
        return raw_input(prompt)
    except NameError:
        return input(prompt)

# Main function executed when this file is called
if __name__ == "__main__":

    # Variable types definition 
    mfcsHandle = ctypes.c_ulonglong(0)    # mfcsHandle is the session handler used by all functions after initialization
    mySerial = c_ushort(0)                # device serial number
    C_error = c_char()                    # error returned code when calling dll functions
    B_OK = bool(False)
    purge_status = c_byte(0)
    
    pressure_setpoint = c_float(20)    # Pressure set in mbar
    pressure_read = c_float(0)
    timeStamp = c_ushort(0)
    
    try:  
        # Load dll into memory
        # If using 64bit python version please load mfcs_c_64.dll instead
        lib_mfcs = ctypes.WinDLL('mfcs_c_64.dll')
        
        # Initialization function prototype
        # Functions can also be directly called using "lib_mfcs" 
        mfcsInit = lib_mfcs.mfcs_initialisation
        mfcsInit.restype = c_ulonglong
        mfcsInit.argtypes = [c_ushort]
        
        # Initialize the first MFCS in Windows enumeration list 
        mfcsHandle = mfcsInit(0)
        
        # Print status on MFCS initialization
        if (mfcsHandle != 0):
            print ('MFCS initialized')
        else:
            print ('Error on MFCS initialization. Please check that device is plugged in.')
    
        C_error=lib_mfcs.mfcs_set_alpha(c_ulonglong(mfcsHandle),0,5);   # Sends channel configuration
        time.sleep(3)
        # Set pressure and check
        C_error = lib_mfcs.mfcs_set_auto(c_ulonglong(mfcsHandle),1,pressure_setpoint)
        # Wait for pressure to set
        time.sleep(3)
        # Read channel pressure
        C_error = lib_mfcs.mfcs_read_chan(c_ulonglong(mfcsHandle),1,byref(pressure_read), byref(timeStamp))
        print ('Pressure set at ', pressure_setpoint.value, ' mbar, read : ', pressure_read.value, ' mbar')
        
        # Set pressure to 0 mbar before exit
        C_error = lib_mfcs.mfcs_set_auto(c_ulonglong(mfcsHandle),0,c_float(0))
            
        # Close communication port 
        B_OK = lib_mfcs.mfcs_close(c_ulonglong(mfcsHandle));
        if (B_OK == True):
            print ('USB connection closed')
        if (B_OK == False):
            print ('Failed to close USB connection')
            
        # Release the DLL
        ctypes.windll.kernel32.FreeLibrary(lib_mfcs._handle)
        del lib_mfcs
        print ('MFCS library unloaded')
            
        # Exit application 
        myinput("Press ENTER to exit application")

    except Exception as e:
        print (e)
