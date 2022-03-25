# bean-cooker-iot
Hackathon Project from DB Evolve (3/25/2022)
Bean Cooker: Data Integration

Session Length: 4 hours
Objectives:
1.	To connect the Bean Cooker to Azure IoT Hub.
2.	To be able to send setpoints from the cloud to the device in order to control it.
3.	To log telemetry data from the device.
Background:
DB Engineering works with IoT devices and systems every day but is usually reliant on others to configure the devices and the pipeline. A typical IoT device has code embedded in it that handles the connection to the cloud and facilitates the transfer of data to the appropriate endpoint; this is usually configured by custom software and workflows on the devices themselves. 
In this session, the participants will connect an existing, open-source device (the Bean Cooker) to the cloud and attempt to write the basic components of an end-to-end system. 
Proposed Architecture:
The device will be connected to IoT Hub and will pass its data to a database. Commands can be sent back to the device from some other source by writing to IoT Hub and posting those to a topic the device listens to.
 
