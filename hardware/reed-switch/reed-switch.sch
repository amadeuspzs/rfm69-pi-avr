EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L power:GND #PWR05
U 1 1 5FC7E839
P 5600 3850
F 0 "#PWR05" H 5600 3600 50  0001 C CNN
F 1 "GND" H 5605 3677 50  0000 C CNN
F 2 "" H 5600 3850 50  0001 C CNN
F 3 "" H 5600 3850 50  0001 C CNN
	1    5600 3850
	1    0    0    -1  
$EndComp
$Comp
L Device:CP C3
U 1 1 5FC7E845
P 5600 3550
F 0 "C3" H 5718 3596 50  0000 L CNN
F 1 "47uF" H 5718 3505 50  0000 L CNN
F 2 "" H 5638 3400 50  0001 C CNN
F 3 "~" H 5600 3550 50  0001 C CNN
	1    5600 3550
	1    0    0    -1  
$EndComp
$Comp
L Device:R R4
U 1 1 5FC7E84B
P 6000 3750
F 0 "R4" V 5793 3750 50  0000 C CNN
F 1 "10K" V 5884 3750 50  0000 C CNN
F 2 "" V 5930 3750 50  0001 C CNN
F 3 "~" H 6000 3750 50  0001 C CNN
	1    6000 3750
	0    1    1    0   
$EndComp
$Comp
L Switch:SW_Reed SW1
U 1 1 5FC7E851
P 6300 3550
F 0 "SW1" V 6254 3635 50  0000 L CNN
F 1 "SW_Reed" V 6345 3635 50  0000 L CNN
F 2 "" H 6300 3550 50  0001 C CNN
F 3 "~" H 6300 3550 50  0001 C CNN
	1    6300 3550
	0    1    1    0   
$EndComp
Wire Wire Line
	5600 3700 5600 3750
Wire Wire Line
	5850 3750 5800 3750
Connection ~ 5600 3750
Wire Wire Line
	5600 3750 5600 3850
Wire Wire Line
	6150 3750 6300 3750
Wire Wire Line
	6300 3350 5600 3350
Wire Wire Line
	5600 3350 5600 3400
Connection ~ 6300 3350
$Comp
L MCU_Microchip_ATtiny:ATtiny84-20PU U?
U 1 1 5FC9BC5C
P 7700 3250
F 0 "U?" H 7171 3296 50  0000 R CNN
F 1 "ATtiny84-20PU" H 7171 3205 50  0000 R CNN
F 2 "Package_DIP:DIP-14_W7.62mm" H 7700 3250 50  0001 C CIN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/doc8006.pdf" H 7700 3250 50  0001 C CNN
	1    7700 3250
	1    0    0    -1  
$EndComp
Wire Wire Line
	6300 3350 8300 3350
Wire Wire Line
	7700 4150 5800 4150
Wire Wire Line
	5800 4150 5800 3750
Connection ~ 5800 3750
Wire Wire Line
	5800 3750 5600 3750
$Comp
L power:+3.3V #PWR?
U 1 1 5FC9D817
P 5650 2350
F 0 "#PWR?" H 5650 2200 50  0001 C CNN
F 1 "+3.3V" H 5665 2523 50  0000 C CNN
F 2 "" H 5650 2350 50  0001 C CNN
F 3 "" H 5650 2350 50  0001 C CNN
	1    5650 2350
	1    0    0    -1  
$EndComp
Wire Wire Line
	7700 2350 5650 2350
$EndSCHEMATC
