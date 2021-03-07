# Autostart

To enable the Freenove Smart Car Server to run at startup follow the steps for your distro.

Credit of Leigh Dastey (ldastey@outlook.com).

## SystemD Configuration

*INSTALL_DIR below should be replaced throughout to the path of the file on your system*

1. Edit *$INSTALL_DIR*/Service/smart-car-server /etc/init.d/smart-car-server and modify $$INSTALL_DIR$$ to be the path of this file on your system
2. sudo ln -s *$INSTALL_DIR*/Service/smart-car-server.service /lib/systemd/system/smart-car-server.service  
3. sudo ln -s *$INSTALL_DIR*/Service/smart-car-server /etc/init.d/smart-car-server
4. sudo systemctl daemon-reload
5. sudo systemctl enable smart-car-server
6. sudo reboot

When the Pi restarts you will be able to connect client applications (i.e. mobile app) and test you can connect.

### SystemD Disable Autostart

1. sudo systemctl disable smart-car-server

