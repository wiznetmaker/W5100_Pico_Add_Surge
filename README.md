# W5100_Pico_Add_Surge

Ethernet Surge Test - W5100S + Pico


## PROJECT DESCRIPTION

 I make a lot of products and always need to be tested.
There can be many problems with the power supply.

![image](https://github.com/wiznetmaker/W5100_Pico_Add_Surge/assets/111826791/32d91f2d-8f58-4970-94c3-503393a6c90d)

There are many reasons for the occurrence of surges, but the biggest cause is ESD.

So it's static electricity.

ESD is used as a means of certification for electronic products in many countries, including KC, FCC, and CE. In other words, only products certified by Test to ensure that they are safe from static electricity can be sold to consumers.

That's how important Surge Test is to the product.

![image](https://github.com/wiznetmaker/W5100_Pico_Add_Surge/assets/111826791/e527774b-e309-4c74-a41e-7a84d41851f3)

So I made a device that can simply apply Surge to each type of module.

![image](https://github.com/wiznetmaker/W5100_Pico_Add_Surge/assets/111826791/ef630a1a-3137-480f-ae82-c7109e21316f)

First, we need a simple relay.

I think we need to use FET to make a high-level surge generator, but this is okay if it is simply for testing a device that uses +5V power.

Variable resistance can determine the level of Surge.

The higher the variable resistance value, the smaller the Surge value.

![image](https://github.com/wiznetmaker/W5100_Pico_Add_Surge/assets/111826791/bf57cd76-d2a2-412d-bf99-497cc8af701b)

Under normal circumstances, the current will output a set voltage value if it flows only through that circuit. This voltage must be the source of the device to be tested.

![image](https://github.com/wiznetmaker/W5100_Pico_Add_Surge/assets/111826791/4c2ce763-dd33-41b6-acce-b2c99cd6d096)

And when the Switch is attached, the current flows like that circuit, and the source voltage increases.

And if you put the ADC value on Ethernet, you can see the voltage status on Ethernet, and you can apply Surge with the button.

https://youtube.com/shorts/BBxDDjOPHuA?feature=share
