----- For nodes participating in processing ----

Run Dependencies.sh

Run sensorserver.py with own ip argument on the bootstrap node
(acts as the bootstrap node for the dht at port 12550)

Run sensorserver.py on all other processing nodes with 4 arguments-
<ownIP,randomPort,bootstrapIP,12550>

Run worker.py on all processing nodes 

------------------------------------------------

Run actuator.py to simulate actuators on different machines 

Run sensor.py or sensor_xml.py to simulate sensors on different machines with 3 arguments
<IPofprocessingnode,imageType,IPofActuator>
##supported imagetypes temp and hum




