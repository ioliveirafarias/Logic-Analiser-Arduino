import matplotlib.pyplot as plt
import numpy as np
import time

plt.style.use('_mpl-gallery')

#################################################################
# Funções auxiliares
#################################################################

def getDataTable():
    return [[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

def refreshDataTable( myDataTable ):
    for line in range( len(myDataTable) ):    
        (myDataTable[line]).append( 0 ) 
        (myDataTable[line]).pop(0)

def getDefaultColors():
    return [(1,0,0,1),
            (0,1,0,1),
            (1,1,0,1),
            (0,0,1,1)]    

#################################################################        
        
#################################################################
# Main
#################################################################

def main():
    myDataTable = getDataTable()
    arrayAux = []
    for lineLength in range( len(myDataTable[0]) ):
        arrayAux.append(lineLength)

    # Definindo janela e gráfico
    plt.ion() 
    plt.rcParams['figure.figsize'] = [10, 5]     
    fig, (ax) = plt.subplots(1, 1, layout='constrained')
    ax.set( ylim=[0, len(myDataTable)+1 ], xlabel='Nível lógico', ylabel='Pontas de prova')
    ax.set_facecolor("lightgray")
    ax.set_title("Analisador de sinais")

    # Associando linhas a valores para impressão
    pltLines = []
    defaultColors = getDefaultColors()    
    for line in range( len(myDataTable) ):
        line1, = ax.plot(arrayAux, myDataTable[line], color=defaultColors[line]) 
        pltLines.append(line1)

    # Atualizando gráfico
    while True:
        for line in range( len(myDataTable) ):
            auxLine = []        
            for lineLength in range( len(myDataTable[line]) ):
                auxLine.append(myDataTable[line][lineLength] + line)
            pltLines[line].set_ydata(auxLine)
        fig.canvas.draw() 
        fig.canvas.flush_events()
        refreshDataTable( myDataTable )

#################################################################
# Script
#################################################################

main()