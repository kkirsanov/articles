import AbstractRemoteRobot

for x in range(10):
    AbstractRemoteRobot.SetEnginePWM(x)
    sleep(100) #100ms pause