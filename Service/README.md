# Autostart

To enable the Freenove Smart Car Server to run at startup follow the steps for your distro.

Credit of Leigh Dastey (ldastey@outlook.com).

## SystemD Configuration

1. sudo ln -s *$INSTALL_DIR*/Service/smart-car-server.service /lib/systemd/system/smart-car-server.service  
2. sudo ln -s *$INSTALL_DIR*/Service/smart-car-server /etc/init.d/smart-car-server
3. sudo systemctl daemon-reload
4. sudo systemctl enable smart-car-server
5. sudo reboot

When the Pi restarts you will be able to connect client applications (i.e. mobile app) and test you can connect.

### SystemD Disable Autostart

1. sudo systemctl disable smart-car-server

