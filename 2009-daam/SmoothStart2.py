import AbstractRemoteRobot
def F():
    for x in range(10):
        self.SetEnginePWM(x)
        sleep(100) #100ms pause

AbstractRemoteRobot.execute(F)
#altrnative style for line 7:
AbstractRemoteRobot.define(F, 'SmoothStart')
AbstractRemoteRobot.SmoothStart()