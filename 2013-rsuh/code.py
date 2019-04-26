import robotcis

r=robotcis.coonect('192.168.4.11')
camera = r.getCameras()
camera.show(block=False)

r.setSpeed((1,1))
r.run()

