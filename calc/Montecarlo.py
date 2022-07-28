import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io
import base64
import itertools
import math
from matplotlib.backends.backend_agg import FigureCanvasAgg

class Montecarlo:
    """
    Clase que manejo diferentes metodos aletorios
    """
    def __init__(self):
        autoXdia = [0,1,2,3,4]
        probAxD = [0.1,0.1,0.25,0.3,0.25]
        self.data1 = pd.DataFrame({'autoxdia': autoXdia, 'probabilidad': probAxD})
        diaXauto = [1,2,3,4]
        probDxA = [0.4,0.35,0.15,0.1]
        self.data2 = pd.DataFrame({'diaxauto': diaXauto, 'probabilidad': probDxA})
        self.aleatorios1 = [0.13,0.95,0.62,0.71,0.54,0.83,0.54,0.63,0.95,0.24,0.02,0.57,0.37,0.02,0.56]
        self.aleatorios2 = [0.90,0.41,0.86,0.18,0.80,0.70,0.09,0.30,0.98,0.23,0.85,0.23,0.89,0.65,0.99]
        
    def probabilidadAuto(self):
        a = self.data1['probabilidad']
        a1= np.cumsum(a) #Cálculo la suma acumulativa de las probabilidades
        self.data1['FPA'] =a1
        self.data1['Min'] = self.data1['FPA']
        self.data1['Max'] = self.data1['FPA']
        lis = self.data1["Min"].values
        lis2 = self.data1['Max'].values
        lis[0]= 0
        for i in range(1,len(self.data1)):
            lis[i] = lis2[i-1]
        self.data1['Min'] = lis
        data = self.data1.to_html(classes="dataTable table table-bordered table-hover", justify="justify-all", border=0)
        return (data)

    def probabilidadDia(self):
        a=self.data2['probabilidad']
        a1= np.cumsum(a) #Cálculo la suma acumulativa de las probabilidades
        self.data2['FPA'] =a1
        self.data2['Min'] = self.data2['FPA']
        self.data2['Max'] = self.data2['FPA']
        lis = self.data2["Min"].values
        lis2 = self.data2['Max'].values
        lis[0]= 0
        for i in range(1,len(self.data2)):
            lis[i] = lis2[i-1]
        self.data2['Min'] = lis
        data = self.data2.to_html(classes="dataTable table table-bordered table-hover", justify="justify-all", border=0)
        return (data)


    def tablaProbabilidades(self):
        def busqueda(arrmin, arrmax, valor):
            #print(valor)
            for i in range (len(arrmin)):
            # print(arrmin[i],arrmax[i])
                if valor >= arrmin[i] and valor <= arrmax[i]:
                    return i
            return -1
        dfMCL = pd.DataFrame({'ri-auto': self.aleatorios1})
        max = self.data1['Max'].values
        min = self.data1['Min'].values
        xpos = dfMCL['ri-auto']
        posi = [0] * len(dfMCL)
        for j in range(len(dfMCL)):
            val = xpos[j]
            pos = busqueda(min,max,val)
            posi[j] = pos
        simula = []
        for j in range(len(dfMCL)):
            for i in range(len(dfMCL)):
                sim = self.data1.loc[self.data1['autoxdia'] == posi[i]+1]
                simu = sim.filter(['probabilidad']).values
                iterator = itertools.chain(*simu)
                for item in iterator:
                    a=item
                simula.append(round(a,2))
        dfMCL["Simulación"] = pd.DataFrame(simula)
        dfMCL['autos'] = posi
        dfMCL['ri-dia'] = self.aleatorios2
        max = self.data2['Max'].values
        min = self.data2['Min'].values
        xpos = dfMCL['ri-dia']
        posi = [0] * len(dfMCL)
        for j in range(len(dfMCL)):
            val = xpos[j]
            pos = busqueda(min,max,val)
            posi[j] = pos
        simula = []
        for j in range(len(dfMCL)):
            for i in range(len(dfMCL)):
                sim = self.data2.loc[self.data2['diaxauto'] == posi[i]+1]
                simu = sim.filter(['probabilidad']).values
                iterator = itertools.chain(*simu)
                for item in iterator:
                    a=item
                simula.append(round(a,2))
        dfMCL["Simulación1"] = pd.DataFrame(simula)
        for i in range(len(posi)):
            posi[i] = posi[i]+1
        dfMCL['dias'] = posi
        data = dfMCL.to_html(classes="dataTable table table-bordered table-hover", justify="justify-all", border=0)
        return (data, dfMCL)

    def simulacion6(self, dfMCL):
        autos = 6
        costoAuto = 75000
        alquilerDiario = 700
        noDisponible = 400
        autoOcioso = 100
        inicial = [0]*len(dfMCL)
        inicial[0] = autos
        final = []
        alquiler = []
        disponibilidad = []
        devolver = []
        ocioso = []
        for index, row in dfMCL.iterrows():
            final.append(inicial[index]-row['autos'])
            devolver.append(row['dias']+index)
            if inicial[index] < row['autos']:
                disponibilidad.append(noDisponible)
                if inicial[index] > 0:
                    alquiler.append(inicial[index]*alquilerDiario*row['dias'])
                else:
                    alquiler.append(0)
            else:
                alquiler.append(alquilerDiario*row['autos']*row['dias'])
                disponibilidad.append(0)
            for i in range(len(inicial)):
                if i==devolver[index]:
                    inicial[i] = row['autos'] + inicial[i]
                if i == index+1:
                    inicial[i] = final[index] + inicial[i]
            #inicial[int(devolver[index])] = row['autos']
            ocioso.append(autoOcioso*final[index])
        dfMCL["inventario-inicial"] = pd.DataFrame(inicial)
        dfMCL["inventario-final"] = pd.DataFrame(final)
        dfMCL["Alquiler"] = pd.DataFrame(alquiler)
        dfMCL["Ocioso"] = pd.DataFrame(ocioso)
        dfMCL["No Disponible"] = pd.DataFrame(disponibilidad)
        data = dfMCL.to_html(classes="dataTable table table-bordered table-hover", justify="justify-all", border=0)
        precioAutos = autos * costoAuto
        alquilerPromedio=dfMCL["Alquiler"].mean()
        ociosoPromedio=dfMCL["Ocioso"].mean()
        noDisponiblePromedio=dfMCL["No Disponible"].mean()
        self.simulacion = pd.DataFrame({'6 autos': [precioAutos, alquilerPromedio, ociosoPromedio, noDisponiblePromedio],
                                'index': ['Precio Autos', ' Promedio alquiler', 'Promedio Ocioso', 'Promedio no disponible']})
        self.simulacion.set_index('index', inplace=True)
        return (data)

    def simulaciones(self, dfMCL):
        autos = 7
        costoAuto = 75000
        alquilerDiario = 700
        noDisponible = 400
        autoOcioso = 100
        #dfMCL['inventario-inicial'] = 0
        #dfMCL.loc[:0,'inventario-inicial'] = autos
        #dfMCL['inventario-final'] = 0
        # dfMCL.loc[:1,'inventario-final'] = autos
        inicial = [0]*len(dfMCL)
        inicial[0] = autos
        final = []
        alquiler = []
        disponibilidad = []
        devolver = []
        ocioso = []
        for index, row in dfMCL.iterrows():
            final.append(inicial[index]-row['autos'])
            devolver.append(row['dias']+index)
            if inicial[index] < row['autos']:
                disponibilidad.append(noDisponible)
                if inicial[index] > 0:
                    alquiler.append(inicial[index]*alquilerDiario*row['dias'])
                else:
                    alquiler.append(0)
            else:
                alquiler.append(alquilerDiario*row['autos']*row['dias'])
                disponibilidad.append(0)
            for i in range(len(inicial)):
                if i==devolver[index]:
                    inicial[i] = row['autos'] + inicial[i]
                if i == index+1:
                    inicial[i] = final[index] + inicial[i]
            #inicial[int(devolver[index])] = row['autos']
            ocioso.append(autoOcioso*final[index])
        dfMCL["inventario-inicial"] = pd.DataFrame(inicial)
        dfMCL["inventario-final"] = pd.DataFrame(final)
        dfMCL["Alquiler"] = pd.DataFrame(alquiler)
        dfMCL["Ocioso"] = pd.DataFrame(ocioso)
        dfMCL["No Disponible"] = pd.DataFrame(disponibilidad)

        precioAutos = autos * costoAuto
        alquilerPromedio = dfMCL["Alquiler"].mean()
        ociosoPromedio = dfMCL["Ocioso"].mean()
        noDisponiblePromedio = dfMCL["No Disponible"].mean()
        self.simulacion['7 autos'] = [precioAutos, alquilerPromedio, ociosoPromedio, noDisponiblePromedio]

        autos = 8
        costoAuto = 75000
        alquilerDiario = 700
        noDisponible = 400
        autoOcioso = 100
        #dfMCL['inventario-inicial'] = 0
        #dfMCL.loc[:0,'inventario-inicial'] = autos
        #dfMCL['inventario-final'] = 0
        # dfMCL.loc[:1,'inventario-final'] = autos
        inicial = [0]*len(dfMCL)
        inicial[0] = autos
        final = []
        alquiler = []
        disponibilidad = []
        devolver = []
        ocioso = []
        for index, row in dfMCL.iterrows():
            final.append(inicial[index]-row['autos'])
            devolver.append(row['dias']+index)
            alquiler.append(alquilerDiario*row['autos']*row['dias'])
            if inicial[index] < row['autos']:
                disponibilidad.append(noDisponible)
                if inicial[index] > 0:
                    alquiler.append(inicial[index]*alquilerDiario*row['dias'])
                else:
                    alquiler.append(0)
            else:
                alquiler.append(alquilerDiario*row['autos']*row['dias'])
                disponibilidad.append(0)
            for i in range(len(inicial)):
                if i==devolver[index]:
                    inicial[i] = row['autos'] + inicial[i]
                if i == index+1:
                    inicial[i] = final[index] + inicial[i]
            #inicial[int(devolver[index])] = row['autos']
            ocioso.append(autoOcioso*final[index])
        dfMCL["inventario-inicial"] = pd.DataFrame(inicial)
        dfMCL["inventario-final"] = pd.DataFrame(final)
        dfMCL["Alquiler"] = pd.DataFrame(alquiler)
        dfMCL["Ocioso"] = pd.DataFrame(ocioso)
        dfMCL["No Disponible"] = pd.DataFrame(disponibilidad)

        precioAutos = autos * costoAuto
        alquilerPromedio = dfMCL["Alquiler"].mean()
        ociosoPromedio = dfMCL["Ocioso"].mean()
        noDisponiblePromedio = dfMCL["No Disponible"].mean()
        self.simulacion['8 autos'] = [precioAutos, alquilerPromedio, ociosoPromedio, noDisponiblePromedio]

        autos = 9
        costoAuto = 75000
        alquilerDiario = 700
        noDisponible = 400
        autoOcioso = 100
        #dfMCL['inventario-inicial'] = 0
        #dfMCL.loc[:0,'inventario-inicial'] = autos
        #dfMCL['inventario-final'] = 0
        # dfMCL.loc[:1,'inventario-final'] = autos
        inicial = [0]*len(dfMCL)
        inicial[0] = autos
        final = []
        alquiler = []
        disponibilidad = []
        devolver = []
        ocioso = []
        for index, row in dfMCL.iterrows():
            final.append(inicial[index]-row['autos'])
            devolver.append(row['dias']+index)
            alquiler.append(alquilerDiario*row['autos']*row['dias'])
            if inicial[index] < row['autos']:
                disponibilidad.append(noDisponible)
                if inicial[index] > 0:
                    alquiler.append(inicial[index]*alquilerDiario*row['dias'])
                else:
                    alquiler.append(0)
            else:
                alquiler.append(alquilerDiario*row['autos']*row['dias'])
                disponibilidad.append(0)
            for i in range(len(inicial)):
                if i==devolver[index]:
                    inicial[i] = row['autos'] + inicial[i]
                if i == index+1:
                    inicial[i] = final[index] + inicial[i]
            #inicial[int(devolver[index])] = row['autos']
            ocioso.append(autoOcioso*final[index])
        dfMCL["inventario-inicial"] = pd.DataFrame(inicial)
        dfMCL["inventario-final"] = pd.DataFrame(final)
        dfMCL["Alquiler"] = pd.DataFrame(alquiler)
        dfMCL["Ocioso"] = pd.DataFrame(ocioso)
        dfMCL["No Disponible"] = pd.DataFrame(disponibilidad)

        precioAutos = autos * costoAuto
        alquilerPromedio = dfMCL["Alquiler"].mean()
        ociosoPromedio = dfMCL["Ocioso"].mean()
        noDisponiblePromedio = dfMCL["No Disponible"].mean()
        self.simulacion['9 autos'] = [precioAutos, alquilerPromedio, ociosoPromedio, noDisponiblePromedio]

        autos = 10
        costoAuto = 75000
        alquilerDiario = 700
        noDisponible = 400
        autoOcioso = 100
        #dfMCL['inventario-inicial'] = 0
        #dfMCL.loc[:0,'inventario-inicial'] = autos
        #dfMCL['inventario-final'] = 0
        # dfMCL.loc[:1,'inventario-final'] = autos
        inicial = [0]*len(dfMCL)
        inicial[0] = autos
        final = []
        alquiler = []
        disponibilidad = []
        devolver = []
        ocioso = []
        for index, row in dfMCL.iterrows():
            final.append(inicial[index]-row['autos'])
            devolver.append(row['dias']+index)
            alquiler.append(alquilerDiario*row['autos']*row['dias'])
            if inicial[index] < row['autos']:
                disponibilidad.append(noDisponible)
                if inicial[index] > 0:
                    alquiler.append(inicial[index]*alquilerDiario*row['dias'])
                else:
                    alquiler.append(0)
            else:
                alquiler.append(alquilerDiario*row['autos']*row['dias'])
                disponibilidad.append(0)
            for i in range(len(inicial)):
                if i==devolver[index]:
                    inicial[i] = row['autos'] + inicial[i]
                if i == index+1:
                    inicial[i] = final[index] + inicial[i]
            #inicial[int(devolver[index])] = row['autos']
            ocioso.append(autoOcioso*final[index])
        dfMCL["inventario-inicial"] = pd.DataFrame(inicial)
        dfMCL["inventario-final"] = pd.DataFrame(final)
        dfMCL["Alquiler"] = pd.DataFrame(alquiler)
        dfMCL["Ocioso"] = pd.DataFrame(ocioso)
        dfMCL["No Disponible"] = pd.DataFrame(disponibilidad)

        precioAutos = autos * costoAuto
        alquilerPromedio = dfMCL["Alquiler"].mean()
        ociosoPromedio = dfMCL["Ocioso"].mean()
        noDisponiblePromedio = dfMCL["No Disponible"].mean()
        self.simulacion['10 autos'] = [precioAutos, alquilerPromedio, ociosoPromedio, noDisponiblePromedio]
        data = self.simulacion.to_html(classes="dataTable table table-bordered table-hover", justify="justify-all", border=0)

        return(data)

    def ganancia(self):
        seis = self.simulacion['6 autos']
        seis = seis[1] - seis[2] - seis[3]
        siete = self.simulacion['7 autos']
        siete = siete[1] - siete[2] - siete[3]
        ocho = self.simulacion['8 autos']
        ocho = ocho[1] - ocho[2] - ocho[3]
        nueve = self.simulacion['9 autos']
        nueve = nueve[1] - nueve[2] - nueve[3]
        diez = self.simulacion['10 autos']
        diez = diez[1] - diez[2] - diez[3]
        dfGanancia = pd.DataFrame({'ganancia': [seis, siete, ocho, nueve, diez]})
        dfGanancia['autos'] = [6,7,8,9,10]
        data = dfGanancia.to_html(classes="dataTable table table-bordered table-hover", justify="justify-all", border=0)

        img = io.BytesIO()
        plt.figure(figsize=(8,4))
        plt.title('Relacion ganancia por auto')
        plt.plot(dfGanancia['autos'], dfGanancia['ganancia'], marker='o', color='red')
        plt.xlabel('Numero de autos comprados')
        plt.ylabel('Ganancia por auto') 
        plt.legend(('Ganancia', ), prop = {'size':12},loc='upper right')
        plt.savefig(img, format='png')
        plt.clf()
        img.seek(0)
        img_url = base64.b64encode(img.getvalue()).decode('UTF-8')

        return(data, img_url)

