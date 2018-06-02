##############################################################################
'''GLOBAL VARIABLES'''
##############################################################################

class GlobalVariables:
    def __init__(self):
        self.cam_number = 0
        self.ROI_vals = (0,0,0,0)
        self.angle_lim = (45,135)
        self.value_range = 5
        self.video = 0
        self.vid_exists = 0
        self.raw_frame = 0
        self.frame = 0
        self.resources_list = ((0,),(0,))
        self.value = -1
        self.angle = 0
        self.passed = False
        self.det_err = 0
        pass
    def clearAll(self):
        pass

##############################################################################
''' INMEL 1000 CLASS section'''
##############################################################################
    
'''                         '''
import serial, time, threading, numpy

class InmelClass(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.my_instrument = None
        
        self.ser_port = serial.Serial()
        self.ser_port.port='COM1'
        self.ser_port.baudrate=19200
        self.ser_port.parity=serial.PARITY_NONE
        self.ser_port.stopbits=serial.STOPBITS_ONE
        self.ser_port.bytesize=serial.EIGHTBITS
        self.ser_port.timeout = 5
        
        print "Konfiguracja watku InmelClass zakonczona."
        
    def getResourcesList(self):
        instr_num = 10
        instrs = ()
        names = ()
        for i in range(0, instr_num):
            try:
                s = 'COM'+ str(i)
                names = names + (s,)
                self.ser_port.port = s
                self.ser_port.open()
                if (self.ser_port.is_open == True):
                    self.ser_port.write(' ID?;')
                    line = self.ser_port.readline()
                    if (len(line) == 0):
                        instrs = instrs + ("not responding",)
                    else:
                        instrs = instrs + (line,)
                    self.ser_port.close()
                else:
                    instrs = instrs + ("nothing connected",)
            except:
                instrs = instrs + ("nothing connected",)
                
        var.resources_list = (names, instrs)
    
    def setResource(self, name="empty"):
        ret = False
        if (not (self.my_instrument is None) ):
            try:
                self.my_instrument = None
                self.ser_port.close()
            except:
                print "closing error"
        try:
            self.ser_port.port = name
            self.ser_port.open()
            self.ser_port.write(' ID?;')
            line = self.ser_port.readline()
            if (len(line) == 0):
                print "not responding"
                ret = False
            else:
                self.my_instrument = name
                ret = True
        except:
            self.ser_port.close()
            self.my_instrument = None
            print "opening error"
            ret = False

        return ret
                
    def clearResource(self):
        if not (self.my_instrument is None ):
            self.ser_port.close()
        self.my_instrument = None
        return True
        
    def connected(self):
        try:
            self.ser_port.write(' ID?;')
            line = self.ser_port.readline()
            if (len(line) == 0):
                line = 'not responding'
                print line
                return False
            return True
        except:
            self.clearResource()
            return False
                
    def write(self, text="ID?"):
        ret = True
        try:
            self.ser_port.write(text)
            ret =  True
        except:
            self.clearResource()
            ret = False
            
        return ret
    
    def setFunc(self, func="DC/SIN", frequency_Hz=0):
        if (func == "SIN"):
            message = "RANG:10;SET F:" + str(frequency_Hz) + ";"
        elif (func == "DC"):
            message = "RANG:1;"
            self.write(text=message)
    
    def func(self):
        self.write(text="RANG?")
        
    def setFrequency(self, FREQ_Hz=100):
        message = "SET F:" + str(FREQ_Hz) + ";"
        self.write(message)
        
    def frequency(self):
        self.write("SET F?;")
        
    def setDcVoltage(self, OFFS_mV=1000):
        #message = "SOUR1:VOLT:OFFS " + str(OFFS_mV) + "mV"
        #self.write(message)
        if (OFFS_mV <= 200):
            self.write("RANG:1;")
            self.write("SET U[mV]:" + str(OFFS_mV) + ";")
            self.setOutputON()
        elif (OFFS_mV <= 2000):
            self.write("RANG:2;")
            self.write("SET U[V]:" + str(OFFS_mV/1000.0) + ";")
            self.setOutputON()
        elif (OFFS_mV <= 20000):
            self.write("RANG:3;")
            self.write("SET U[V]:" + str(OFFS_mV/1000.0) + ";")
            self.setOutputON()
        elif (OFFS_mV <= 200000):
            self.write("RANG:4;")
            self.write("SET U[V]:" + str(OFFS_mV/1000.0) + ";") 
            self.setOutputON()

    
    def dcVoltage(self):
        self.write("SET U?;   ")
        
    def setAmplitude(self, AMPL_mV=1000):
        if (AMPL_mV <= 200):
            self.write("RANG:10;")
            self.write("SET U[mV]:" + str(AMPL_mV) + ";   ")
        elif (AMPL_mV <= 2000):
            self.write("RANG:11;")
            self.write("SET U[V]:" + str(AMPL_mV/1000.0) + ";   ")
        elif (AMPL_mV <= 20000):
            self.write("RANG:12;")
            self.write("SET U[V]:" + str(AMPL_mV/1000.0) + ";   ")
        elif (AMPL_mV <= 200000):
            self.write("RANG:13;")
            self.write("SET U[V]:" + str(AMPL_mV/1000.0) + ";   ")   
        
    def amplitude(self): #OK
        self.write("SET U?;")
        
    def setOutputON(self): #OK
        self.write("OPER;")
    
    def setOutputOFF(self): #OK
        self.write("STDBY;")
        
    def outputState(self): #OK
        self.write("OPER?;")
        
    def findVoltageForAngle(self, find_angle=60, max_iter=100):
        now_angle= var.angle-find_angle
        
        gen_v = 1.0
        self.setDcVoltage(OFFS_mV = 1)
        
        d_volt = 1.0
        last_angle= var.angle-find_angle
        
        i = 0
        
        while ( (numpy.fabs(now_angle)>2) and (i < max_iter) ):
            i = i+1

            last_angle = now_angle
            print "angle: ", var.angle
            now_angle = var.angle-find_angle
            
            delta_angle = numpy.fabs(now_angle-last_angle)
            
            if (delta_angle < 5):
                d_volt = d_volt *2
            elif (delta_angle > 10):
                d_volt = d_volt /2
            else:
                d_volt = d_volt
                
            if (now_angle < 0):
                gen_v = gen_v + d_volt
            else:
                gen_v = gen_v - d_volt
                
            self.setDcVoltage(OFFS_mV = numpy.around(gen_v))
            time.sleep(5)
        pass
        
        if (i == max_iter):
            return (False, 0)
        else:
            return (True, gen_v)
        pass
    
    def findAngleForVoltage(self, find_voltage):
        self.setDcVoltage(OFFS_mV = find_voltage*1000)
        time.sleep(1)
        return (True, var.angle)

    def run(self):
        while (True):
            
            if (self.ser_port.is_open):  
                try:
                    line = self.ser_port.readline()
                    if (len(line) == 0):
                        pass
                    else:
                        line = line.translate(None, '\n\r')
                        print line
                except:
                    self.clearResource()
            else:
                time.sleep(2)
                        
        pass
    
var = GlobalVariables()
inmel = InmelClass()
inmel.getResourcesList()
inmel.start()
print var.resources_list
inmel.setResource(name="COM8")
print 'connected', inmel.connected()
