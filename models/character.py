import socket
import bge

cont = bge.logic.getCurrentController()
own = cont.owner
sce = bge.logic.getCurrentScene()



def main():
    level = sce.name
    if level == 'Level1':
        tank = sce.objects['Body']
        hamster = sce.objects['HamsterHost']
        boot = sce.objects['boot']
        wheel0 = sce.objects['Wheel0']
        wheel1 = sce.objects['Wheel1']
        wheel2 = sce.objects['Wheel2']
        wheel3 = sce.objects['Wheel3']
    elif level == 'Level2':
        tank = sce.objects['Body.001']
        hamster = sce.objects['HamsterHost.001']
        boot = sce.objects['boot.001']
        wheel0 = sce.objects['Wheel4']
        wheel1 = sce.objects['Wheel5']
        wheel2 = sce.objects['Wheel6']
        wheel3 = sce.objects['Wheel7']


    if bge.logic.globalDict['characterProperty'] == "tank":
        #set visibility
        tank.setVisible(True, True)
        hamster.setVisible(False, True)
        boot.setVisible(False, True)
        wheel0.setVisible(False,True)
        wheel1.setVisible(False,True)
        wheel2.setVisible(False,True)
        wheel3.setVisible(False,True)
    elif bge.logic.globalDict['characterProperty'] == "hamster":
        tank.setVisible(False, True)
        hamster.setVisible(True, True)
        boot.setVisible(False, True)
    elif  bge.logic.globalDict['characterProperty'] == "boot":
        tank.setVisible(False, True)
        hamster.setVisible(False, True)
        boot.setVisible(True, True)
        wheel0.setVisible(False,True)
        wheel1.setVisible(False,True)
        wheel2.setVisible(False,True)
        wheel3.setVisible(False,True)



if __name__ == "__main__":
    main()
