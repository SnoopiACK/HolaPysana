
import numpy as np
import pyaudio

import matplotlib.pyplot as plt
from matplotlib.widgets import Button

class SpectrumAnalyzer:
    FORMAT = pyaudio.paFloat32
    CHANNELS = 1
    RATE = int(16000/5)
    CHUNK = 512
    START = 0
    N = 512

    wave_x = 0
    wave_y = 0
    spec_x = 0
    spec_y = 0
    data = []
    
    frec697=112
    frec770=123
    frec852=137
    frec941=151
    
    frec1209=193
    frec1336=214
    frec1477=237
    
    teclado = np.matrix('1 2 3; 4 5 6;7 8 9; 77 0 99')
    
    numero = ""  #Se va ir guardando el numero en string
    
    anterior = 40
    
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(format = self.FORMAT,
            channels = self.CHANNELS, 
            rate = self.RATE, 
            input = True,
            output = False,
            frames_per_buffer = self.CHUNK)
        # Main loop
        
        
        self.loop()

    def loop(self):
        try:
            while True :
                self.data = self.audioinput()
                self.fft()
                self.graphplot()

        except KeyboardInterrupt:
            self.pa.close()

        print("End...")

    def audioinput(self):
        ret = self.stream.read(self.CHUNK)
        ret = np.fromstring(ret, np.float32)
        return ret

    def fft(self):
        self.wave_x = range(self.START, self.START + self.N)
        self.wave_y = self.data[self.START:self.START + self.N]
        self.spec_x = np.fft.fftfreq(self.N, d = 1.0 / self.RATE)  
        y = np.fft.fft(self.data[self.START:self.START + self.N])    
        self.spec_y = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in y]

    def graphplot(self):
        plt.clf()
        # wave
        plt.subplot(311)
        plt.plot(self.wave_x, self.wave_y*40)
        plt.axis([self.START, self.START + self.N, -0.5, 0.5])
        plt.xlabel("time [sample]")
        plt.ylabel("amplitude")
        #Spectrum
        plt.subplot(312)

        plt.plot(self.spec_x, self.spec_y, marker= 'o', linestyle='-')
        plt.axis([0, self.RATE / 2, 0, 2])
        plt.xlabel("frequency [Hz]")
        plt.ylabel("amplitude spectrum")
        #Pause
        
        plt.subplot(313)
        plt.axis('off')
        if(len(self.numero)>=16 ):
            self.numero=self.numero[1:]
        plt.text(0,0,   self.numero ,fontsize=50)
        
        plt.pause(.02)

        

        
        frecuenciaCorta=self.spec_y[110:241]
        if(max(frecuenciaCorta)<0.2):
            self.anterior=40
            return
        
             
        
        tacladoHori = np.array([(self.spec_y[self.frec1209-1]+self.spec_y[self.frec1209]+self.spec_y[self.frec1209+1])
                               ,(self.spec_y[self.frec1336-1]+self.spec_y[self.frec1336]+self.spec_y[self.frec1336+1])
                               ,(self.spec_y[self.frec1477-1]+self.spec_y[self.frec1477]+self.spec_y[self.frec1477+1])])
       
        
        tecladoVert = np.array([(self.spec_y[self.frec697-1]+self.spec_y[self.frec697]+self.spec_y[self.frec697+1])
                               ,(self.spec_y[self.frec770-1]+self.spec_y[self.frec770]+self.spec_y[self.frec770+1])
                               ,(self.spec_y[self.frec852-1]+self.spec_y[self.frec852]+self.spec_y[self.frec852+1])
                               ,(self.spec_y[self.frec941-1]+self.spec_y[self.frec941]+self.spec_y[self.frec941+1])])
       
        
         
        segundoMayor = max(np.where(tacladoHori == max(tacladoHori),0,(tacladoHori)))   #Si el SEGUNDO MAYOR es mayor que el 70% del MAYOR 
        if(max(tacladoHori)*0.5<segundoMayor):                                                  #Puro ojímetro                         
            self.anterior=40
            return
        
        
        segundoMayor = max(np.where((tecladoVert) == max(tecladoVert),0,tecladoVert))
        if(max(tecladoVert)*0.5<segundoMayor):          
            self.anterior=40
            return
                
        
        
#        print(int(self.spec_y[self.frec697]),int(self.spec_y[self.frec770]),int(self.spec_y[self.frec852]),int(self.spec_y[self.frec941]),int(self.spec_y[self.frec1209]),int(self.spec_y[self.frec1336]),int(self.spec_y[self.frec1477])) 
        
        resultado=self.teclado[ np.argmax(tecladoVert),np.argmax(tacladoHori)]
       
        if(resultado!=self.anterior):
            if(resultado==77):
                self.numero=self.numero+"*"
            elif(resultado==99):
                self.numero=self.numero+"#"
            else:
                self.numero=self.numero+str(resultado)           
                print(resultado)
        
        self.anterior=resultado

        

if __name__ == "__main__":
    spec = SpectrumAnalyzer()
