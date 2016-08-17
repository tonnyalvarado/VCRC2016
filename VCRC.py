import mraa
import time
import pyupm_i2clcd as lcd
import signal
import sys
import dweepy

def interruptHandler(signal, frame):
	sys.exit(0)

def sensorPresion():
	v = leerSensor(0)
	li = 0.0
	lf = 40.0
	return [v,li,lf] 

def sensorFlujo():
    v = leerSensor(1)
    li = 0.05
    lf = 10.0
    return [v,li,lf]

def sensorNivel():
    v = leerSensor(2)
    li = 4.0
    lf = 168.0
    return [v, li,lf]

def calculo(li):
    resultado = (((li[0]*2**12/5.0)*(100.0/2**12))/100)*(li[2]-li[1])
    return resultado + li[1]
    
def leerSensor(n):
    try:
        pinsensor = mraa.Aio(n)
        pinsensor.setBit(12)
        
        valorsensor = pinsensor.read()
        return valorsensor/819.0
    except:
        print "Error en el conversor ADC"

if __name__ == '__main__':
    signal.signal(signal.SIGINT, interruptHandler)
    myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)
    colorR = 0;
    colorG = 255;
    colorB = 0;
    sensor = 0
    presion=0
    flujo=0
    nivel=0   
    
    myLcd.setColor(colorR,colorG,colorB)
    myLcd.setCursor(0,0)
    while True:      
	  myLcd.clear()
	  presion = calculo(sensorPresion())
	  flujo = calculo(sensorFlujo())
	  nivel = calculo(sensorNivel())
          if sensor==0:
              myLcd.write('Presion: %.6f'%presion)
              time.sleep(2)
          elif sensor == 1:
              myLcd.write('Flujo: %.6f'%flujo)
              time.sleep(2)
          else:
              myLcd.write('Nivel: %.6f'%nivel)
              time.sleep(2)
	  if sensor < 2:
		sensor+=1
	  else:
		sensor = 0
          datos = {"presion":presion , "flujo":flujo,"nivel":nivel}
          dweepy.dweet_for("VCRCTonnyAlvarado",datos)
