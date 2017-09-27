#include <rs232/linux_rs232.h>

#define MAX_BUF_LEN	64
#define STX		0x02
#define ETX		0x03
#define	CR		0x0D

class sipm_fe {
	private:
	linux_rs232* _port;
	int _fd;
	struct termios _port_attr;
	uint8_t rtx_buf[MAX_BUF_LEN];

	// Converts a hex number into a string
	// e.g. 0xAB -> {'A', 'B'}
	void hex_to_ascii(char* str, uint16_t hex, int len);

	// Converts a ASCII string into a hex number
	// e.g. {'B', 'E' , 'E', 'F'} -> 0xBEEF
	uint16_t ascii_to_hex(char* str, int len);

	public:
	sipm_fe(linux_rs232* port);
	~sipm_fe();

	// Sends a 3 byte command with defined payload dat to front-end
	// Returns number of sent bytes (including STX, ETX, checksum, ...)
	int send_command(const uint8_t* cmd, const uint8_t* dat, int len);

	// Reads data (if available) from front-end
	// Returns number of read bytes
	int read_in(uint8_t* msg);

	void set_temperature_correction_factor(const float* hst_vec);
	void read_temperature_correction_factor(float* hrt_vec); 
	void read_temperature(float* hgt_vec);
	void read_output_voltage(float* hgv_vec);
	void read_output_current(float* hgc_vec);
};
