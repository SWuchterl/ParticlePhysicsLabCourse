#include <stdio.h>
#include <unistd.h>

#include <fcntl.h>
#include <termios.h>
#include <termio.h>

#include <rs232/linux_rs232.h>
#include "sipm_fe.h"

#include <iostream>
#include <fstream>

using namespace std;

#define USB_PORT "/dev/ttyUSB0"

int main () {

	// Open usb port
	linux_rs232 usb(USB_PORT);

	// Create front-end object
	sipm_fe sipm(&usb);
	uint8_t data[64];	// data buffer for reading
	int len;		// length of read data

	//Temperature correction
	float s_coef[6] = {	// array to set temperature correction factor (command ref. p. 10)
			0,	// dT1'
			0,	// dT2'
			54.,	// dT1
			54.,	// dT2
			56.4,	// Ub
			25.0	// Tb
			};

	sipm.set_temperature_correction_factor(s_coef);

	float r_coef[6];
	sipm.read_temperature_correction_factor(r_coef);

	printf("Temperature correction factor reading:\n");
	printf("dT1' = %.01f mV/degC^2	\n", r_coef[0]);
	printf("dT2' = %.01f mV/degC^2	\n", r_coef[1]);
	printf("dT1 = %.01f mV/degC	\n", r_coef[2]);
	printf("dT2 = %.01f mV/degC	\n", r_coef[3]);
	printf("Ub = %.01f V		\n", r_coef[4]);
	printf("Tb = %.01f degC	\n", r_coef[5]);



	ofstream temp,volt,current,time;
	time.open("results/time.txt");
	temp.open("results/temperature.txt");
	volt.open("results/voltage.txt");
	current.open("results/current.txt");

	int i=0;	
	for (unsigned int i=0; i<=6;i++){

		int wait=30; //seconds

		float timestamp=i*wait;
		time<<timestamp<<"\n";

		// Temperature
		float r_temp[0];
		sipm.read_temperature(r_temp);
	
		temp<<r_temp[0]<<"\n";	
		printf("Temperature = %.01f degC	\n", r_temp[0]);

		//Output voltage
		float r_volt[0];
		sipm.read_output_voltage(r_volt);

		volt<<r_volt[0]<<"\n";
		printf("Output Voltage = %.02f V	\n", r_volt[0]);

		//Output current
		float r_current[0];
		sipm.read_output_current(r_current);
	
		current<<r_current[0]<<"\n";
		printf("Output current = %.01f mA	\n", r_current[0]);
		
		sleep(wait);
	}
	time.close();
	temp.close();
	current.close();
	volt.close();


	return 0;

	
}
