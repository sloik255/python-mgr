from PyQt5.QtWidgets import QDialog
from PyQt5 import uic

import preprocessing as prep
import akwizycja as akw
import ekstrakcja
import detekcja
import cv2, threading
import numpy as np

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
        pass
    def clearAll(self):
        pass


##############################################################################
''' SETTINGSWINDOW section'''
##############################################################################

class SettingsWindow(QDialog):
    def __init__(self):
        super(SettingsWindow, self).__init__()
        uic.loadUi('ui/settings.ui', self)
        self.setWindowTitle("Settings")
        self.pb_run.clicked.connect(self.slot_RUNCAMERA)
        
        self.pb_refresh.clicked.connect(self.slot_REFRESH)
        self.pb_polacz.clicked.connect(self.slot_KALIBRATOR_POLACZ)
        self.pb_rozlacz.clicked.connect(self.slot_KALIBRATOR_ROZLACZ)
        self.pb_kalcheck.clicked.connect(self.slot_KALCHECK)
        self.pb_kalibruj.clicked.connect(self.slot_KALIBRUJ)
        
        self.pb_autoroi.clicked.connect(self.slot_AUTO_ROI)
        self.pb_roireset.clicked.connect(self.slot_RESET_ROI)
        self.sb_l.valueChanged.connect(self.slot_ROI_UPDATE_L)
        self.sb_r.valueChanged.connect(self.slot_ROI_UPDATE_R)
        self.sb_t.valueChanged.connect(self.slot_ROI_UPDATE_T)
        self.sb_b.valueChanged.connect(self.slot_ROI_UPDATE_B)
        
        self.pb_pomiarW.clicked.connect(self.slot_pomiarW)
        self.pb_sprawdzW.clicked.connect(self.slot_sprawdzW)
    def slot_pomiarW(self):
        measureW.show()
        pass
    def slot_sprawdzW(self):
        ckeckW.show()
        pass
    def slot_RUNCAMERA(self):
        var.cam_number = self.spinBox.value()
        cp.forcedClose()
        print "Camera started: " + str(var.cam_number)
        cp.setCamera(run=True)
    def slot_KALIBRATOR_POLACZ(self):
        i = self.comboBox_visa.currentIndex()
        n = str(var.resources_list[0][i])
        if (vi.setResource(name=n) and vi.connected()):
            self.lineEdit_visa.setText("polaczono")
        pass
    def slot_KALIBRATOR_ROZLACZ(self):
        vi.clearResource()
        if (not vi.connected()):
            self.lineEdit_visa.setText("rozlaczono")
        pass
    def slot_REFRESH(self):
        self.comboBox_visa.clear()
        self.comboBox_visa.addItem("czekaj...")
        vi.getResourcesList()
        
        self.comboBox_visa.clear()
        for i in range (0, len(var.resources_list[1])):
            self.comboBox_visa.addItem(var.resources_list[1][i])
        pass
    def slot_KALCHECK(self):
        if (vi.connected()):
            self.lineEdit_visa.setText("urzadzenie odpowiada")
        else:
            self.lineEdit_visa.setText("brak polaczenia")
            self.slot_KALIBRATOR_ROZLACZ()
        pass
    def slot_KALIBRUJ(self):
        cp.setMeasurementParams(True)
        self.KALIBRUJ()
        cp.setMeasurementParams()
        pass
    def slot_AUTO_ROI(self):
        var.ROI_vals = akw.getPoints(var.raw_frame)
        self.UPDATE_UI()
        pass
    def slot_RESET_ROI(self):
        self.RESET_ROI()
    def slot_ROI_UPDATE_L(self):
        self.sb_r.setMinimum(self.sb_l.value()+130)
        var.ROI_vals = ( self.sb_l.value(), var.ROI_vals[1], var.ROI_vals[2], var.ROI_vals[3] )
    def slot_ROI_UPDATE_R(self):
        self.sb_r.setMinimum(self.sb_l.value()+130)
        var.ROI_vals = ( var.ROI_vals[0], self.sb_r.value(), var.ROI_vals[2], var.ROI_vals[3] )
    def slot_ROI_UPDATE_T(self):
        self.sb_b.setMinimum(self.sb_t.value()+70)
        var.ROI_vals = ( var.ROI_vals[0], var.ROI_vals[1], self.sb_t.value(), var.ROI_vals[3] )
    def slot_ROI_UPDATE_B(self):
        self.sb_b.setMinimum(self.sb_t.value()+70)
        var.ROI_vals = ( var.ROI_vals[0], var.ROI_vals[1], var.ROI_vals[2], self.sb_b.value() )
    def UPDATE_UI(self):
        settingsW.sb_l.setValue(var.ROI_vals[0])
        settingsW.sb_r.setValue(var.ROI_vals[1])
        settingsW.sb_t.setValue(var.ROI_vals[2])
        settingsW.sb_b.setValue(var.ROI_vals[3])
    def KALIBRUJ(self):
        print var.angle
        pass
    def RESET_ROI(self):
        var.ROI_vals = (0,0,0,0)
        try:
            height, width, _ = var.raw_frame.shape
        except:
            print "cannot get raw_frame"
            height = 100
            width = 100
        var.ROI_vals = (0, width, 0, height)

        self.UPDATE_UI()
    def getAnglesLim(self):
        a = (self.min_spin.value(), self.max_spin.value())
        return a
    def closeEvent(self, event):
        cp.forcedClose()
        pass
    

##############################################################################
''' MEASUREWINDOW section'''
##############################################################################

class MeasureWindow(QDialog):
    def __init__(self):
        super(MeasureWindow, self).__init__()
        uic.loadUi('ui/meas.ui', self)
        self.setWindowTitle("Measurement")
        self.unit_combo.addItems(("uV", "mV", " V", "kV"))
        
        self.pb_czysc.clicked.connect(self.slot_CZYSCHISTORIE)
        self.pb_ciagly.clicked.connect(self.slot_POM_CIAGLY)
        self.pb_pauza.clicked.connect(self.slot_PAUZA)
        self.pb_series_start.clicked.connect(self.slot_SERIES_START)
        self.pb_series_stop.clicked.connect(self.slot_SERIES_STOP)
        
        self.pb_pauza.setEnabled(False)
        self.pb_series_stop.setEnabled(False)

    def slot_CZYSCHISTORIE(self):
        self.plainTextEdit.clear()
    def slot_POM_CIAGLY(self):
        self.pb_ciagly.setEnabled(False)
        self.pb_pauza.setEnabled(True)
        self.plainTextEdit.appendPlainText("Pomiar ciagly")
        self.startMeasurement(run=True)
    def slot_PAUZA(self):
        self.plainTextEdit.appendPlainText("Pauza")
        self.stopMeasurement()
        self.pb_ciagly.setEnabled(True)
    def slot_SERIES_START(self):
        self.pb_series_start.setEnabled(False)
        self.pb_series_stop.setEnabled(True)
        self.plainTextEdit.appendPlainText("Start serii")
        t = self.sb_interval.value()
        self.startMeasurement(run=True,series_interval_s=t)
    def slot_SERIES_STOP(self):
        self.plainTextEdit.appendPlainText("Seria stop")
        self.stopMeasurement()
        self.pb_series_start.setEnabled(True)       
    def setValue(self, value = -0.0):
        self.sign_label.setText("-")
        if (value >= 0):
            self.sign_label.setText(" ")
        txt = "%.3f" % value
        self.value_label.setText(txt)
        self.unit_label.setText(self.unit_combo.currentText())
        
    def getRange(self):
        return self.range_spinBox.value()

    def startMeasurement(self, run=False, series_interval_s=0):
        cp.setMeasurementParams(run, series_interval_s)
    
    def stopMeasurement(self):
        cp.setMeasurementParams()
        
    def measurement(self):
        return 0
    def measurement2(self):
        return 0

##############################################################################
''' CheckOutWindow section'''
##############################################################################

from PyQt5.QtWidgets import QMessageBox

class CheckWindow(QDialog):
    def __init__(self):
        super(CheckWindow, self).__init__()
        uic.loadUi('ui/check.ui', self)
        self.setWindowTitle("Check your meter")
        self.type_combo.addItems( ("voltage DC", "voltage AC (sin)") )
        self.type_combo.currentIndexChanged.connect(self.slot_typeIntexChanged)
        self.freq_spin.valueChanged.connect(self.slot_typeIntexChanged)
        
        self.zakresy_pb.clicked.connect(self.slot_startRangeCapture)
        self.range_spin.valueChanged.connect(self.slot_spinsChanged)
        self.angle_min_spin.valueChanged.connect(self.slot_spinsChanged)
        self.angle_max_spin.valueChanged.connect(self.slot_spinsChanged)
        
        self.check_pb.clicked.connect(self.slot_checkClicked)

    def slot_typeIntexChanged(self):
        if ( self.type_combo.currentIndex() == 0 ):
            self.freq_box.setEnabled(False)
            vi.setFunc("DC")
            pass
        elif ( self.type_combo.currentIndex() == 1 ):
            self.freq_box.setEnabled(True)
            vi.setFunc("SIN", self.freq_spin.value())
            pass
        else:
            pass
    def slot_startRangeCapture(self):
        var.angle_lim = (45, 135)
        self.angle_min_spin.setValue(45)
        self.angle_max_spin.setValue(135)
        var.value_range = 5
        self.range_spin.setValue(5)
        pass
    def slot_checkClicked(self):
        a = 4.3 #vi.findVoltageForAngle(find_angle=90, max_iter=100)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
       
        msg.setText("Zweryfikuj poprawnosc ZGRUBNEGO wskazania srodka skali.")
        msg.setInformativeText("Jesli wskazanie jest poprawne kliknij OK, w innym przypadku ustaw recznie wskaznik na srodku skali i wcisnij CANCEL.")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()
        if (retval == 1024):
            val = np.int(a*2+0.5)
            if(val > 9)
                val = np.int(a*2/10+0.5)*10
            self.range_spin.setValue( val )
        else:
            while ( not var.passed ):
                pass
            a = var.angle
            val = np.int(a*2+0.5)
            if(val > 9)
                val = np.int(a*2/10+0.5)*10
            self.range_spin.setValue( val )
            
        #a =  vi.findAngleForVoltage(find_voltage=0, max_iter=100) 
        #self.angle_min_spin.setValue( a )
        pass
    def slot_spinsChanged(self):
        var.value_range = self.range_spin.value()
        var.angle_lim = (self.angle_min_spin.value(), self.angle_max_spin.value())
            

##############################################################################
''' CAMERA SIGNAL PROCESSING section'''
##############################################################################
    
'''                         '''
class CameraProcessing(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._run = False
        self._runMeas = False
        self._series_interval_ms = 0
        print "Konfiguracja watku frameProcessing zakonczona."
        
    def setMeasurementParams(self, runMeas=False, series_interval_s=0):
        if (self._run):
            self._runMeas = runMeas
            self._series_interval_ms = np.float32(series_interval_s)*1000
            print "Watek frameProcessing ponownie skonfigurowano!"
        pass
        
    def setCamera(self, run=False):
        self._run = run
        if (run):
            self.run()
    
    def forcedClose(self):
        try:
            var.video.release()
            cv2.destroyWindow("live")
        except:
            pass
        
    def run(self):
        if (self._run):
            cv2.namedWindow("live", cv2.WINDOW_AUTOSIZE)
            var.video = cv2.VideoCapture(var.cam_number)
            
            if var.video.isOpened():
                var.vid_exists, var.raw_frame = var.video.read()
                print "video opened"
                settingsW.RESET_ROI()
                
            else:
                var.vid_exists = False
                cv2.destroyWindow("live")
                print "analyze stopped by hardware"
                #self.pushButton_3.setEnabled(True)
                
            while (var.vid_exists):
                var.vid_exists, var.raw_frame = var.video.read()
                
                var.frame = var.raw_frame

                var.frame = cam_cropFrame(var.frame)
                ret, var.frame = cam_preprocessing(var.frame)
                if (not ret):
                    var.video.release()
                    cv2.destroyWindow("live")
                    print "analyze error"
                    break
                var.frame = cam_ekstrakcja(var.frame)
                    
                
                if (np.size(var.frame, axis=1)==0 or np.size(var.frame, axis=0)==0):
                    var.video.release()
                    cv2.destroyWindow("live")
                    print "analyze stopped by size"
                    break
                
                cv2.imshow("live", var.frame) 
                
                if(self._runMeas):
                    cv2.waitKey(100)
                    temp_counter = self._series_interval_ms - 100
                    while (temp_counter>0):
                        cv2.waitKey(100)
                        temp_counter -= 100
                    pass
                    
                    #hough from frame
                    var.passed = False
                    #measureW.setValue()
                    
                    var.angle = detekcja.detection(var.frame)
                    
                    var.value_range = measureW.getRange()
                    var.angle_lim = settingsW.getAnglesLim()
                    
                    var.value = detekcja.calculateValue(var.angle, var.angle_lim, var.value_range)
                        
                    if ( (var.value >= 0) and (var.angle >= 0) ):
                        var.passed = True
                        measureW.setValue(var.value)
                    
                    print "angle: ", var.angle, "  measured value: ", var.value
                    
                else:
                    key = cv2.waitKey(100)
                    if (key == 27):
                        cv2.destroyWindow("live")
                        var.video.release()
                        print "analyze stopped"
                        self._run = False
                        #self.pushButton_3.setEnabled(True)
                        break
        pass
            
    
def cam_cropFrame(frame):
    t = frame[var.ROI_vals[2]:var.ROI_vals[3],var.ROI_vals[0]:var.ROI_vals[1],:]
    return t

def cam_preprocessing(frame):
    return prep.preprocessing(frame)

def cam_ekstrakcja(frame):
    return ekstrakcja.ekstrakcja(frame)


##############################################################################
''' VISA CLASS section'''
##############################################################################
    
'''                         '''
import visa, time, threading, numpy

class VisaInstrument(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.rm = visa.ResourceManager()
        self.instr_list = self.rm.list_resources()
        self.instr_num = len(self.instr_list)
        self.my_instrument = None
        
        
        print "Konfiguracja watku VisaInstrument zakonczona."
        
    def getResourcesList(self):
        self.instr_list = self.rm.list_resources()   
        self.instr_num = len(self.instr_list)
        instrs = ()
        names = ()
        for i in range(0, self.instr_num):
            try:
                s = self.instr_list[i]
                names = names + (s,)
                my_instrument = self.rm.open_resource(s)
                s = my_instrument.query('*IDN?')
                instrs = instrs + (s,)
                my_instrument.close()
            except:
                instrs = instrs + ("instrument invalid",)
                
        var.resources_list = (names, instrs)
    
    def setResource(self, name="empty"):
        ret = False
        if (not (self.my_instrument is None) ):
            try:
                self.my_instrument.close()
            except:
                print "closing error"
        try:
            self.my_instrument = self.rm.open_resource(name)
            ret = True
        except:
            print "opening error"
            ret = False

        return ret
                
    def clearResource(self):
        if not (self.my_instrument is None ):
            self.my_instrument.close()
        self.my_instrument = None
        return True
        
    def connected(self):
        connected = False
        try:
            connected = True
            self.my_instrument.write()
            print self.my_instrument.read()
        except:
            try:
                self.my_instrument.write(":SYST:ERR?") 
                print self.my_instrument.read()
            except:
                connected = False
        return connected
    
    def write(self, text="*IDN?"):
        ret = True
        try:
            self.my_instrument.write(text)
            ret =  True
        except:
            ret = False
            
        return ret
    
    def setFunc(self, func="DC/SIN/TRI/RAMP/SQU", frequency_Hz=0):
        message = "SOUR1:FUNC " + func
        self.write(text=message)
    
    def func(self):
        self.write(text="SOUR1:FUNC?")
        return self.my_instrument.read()
        
    def setFrequency(self, FREQ_Hz=100):
        message = "SOUR1:FREQ " + str(FREQ_Hz)
        self.write(message)
        
    def frequency(self):
        self.write("SOUR1:FREQ?")
        return self.my_instrument.read()
        
    def setDcVoltage(self, OFFS_mV=1000):
        message = "SOUR1:VOLT:OFFS " + str(OFFS_mV) + "mV"
        self.write(message)
    
    def dcVoltage(self):
        self.write("SOUR1:VOLT:OFFS?")
        return self.my_instrument.read()
        
    def setAmplitude(self, AMPL_mV=1000):
        message = "SOUR1:VOLT:AMPL " + str(AMPL_mV) + "mV"
        self.write(message)
        
    def amplitude(self):
        self.write("SOUR1:VOLT:AMPL?")
        return self.my_instrument.read()
        
    def setOutputON(self):
        message = "OUTP1 1"
        self.write(message)
    
    def setOutputOFF(self):
        message = "OUTP1 0"
        self.write(message)
        
    def outputState(self):
        self.write("OUTP1?")
        return self.my_instrument.read()
        
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
                
            self.setDcVoltage(OFFS_mV = numpy.around(d_volt))
            time.sleep(1)
        pass
        
        if (i == max_iter):
            return (False, 0)
        else:
            return (True, var.angle)
        
        
        
    def run(self):
        connected = False
        while (True):
            
            if (connected == False):
                time.sleep(2)
                
            try:
                connected = True
                print self.my_instrument.read()
            except:
                try:
                    self.my_instrument.write(":SYST:ERR?") 
                    print self.my_instrument.read()
                except:
                    connected = False
        pass
            
 
##############################################################################
''' MAIN section'''
##############################################################################


from PyQt5.QtWidgets import QApplication
import sys
   
if __name__ == '__main__':
    
    var = GlobalVariables()

    cp = CameraProcessing()
    cp.setMeasurementParams()
    cp.start()
    
    vi = VisaInstrument()
    vi.getResourcesList()
    
      
    app = QApplication(sys.argv)
    
    settingsW = SettingsWindow()
    
    measureW = MeasureWindow()
    measureW.setWindowModality(1)
    
    ckeckW = CheckWindow()
    ckeckW.setWindowModality(1)
    
    settingsW.show()
    
    

    app.exec_()  
    