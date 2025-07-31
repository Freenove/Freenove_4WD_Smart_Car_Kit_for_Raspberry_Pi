##############################################################################
Chapter 4 Light tracing Car
##############################################################################

**If you have any concerns, please feel free to contact us via** support@freenove.com

Description
****************************************************************

The light-tracing function of the car mainly uses a photoresistor. The car has two photoresistors located on the left and right sides at the front to detect light

A photoresistor is a resistor based on the photoelectric effect of the semiconductor. The resistance changes with the intensity of the incident light. With the incident light intensity increasing, the resistance decreases. With the incident light intensity decreasing, the resistance increases.

And the change of the resistance value also causes voltage applied to the photoresistor changes. According to the change of voltage, the position of the light to the car will be detected, and then make the car move corresponding action to trace light.
 
Put your car in a darker environment. 

Run program
****************************************************************

If the terminal displays the directory as below, you can directly execute the Light.py command. 
 
.. image:: ../_static/imgs/Chapter_4_Light_tracing_Car/Chapter4_00.png
    :align: center

1.	If not, execute the cd command:

.. code-block:: console

    $ cd ~/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/Code/Server

2.	Run Light.py:

.. code-block:: console

    $ sudo python car.py Light

The code is below:

.. literalinclude:: ../../../freenove_Kit/Code/Server/car.py
    :linenos: 
    :language: python
    :lines: 1-9, 108-123, 159-167, 179-183, 188-189

Result analysis
================================================================

When the voltages of left and right photoresistor are less than 2.99V, the car move forward straightly. And when one of the voltages is greater than 3V:

If the left voltage is greater than the right, the car turns left. 

If the right voltage is greater than the left, the car turns right. 

You can change the judgment of the program to achieve the result you want, according to the light intensity of the environment.