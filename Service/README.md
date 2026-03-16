# Autostart

To enable the Freenove Smart Car Server to run at startup follow the steps for your distro.

Credit of Leigh Dastey (ldastey@outlook.com).

## SystemD Configuration

**INSTALL_DIR below should be replaced throughout to the path of the file on your system**

Edit **$INSTALL_DIR**/Service/smart-car-server and change $INSTALL_DIR to be the path of this file on your system

Then run the following commands:

    sudo chmod 755 $INSTALL_DIR/Service/smart-car-server
    sudo ln -s $INSTALL_DIR/Service/smart-car-server.service /lib/systemd/system/smart-car-server.service  
    sudo ln -s $INSTALL_DIR/Service/smart-car-server /etc/init.d/smart-car-server
    sudo systemctl daemon-reload
    sudo systemctl enable smart-car-server
    sudo reboot

When the Pi restarts you will be able to connect client applications (i.e. mobile app) and test you can connect.

### SystemD Disable Autostart

To disable the SystemD autostart run 

    sudo systemctl disable smart-car-server

