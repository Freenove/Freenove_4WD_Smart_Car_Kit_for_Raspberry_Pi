##############################################################################
0. Chapter Raspberry Pi Preparation
##############################################################################

Component List 
****************************************************************

Required Components
================================================================

.. list-table:: 
    :width: 100%
    :widths: 50 50
    :align: center
    :class: product-table

    *   -   Raspberry Pi 5 / 4B / 3B+ (Recommended) 
        -   5V/3A Power Adapter. Different versions of  
  
            Raspberry Pi have different power requirements.
    *   -   |Preparation00|
        -   |Preparation01|
    *   -   Micro USB Cable x1
        -   Micro SD Card (TF Card) x1, Card Reader x1
    *   -   |Preparation02|
        -   |Preparation03|


.. |Preparation00| image:: ../_static/imgs/Preparation/Preparation00.png
.. |Preparation01| image:: ../_static/imgs/Preparation/Preparation01.png
.. |Preparation02| image:: ../_static/imgs/Preparation/Preparation02.png
.. |Preparation03| image:: ../_static/imgs/Preparation/Preparation03.png

This robot also supports the following versions of the Raspberry Pi, but additional accessories need to be prepared by yourself. 

+--------------------------------------------+------------------------------------------------------------------------+
|  Raspberry                                 | Additional accessories                                                 |      
+--------------------------------------------+------------------------------------------------------------------------+
|                                            | Camera cable(>25cm) for zero w, 15 Pin 1.0mm Pitch to 22 Pin 0.5mm     |
|  Raspberry Pi Zero W                       |                                                                        |
|                                            | https://www.amazon.com/dp/B076Q595HJ/                                  |     
+--------------------------------------------+------------------------------------------------------------------------+
|                                            | wireless network adapter,                                              |      
|                                            |                                                                        |     
|  Raspberry Pi Zero 1.3                     | Camera cable(>25cm) for zero w, 15 Pin 1.0mm Pitch to 22 Pin 0.5mm,    |     
|                                            |                                                                        |     
|                                            | OTG cable (USB Type micro B to USB Type A)                             |     
+--------------------------------------------+------------------------------------------------------------------------+
|  Raspberry Pi 2 Model B                    | wireless network adapter                                               |     
+--------------------------------------------+------------------------------------------------------------------------+
|  Raspberry Pi 1 Model A+                   | wireless network adapter                                               |     
+--------------------------------------------+------------------------------------------------------------------------+
|  Raspberry Pi 1 Model B+                   | wireless network adapter                                               |     
+--------------------------------------------+------------------------------------------------------------------------+

Power requirements of various versions of Raspberry Pi are shown in following table:

+-------------------------+----------------------------------+----------------------------------------------------+------------------------------------------------+
| Product                 | Recommended PSU current capacity | Maximum total USB peripheral current draw          | Typical bare-board active current consumption  |
+=========================+==================================+====================================================+================================================+
| Raspberry Pi 1 Model A  | 700mA                            | 500mA                                              | 200mA                                          |
+-------------------------+----------------------------------+----------------------------------------------------+------------------------------------------------+
| Raspberry Pi 1 Model B  | 1.2A                             | 500mA                                              | 500mA                                          |
+-------------------------+----------------------------------+----------------------------------------------------+------------------------------------------------+
| Raspberry Pi 1 Model A+ | 700mA                            | 500mA                                              | 180mA                                          |
+-------------------------+----------------------------------+----------------------------------------------------+------------------------------------------------+
| Raspberry Pi 1 Model B+ | 1.8A                             | 1.2A                                               | 330mA                                          |
+-------------------------+----------------------------------+----------------------------------------------------+------------------------------------------------+
| Raspberry Pi 2 Model B  | 1.8A                             | 1.2A                                               | 350mA                                          |
+-------------------------+----------------------------------+----------------------------------------------------+------------------------------------------------+
| Raspberry Pi 3 Model B  | 2.5A                             | 1.2A                                               | 400mA                                          |
+-------------------------+----------------------------------+----------------------------------------------------+------------------------------------------------+
| Raspberry Pi 3 Model A+ | 2.5A                             | Limited by PSU, board, and connector ratings only. | 350mA                                          |
+-------------------------+----------------------------------+----------------------------------------------------+------------------------------------------------+
| Raspberry Pi 3 Model B+ | 2.5A                             | 1.2A                                               | 500mA                                          |
+-------------------------+----------------------------------+----------------------------------------------------+------------------------------------------------+
| Raspberry Pi 4 Model B  | 3.0A                             | 1.2A                                               | 600mA                                          |
+-------------------------+----------------------------------+----------------------------------------------------+------------------------------------------------+
| Raspberry Pi 5          | 5.0A                             | 1.6A (600mA if using a 3A power supply)            | 800mA                                          |
+-------------------------+----------------------------------+----------------------------------------------------+------------------------------------------------+
| Raspberry Pi 400        | 3.0A                             | 1.2A                                               | 800mA                                          |
+-------------------------+----------------------------------+----------------------------------------------------+------------------------------------------------+
| Raspberry Pi Zero       | 1.2A                             | Limited by PSU, board, and connector ratings only  | 100mA                                          |
+-------------------------+----------------------------------+----------------------------------------------------+------------------------------------------------+

.. seealso:: 

    For more details, please refer to https://www.raspberrypi.org/help/faqs/#powerReqs

In addition, RPi also needs an Ethernet network cable used to connect it to a WAN (Wide Area Network).

The Raspberry Pi 5 provides 1.6A of power to downstream USB peripherals when connected to a power supply capable of 5A at +5V (25W). When connected to any other compatible power supply, the Raspberry Pi 5 restricts downstream USB devices to 600mA of power.

Optional Components
****************************************************************

Under normal circumstances, there are two ways to login to Raspberry Pi: 

1) Using a stand-alone monitor. 
2) Using a remote desktop or laptop computer monitor “sharing” the PC monitor with your RPi.

Required Accessories for Monitor
================================================================

If you choose to use an independent monitor, mouse and keyboard, you also need the following accessories:
1. A display with a HDMI interface
2. A Mouse and a Keyboard with an USB interface

As to Pi Zero and Pi Zero W, you also need the following accessories:
1.	A Mini-HDMI to HDMI Adapter and Cable.
2.	A Micro-USB to USB-A Adapter and Cable (Micro USB OTG Cable). 
3.	A USB HUB.
4.	USB to Ethernet Interface or USB Wi-Fi receiver. 

For different Raspberry Pi Modules, the optional items may vary slightly but they all aim to convert the interfaces to Raspberry Pi standards.

+----------------------------------------------------------+--------------------------------------------+----------------------+----------------------+-----------------------+----------+-----------+-------+-------+
|                                                          | Pi Zero                                    | Pi A+                | Pi Zero W            | Pi 3A+                | Pi B+/2B | Pi 3B/3B+ | Pi 4B | Pi 5  |
+==========================================================+============================================+======================+======================+=======================+==========+===========+=======+=======+
| Monitor                                                  | Yes (All)                                                                                                                                               |
+----------------------------------------------------------+                                                                                                                                                         +
| Mouse                                                    |                                                                                                                                                         |
+----------------------------------------------------------+                                                                                                                                                         +
| Keyboard                                                 |                                                                                                                                                         |
+----------------------------------------------------------+--------------------------------------------+----------------------+----------------------+-----------------------+----------+-----------+-------+-------+
| Micro-HDMI to HDMI Adapter & Cable                       | Yes                                        | No                   | Yes                  | No                    | No       | No        | No    | No    |
+----------------------------------------------------------+--------------------------------------------+----------------------+----------------------+-----------------------+----------+-----------+-------+-------+
| Micro-HDMI to HDMI Adapter & Cable                       | No                                         | Yes                  |                      |                       |          |           |       |       |
+----------------------------------------------------------+--------------------------------------------+----------------------+----------------------+-----------------------+----------+-----------+-------+-------+
| Micro-USB to USB-A Adapter & Cable (Micro USB OTG Cable) | Yes                                        | No                   | Yes                  | No                    |          |           |       |       |
+----------------------------------------------------------+--------------------------------------------+----------------------+----------------------+-----------------------+----------+-----------+-------+-------+
| USB HUB                                                  | Yes                                        | Yes                  | Yes                  | Yes                   | No       | No        | No    | No    |
+----------------------------------------------------------+--------------------------------------------+----------------------+----------------------+-----------------------+----------+-----------+-------+-------+
| USB to Ethernet Interface                                | select one from two or select two from two | optional             | Internal Integration | Internal Integration  |          |           |       |       |
+----------------------------------------------------------+--------------------------------------------+----------------------+----------------------+-----------------------+----------+-----------+-------+-------+
| USB Wi-Fi Receiver                                       |                                            | Internal Integration | optional             |                       |          |           |       |       |
+----------------------------------------------------------+--------------------------------------------+----------------------+----------------------+-----------------------+----------+-----------+-------+-------+

Required Accessories for Remote Desktop
================================================================

+----------------------------------------------------------+---------+-----------+-------+--------+----------+----------------+
|                                                          | Pi Zero | Pi Zero W | Pi A+ | Pi 3A+ | Pi B+/2B | Pi 3B/3B+/4B/5 |
+==========================================================+=========+===========+=======+========+==========+================+
| Micro-USB to USB-A Adapter & Cable (Micro USB OTG Cable) | Yes     | Yes       | No    | NO                                 |
+----------------------------------------------------------+---------+-----------+-------+                                    +
| USB to Ethernet interface                                | Yes     | Yes       | Yes   |                                    |
+----------------------------------------------------------+---------+-----------+-------+--------+----------+----------------+

Raspberry Pi OS
****************************************************************

**Without Screen - Use Raspberry Pi - under Windows PC:** https://youtu.be/7vA5utwzY0E

.. raw:: html

   <iframe height="500" width="690" src="https://www.youtube.com/embed/7vA5utwzY0E" frameborder="0" allowfullscreen></iframe>

**With Screen - Use Raspberry Pi - under Windows PC:** https://youtu.be/HEywFsFrj3I

.. raw:: html

   <iframe height="500" width="690" src="https://www.youtube.com/embed/HEywFsFrj3I" frameborder="0" allowfullscreen></iframe>

Automatically Method
================================================================

| You can follow the official method to install the system for raspberry pi via visiting link below:
| https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/2
| In this way, the system will be downloaded **automatically** via the application. 

Manually Method
================================================================

After installing the Imager Tool in the **link above**. You can **also** download the system **manually** first. 

Visit https://www.raspberrypi.org/downloads/


.. image:: ../_static/imgs/Preparation/install-system-01.png

.. image:: ../_static/imgs/Preparation/install-system-02.png

And then the zip file is downloaded. 

Write System to Micro SD Card 
----------------------------------------------------------------

First, put your Micro SD card into card reader and connect it to USB port of PC. 

.. image:: ../_static/imgs/Preparation/install-system-03.png

Then open imager toll. Clicked Choose Device.

.. image:: ../_static/imgs/Preparation/install-system-04.png

Select a Raspberry PI Device based on your Raspberry PI version. It will help us filter out the right version of the system for the Raspberry PI.

.. image:: ../_static/imgs/Preparation/install-system-05.png

Clicked Operating System. 

.. image:: ../_static/imgs/Preparation/install-system-06.png

Choose system that you just downloaded in Use custom.

.. image:: ../_static/imgs/Preparation/install-system-07.png

Choose the SD card. Then click “Next”. 

.. image:: ../_static/imgs/Preparation/install-system-08.png

You can configure the Raspberry PI according to your needs.

.. image:: ../_static/imgs/Preparation/install-system-09.png

Enable ssh and configure WiFi
================================================================
On the GENERAL screen, configure your information based on your actual situation.
Enable SSH on the SERVICES page.

.. image:: ../_static/imgs/Preparation/install-system-10.png
    :width: 48%

.. image:: ../_static/imgs/Preparation/install-system-11.png
    :width: 48%

Click Save, in the new screen, click Yes, wait for SD to brush into the Raspberry system.

.. image:: ../_static/imgs/Preparation/install-system-12.png

Insert SD card
================================================================
Then remove SD card from card reader and insert it into Raspberry Pi.

.. image:: ../_static/imgs/Preparation/install-system-13.png

Connect to the power supply and wait for the Raspberry PI to turn on.

Getting Started with Raspberry Pi
****************************************************************

Monitor desktop
================================================================
If you do not have a spare monitor, please skip to next section `Remote desktop & VNC`_. If you have a spare monitor, please follow the steps in this section. 

After the system is written successfully, take out Micro SD Card and put it into the SD card slot of RPi. Then connect your RPi to the monitor through the HDMI port, attach your mouse and keyboard through the USB ports, attach a network cable to the network port and finally, connect your power supply (making sure that it meets the specifications required by your RPi Module Version. Your RPi should start (power up). Later, after setup, you will need to enter your user name and password to login. The default user name: pi; password: raspberry. After login, you should see the following screen.

.. image:: ../_static/imgs/Preparation/install-system-14.png

**Congratulations!** You have successfully installed the RASPBERRY PI OS operating system on your RPi.

Raspberry Pi 5, 4B, 3B+/3B integrates a Wi-Fi adaptor. You can use it to connect to your Wi-Fi. Then you can use the wireless remote desktop to control your RPi. This will be helpful for the following work. Raspberry Pi of other models can use wireless remote desktop through accessing an external USB wireless card.

.. image:: ../_static/imgs/Preparation/install-system-15.png

Set Resolution
================================================================

You can also set other resolutions. 

.. image:: ../_static/imgs/Preparation/Preparation04.png
    :align: center

If you don't know what resolution to set properly, you can try 1920x1080.

.. image:: ../_static/imgs/Preparation/Preparation05.png
    :align: center

In addition, your VNC Viewer window may zoom your Raspberry Pi desktop. You can change it. On your VNC View control panel, click right key. And select Properties->Options label->Scaling. Then set proper scaling. 

.. image:: ../_static/imgs/Preparation/Preparation06.png
    :align: center

.. image:: ../_static/imgs/Preparation/Preparation07.png
    :align: center

Here, you have logged in to Raspberry Pi successfully by using VNC Viewer and operated proper setting.

Raspberry Pi 5/4B/3B+/3B integrates a Wi-Fi adaptor.If you did not connect Pi to WiFi. You can connect it to wirelessly control the robot.

.. image:: ../_static/imgs/Preparation/Preparation08.png
    :align: center

Remote desktop & VNC
================================================================

**If you have logged in Raspberry Pi via display, you can skip to** `VNC Viewer & VNC`_.

If you don't have a spare display, mouse and keyboard for your RPi, you can use a remote desktop to share a display, keyboard, and mouse with your PC. Below is how to use: 
`MAC OS remote desktop`_ and `Windows OS remote desktop`_.

MAC OS Remote Desktop
----------------------------------------------------------------

Open the terminal and type following command. :red:`If this command doesn't work, please move to next page.`

.. code-block:: console

    $ ssh pi@raspberrypi.local

The password is **raspberry** by default, case sensitive. You may need to type **yes** during the process.

.. image:: ../_static/imgs/Preparation/install-system-16.png

.. image:: ../_static/imgs/Preparation/install-system-17.png

You can also use the IP address to log in Pi. 

Enter **router** client to **inquiry IP address** named **“raspberry pi”**. For example, I have inquired to **my RPi IP address, and it is “192.168.1.95".**

Open the terminal and type following command.

.. code-block:: console

    $ ssh pi@192.168.1.95

When you see :red:`pi@raspberrypi:`:blue:`~ $`, you have logged in Pi successfully. Then you can skip to next section.

.. image:: ../_static/imgs/Preparation/install-system-18.png

Then you can skip to `VNC Viewer & VNC`_.

Windows OS Remote Desktop
----------------------------------------------------------------
**If you are using win10, you can use follow way to login Raspberry Pi without desktop.**
Press `Win+R`. Enter `cmd`. Then use this command to check IP:

.. code-block:: console

    $ ping -4 raspberrypi.local

.. image:: ../_static/imgs/Preparation/install-system-19.png

| Then 192.168.1.147 is my Raspberry Pi IP.
| Or enter **router** client to **inquiry IP address** named **“raspberrypi”**. For example, I have inquired to **my RPi IP address, and it is “192.168.1.95".**

.. code-block:: console
    
    $ ssh pi@xxxxxxxxxxx(IP address)

Enter the following command:

.. code-block:: console
    
    $ ssh pi@192.168.1.95

.. image:: ../_static/imgs/Preparation/install-system-20.png

VNC Viewer & VNC
----------------------------------------------------------------

Enable VNC
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Type the following command. And select Interface Options->P5 VNC -> Enter->Yes->OK. Here Raspberry Pi may need be restarted, and choose ok. Then open VNC interface. 

.. code-block:: console
    
    $ sudo raspi-config

.. image:: ../_static/imgs/Preparation/install-system-21.png

.. image:: ../_static/imgs/Preparation/install-system-22.png

.. image:: ../_static/imgs/Preparation/install-system-23.png

.. image:: ../_static/imgs/Preparation/install-system-24.png

| Then download and install VNC Viewer according to your computer system by click following link:
| https://www.realvnc.com/en/connect/download/viewer/
| After installation is completed, open VNC Viewer. And click File -> New Connection. Then the interface is shown below. 

.. image:: ../_static/imgs/Preparation/install-system-25.png

| Enter ip address of your Raspberry Pi and fill in a name. Then click OK.
| Then on the VNC Viewer panel, double-click new connection you just created, 

.. image:: ../_static/imgs/Preparation/install-system-26.png

and the following dialog box pops up.  

.. image:: ../_static/imgs/Preparation/install-system-27.png

Enter username: **pi** and Password: **raspberry**. And click OK.     

.. image:: ../_static/imgs/Preparation/install-system-28.png

Here, you have logged in to Raspberry Pi successfully by using VNC Viewer

.. image:: ../_static/imgs/Preparation/install-system-29.png

If there is black window, please set resolution.

set resolution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You can also set other resolutions. 

.. image:: ../_static/imgs/Preparation/install-system-30.png

If you don't know what resolution to set properly, you can try 1920x1080.

.. image:: ../_static/imgs/Preparation/install-system-31.png

In addition, your VNC Viewer window may zoom your Raspberry Pi desktop. You can change it. On your VNC View control panel, click right key. And select Properties->Options label->Scaling. Then set proper scaling. 

.. image:: ../_static/imgs/Preparation/install-system-32.png

.. image:: ../_static/imgs/Preparation/install-system-33.png

Here, you have logged in to Raspberry Pi successfully by using VNC Viewer and operated proper setting.

Raspberry Pi 5/4B/3B+/3B integrates a Wi-Fi adaptor.If you did not connect Pi to WiFi. You can connect it to wirelessly control the robot.

.. image:: ../_static/imgs/Preparation/install-system-34.png
