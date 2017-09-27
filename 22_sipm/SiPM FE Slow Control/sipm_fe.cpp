#include "sipm_fe.h"
#include <unistd.h>
#include <stdio.h>
#include <string.h>

//#define DEBUG


sipm_fe::sipm_fe(linux_rs232* port) {
	_port = port;

	/* Set uart to 38400 BAUD and 8E1 */

	// Get current settings
	_fd = _port->getfd();
	tcgetattr(_fd, &_port_attr);
	// Set UART to 8E1
	_port_attr.c_cflag = CS8 | CLOCAL | CREAD | PARENB | HUPCL;
	// Set speed to 38400 BAUD
	cfsetispeed(&_port_attr, B38400);
	cfsetospeed(&_port_attr, B38400);
	// Apply settings to port
	tcsetattr(_fd, TCSAFLUSH, &_port_attr);

}

sipm_fe::~sipm_fe() {
	
}

void sipm_fe::hex_to_ascii(char* str, uint16_t hex, int len) {
	uint8_t buf;
	for (int i = 0; i < len; i++) {
		buf = (hex & 0xF0) >> 4;	
		if ( (buf >= 0x00) && (buf < 0x0A) )		// Digit from 0 to 9
			buf += '0';
		else if ( (buf >= 0x0A) && (buf < 0x10) )	// Digit from A to F
			buf += 'A' - 0x0A;
		str[i] = buf;
		hex = hex << 4;
	}
	return;
}

uint16_t sipm_fe::ascii_to_hex(char* str, int len) {
	uint16_t hex = 0x0000;
	for (int i = 0; i < len; i++) {
		hex = hex << 4;
		if ( (str[i] >= '0') && (str[i] <= '9') )
			hex |= 0x0F & (str[i] - '0');	
		else if ( (str[i] >= 'A') && (str[i] <= 'F') )
			hex |= 0x0F & (str[i] - 'A' + 10);
	}	
	return hex;
}

int sipm_fe::send_command(const uint8_t* cmd, const uint8_t* dat, int len) {

	/* 	The receiver and transmitter buffer rtx_buf
		is filled according to the protocol specified
		in the C11204-2 Command Reference (p. 5)	*/

	// Communication is ASCII based, so 0xAB (1 byte) has to be converter to 'A' and 'B' (2 byte)
	int ascii_len = 2*len;			
	if ( (ascii_len + 7) > MAX_BUF_LEN )	// Check for max length
		return -1;

	char str_buf[2];
	rtx_buf[0] = STX; 
	for (int i = 0; i < 3; i++)
		rtx_buf[1 + i] = cmd[i];
	for (int i = 0; i < len; i++) {		// Convert data to ASCII string
		hex_to_ascii(str_buf, dat[i], 2);	
		rtx_buf[4 + 2*i] = str_buf[0];
		rtx_buf[4 + 2*i + 1] = str_buf[1];
	}
	rtx_buf[4 + ascii_len] = ETX;
	// Calculate checksum from STX to ETX
	uint8_t cs = 0;	
	for (int i = 0; i < (5 + ascii_len); i++)
		cs += rtx_buf[i];
	hex_to_ascii(str_buf, cs, 2);	
	rtx_buf[5 + ascii_len] = str_buf[0];
	rtx_buf[6 + ascii_len] = str_buf[1];
	// Last character is carriage-return
	rtx_buf[7 + ascii_len] = CR;

#ifdef DEBUG
	// Debugging
	printf("\tSending: ");
	for (int i = 0; i < (8 + ascii_len); i++)
		printf("%c ", rtx_buf[i]);
	printf("\n");
#endif

	return _port->sendout(rtx_buf, 8+ascii_len);
}


int sipm_fe::read_in(uint8_t* msg){
	int len = 0;
	uint8_t cbuf;

	// Read single bytes using 100ms timeouts
	while ( _port->readin(&cbuf, 1, 100) ) {
		msg[len] = cbuf;
		len++;
	}

#ifdef DEBUG
	// Debugging
	printf("\tReading: ");
	for (int i = 0; i < len; i++)
		printf("%c ", msg[i]);
	printf("\n");
#endif
	return len;
}

void sipm_fe::set_temperature_correction_factor(const float* hst_vec){ 
	uint8_t cmd[3] = {'H', 'S', 'T'};
	uint8_t read_buf[64];
	uint16_t ddT1, ddT2, dT1, dT2, Ub, Tb;
	// Conversion from float to hex number (Command Reference p. 23)
	ddT1 = (uint16_t) (hst_vec[0]/1.507e-3);
	ddT2 = (uint16_t) (hst_vec[1]/1.507e-3);
	dT1 = (uint16_t) (hst_vec[2]/5.225e-2);
	dT2 = (uint16_t) (hst_vec[3]/5.225e-2);
	Ub = (uint16_t) (hst_vec[4]/1.812e-3);
	Tb = (uint16_t) ( (1.035-hst_vec[5]*5.5e-3)/1.907e-5 );

	// Cast 2 byte value into 1 byte data array
	uint8_t data[12];	
	data[0] = 0xFF & (ddT1 >> 8);
	data[1] = 0xFF & ddT1;
	data[2] = 0xFF & (ddT2 >> 8);
	data[3] = 0xFF & ddT2;
	data[4] = 0xFF & (dT1 >> 8);
	data[5] = 0xFF & dT1;
	data[6] = 0xFF & (dT2 >> 8);
	data[7] = 0xFF & dT2;
	data[8] = 0xFF & (Ub >> 8);
	data[9] = 0xFF & Ub;
	data[10] = 0xFF & (Tb >> 8);
	data[11] = 0xFF & Tb;

	this->send_command(cmd, data, 12);
	sleep(1);	// give it some time...
	this->read_in(read_buf);

	if ( strncmp( (const char*) (read_buf+1), "hst", 3) != 0 ) {
		printf("Error on return value - expected 'hst', read %c%c%c .\n", read_buf[1], read_buf[2], read_buf[3]);
		return;
	}

	return;
}

void sipm_fe::read_temperature_correction_factor(float* hrt_vec){ 
	uint8_t cmd[3] = {'H', 'R', 'T'};	
	uint8_t read_buf[64];
	this->send_command(cmd, read_buf, 0);
	usleep(100);	// wait a bit for an answer...

	int len = this->read_in(read_buf);	
	if (len != 32) {
		printf("Error on reading temperature coef.\n");
		return;
	}

	if ( strncmp( (const char*) (read_buf+1), "hrt", 3) != 0 ) {
		printf("Error on return value - expected 'hrt', read %c%c%c .\n", read_buf[1], read_buf[2], read_buf[3]);
		return;
	}

	// Extract coefficients from ASCII string
	hrt_vec[0] = 1.507e-3 * ascii_to_hex( (char*) (read_buf+4), 4);		// dT1'		
	hrt_vec[1] = 1.507e-3 * ascii_to_hex( (char*) (read_buf+8), 4);		// dT2'		
	hrt_vec[2] = 5.225e-2 * ascii_to_hex( (char*) (read_buf+12), 4);	// dT1		
	hrt_vec[3] = 5.225e-2 * ascii_to_hex( (char*) (read_buf+16), 4);	// dT2		
	hrt_vec[4] = 1.812e-3 * ascii_to_hex( (char*) (read_buf+20), 4);	// Ub		
	hrt_vec[5] = (1.035-1.907e-5*ascii_to_hex( (char*) (read_buf+24), 4))/5.5e-3;	// Tb		

	return;
}

void sipm_fe::read_temperature(float* hgt_vec){ 
	uint8_t cmd[3] = {'H', 'G', 'T'};	
	uint8_t read_buf[64];
	this->send_command(cmd, read_buf, 0);
	usleep(100);	// wait a bit for an answer...

	int len = this->read_in(read_buf);	
	if (len != 12) {
		printf("Error on reading temperature.\n");
		return;
	}

	if ( strncmp( (const char*) (read_buf+1), "hgt", 3) != 0 ) {
		printf("Error on return value - expected 'hgt', read %c%c%c .\n", read_buf[1], read_buf[2], read_buf[3]);
		return;
	}

	// Extract coefficients from ASCII string
	hgt_vec[0] = (1.035-1.907e-5*ascii_to_hex( (char*) (read_buf+4), 4))/5.5e-3;	// Temperature		

	return;
}

void sipm_fe::read_output_voltage(float* hgv_vec){ 
	uint8_t cmd[3] = {'H', 'G', 'V'};	
	uint8_t read_buf[64];
	this->send_command(cmd, read_buf, 0);
	usleep(100);	// wait a bit for an answer...

	int len = this->read_in(read_buf);	
	if (len != 12) {
		printf("Error on reading output voltage.\n");
		return;
	}

	if ( strncmp( (const char*) (read_buf+1), "hgv", 3) != 0 ) {
		printf("Error on return value - expected 'hgv', read %c%c%c .\n", read_buf[1], read_buf[2], read_buf[3]);
		return;
	}

	// Extract coefficients from ASCII string
	hgv_vec[0] = 1.812e-3 * ascii_to_hex( (char*) (read_buf+4), 4);	// output voltage		

	return;
}

void sipm_fe::read_output_current(float* hgc_vec){ 
	uint8_t cmd[3] = {'H', 'G', 'C'};	
	uint8_t read_buf[64];
	this->send_command(cmd, read_buf, 0);
	usleep(100);	// wait a bit for an answer...

	int len = this->read_in(read_buf);	
	if (len != 12) {
		printf("Error on reading output current.\n");
		return;
	}

	if ( strncmp( (const char*) (read_buf+1), "hgc", 3) != 0 ) {
		printf("Error on return value - expected 'hgc', read %c%c%c .\n", read_buf[1], read_buf[2], read_buf[3]);
		return;
	}

	// Extract coefficients from ASCII string
	hgc_vec[0] = 4.980e-3 * ascii_to_hex( (char*) (read_buf+4), 4);	// output voltage		

	return;
}
