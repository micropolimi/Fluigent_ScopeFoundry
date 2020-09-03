from ScopeFoundry import HardwareComponent
import time
from FluigentHardwareUpdated.PumpDevice import MFCSDevice


class MFCSHardware(HardwareComponent):
    
    name = "MFCSHardware"
    
    def setup(self):
        
        self.saved_pressures = [0, 0, 0, 0]
        
        self.pump = self.add_logged_quantity('pump', dtype = str, si=False, ro=1,
                                            initial = "no pump") 
        self.set_pressure_1 = self.add_logged_quantity('set_pressure_1' , dtype=float, si=False, ro = 0, 
                                                spinbox_step = 0.0001,spinbox_decimals = 4, initial = 0.0001,
                                                unit = 'mbar', vmin = 0, vmax = 25)
        self.read_pressure_1 = self.add_logged_quantity('read_pressure_1', dtype = float, si = False, ro = 1,
                                                       spinbox_decimals = 4 ,initial = 0, unit = 'mbar')
        self.set_pressure_2 = self.add_logged_quantity('set_pressure_2', dtype=float, si=False, ro = 0, 
                                                spinbox_step = 0.0001,spinbox_decimals = 4, initial = 0.0001,
                                                unit = 'mbar', vmin = 0, vmax = 25)
        self.read_pressure_2 = self.add_logged_quantity('read_pressure_2', dtype = float, si = False, ro = 1,
                                                     initial = 0, unit = 'mbar')
        self.set_pressure_3 = self.add_logged_quantity('set_pressure_3' , dtype=float, si=False, ro = 0, 
                                                spinbox_step = 0.0001,spinbox_decimals = 4, initial = 0.0001,
                                                unit = 'mbar', vmin = 0, vmax = 1000)
        self.read_pressure_3 = self.add_logged_quantity('read_pressure_3', dtype = float, si = False, ro = 1,
                                                       spinbox_decimals = 4 ,initial = 0, unit = 'mbar')
        self.set_pressure_4 = self.add_logged_quantity('set_pressure_4', dtype=float, si=False, ro = 0, 
                                                spinbox_step = 0.0001,spinbox_decimals = 4, initial = 0.0001,
                                                unit = 'mbar', vmin = 0, vmax = 1000)
        self.read_pressure_4 = self.add_logged_quantity('read_pressure_4', dtype = float, si = False, ro = 1,
                                                        spinbox_decimals = 4 ,initial = 0, unit = 'mbar')
        self.save_pressure_1 = self.add_logged_quantity('save_pressure_1', dtype = bool, si = False, ro = 0, 
                                                       initial = False, reread_from_hardware_after_write = True)
        self.save_pressure_2 = self.add_logged_quantity('save_pressure_2', dtype = bool, si = False, ro = 0, 
                                                       initial = False, reread_from_hardware_after_write = True)
        self.save_pressure_3 = self.add_logged_quantity('save_pressure_3', dtype = bool, si = False, ro = 0, 
                                                       initial = False, reread_from_hardware_after_write = True)
        self.save_pressure_4 = self.add_logged_quantity('save_pressure_4', dtype = bool, si = False, ro = 0, 
                                                       initial = False, reread_from_hardware_after_write = True)

        self.set_saved_pressure = self.add_logged_quantity('set_saved_pressure', dtype = bool, si = False, ro = 0, 
                                                       initial = False)
        #self.purge = self.add_logged_quantity('purge', dtype=bool, si=False, ro=0, 
        #                                     initial = False, reread_from_hardware_after_write = True)
        #self.set_zeropressure = self.add_logged_quantity('reset pressure', dtype=bool, si=False, ro=0, 
                                            # initial = False)
        
        #self.add_operation("set zero pressure",self.setall_zeropressure)
        #self.add_operation("save pressure", self.save_pressure)
        #self.add_operation("apply saved pressure", self.apply_saved_pressure)
        
    def connect(self):
        """
        The initial connection does not update the value in the device,
        since there is no set_from_hardware function, so the device has
        as initial values the values that we initialize in the HamamatsuDevice
        class. I'm struggling on how I can change this. There must be some function in
        ScopeFoundry
        """

        self.MFCS = MFCSDevice(hardware = self)
        self.pump.hardware_read_func = self.MFCS.get_serial
    
        
        self.read_pressure_1.hardware_read_func = self.MFCS.read_pressure_channel_1
        self.set_pressure_1.hardware_set_func = self.MFCS.set_pressure_channel_1
        self.save_pressure_1.hardware_set_func = self.saving_pressure_1
        #self.set_saved_pressure_1.hardware_set_func = self.setting_saved_pressure_1
        
        self.read_pressure_2.hardware_read_func = self.MFCS.read_pressure_channel_2
        self.set_pressure_2.hardware_set_func = self.MFCS.set_pressure_channel_2
        self.save_pressure_2.hardware_set_func = self.saving_pressure_2
        #self.set_saved_pressure_2.hardware_set_func = self.setting_saved_pressure_2
        
        self.read_pressure_3.hardware_read_func = self.MFCS.read_pressure_channel_3
        self.set_pressure_3.hardware_set_func = self.MFCS.set_pressure_channel_3
        self.save_pressure_3.hardware_set_func = self.saving_pressure_3
#         self.set_saved_pressure_1.hardware_set_func = self.setting_saved_pressure_1

        self.read_pressure_4.hardware_read_func = self.MFCS.read_pressure_channel_4
        self.set_pressure_4.hardware_set_func = self.MFCS.set_pressure_channel_4
        self.save_pressure_4.hardware_set_func = self.saving_pressure_4
        
        self.set_saved_pressure.hardware_set_func = self.setting_saved_pressure

        self.save_pressure_1.hardware_read_func = self.read_save_pressure_1
        self.save_pressure_2.hardware_read_func = self.read_save_pressure_2
        self.save_pressure_3.hardware_read_func = self.read_save_pressure_3
        self.save_pressure_4.hardware_read_func = self.read_save_pressure_4
        
        time.sleep(2) #necessary for establishing the communication
        
 
        self.read_from_hardware() #read from hardware at connection

        
        
    def setall_zeropressure (self):
        
        self.MFCS.setall_zeropressure()
    
    def setting_saved_pressure (self, flag):
        
        if flag:
            
            self.settings["set_pressure_1"] = self.saved_pressures[0]
            self.settings["set_pressure_2"] = self.saved_pressures[1]
            self.settings["set_pressure_3"] = self.saved_pressures[2]
            self.settings["set_pressure_4"] = self.saved_pressures[3]
            
            
    def saving_pressure_1(self, flag):
        
        if flag:
            
            self.saved_pressures[0] = self.set_pressure_1.val


    def saving_pressure_2(self, flag):
        
        if flag:
            
            self.saved_pressures[1] = self.set_pressure_2.val
    
    def saving_pressure_3(self, flag):
        
        if flag:
            
            self.saved_pressures[2] = self.set_pressure_3.val
    

    def saving_pressure_4(self, flag):
        
        if flag:
            
            self.saved_pressures[3] = self.set_pressure_4.val

    def read_save_pressure_1(self):
        
        return False
    
    def read_save_pressure_2(self):
        
        return False
    
    def read_save_pressure_3(self):
        
        return False
    
    
    def read_save_pressure_4(self):
        
        return False
                
    def disconnect(self):

        
        if hasattr(self, 'MFCS'):
            self.MFCS.close()
#             error_uninit = self.hamamatsu.dcam.dcamapi_uninit()
#             if (error_uninit != DCAMERR_NOERROR):
#                 raise DCAMException("DCAM uninitialization failed with error code " + str(error_uninit))    
            del self.MFCS
            
        for lq in self.settings.as_list():
            lq.hardware_read_func = None
            lq.hardware_set_func = None
            
   