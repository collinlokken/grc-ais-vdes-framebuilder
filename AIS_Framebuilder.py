"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import time

result = []

class blk(gr.basic_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, longitude=9.344559, latitude=63.044153):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='AIS Framebuilder',   # will show up in GRC
            in_sig=None,
            out_sig=[np.byte]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        #self.example_param = example_param

        self.latitude = latitude
        self.longitude = longitude

    def generate_payload(self, lng, lat):
        first = "0000010000111010111101110011100110101011111000000000010001100"
        last = "0010111011101111111111001100000000000000000000000000"
        longitude = '{0:b}'.format(int(round(lng*600000)) & 0b1111111111111111111111111111).rjust(28,'0')
        latitude =  '{0:b}'.format(int(round(lat*600000)) & 0b111111111111111111111111111).rjust(27,'0')

        return first + longitude + latitude + last
    

    CRC16_XMODEM_TABLE = [
        0x0000, 0x1189, 0x2312, 0x329B, 0x4624, 0x57AD, 0x6536, 0x74BF,
        0x8C48, 0x9DC1, 0xAF5A, 0xBED3, 0xCA6C, 0xDBE5, 0xE97E, 0xF8F7,
        0x1081, 0x0108, 0x3393, 0x221A, 0x56A5, 0x472C, 0x75B7, 0x643E,
        0x9CC9, 0x8D40, 0xBFDB, 0xAE52, 0xDAED, 0xCB64, 0xF9FF, 0xE876,
        0x2102, 0x308B, 0x0210, 0x1399, 0x6726, 0x76AF, 0x4434, 0x55BD,
        0xAD4A, 0xBCC3, 0x8E58, 0x9FD1, 0xEB6E, 0xFAE7, 0xC87C, 0xD9F5,
        0x3183, 0x200A, 0x1291, 0x0318, 0x77A7, 0x662E, 0x54B5, 0x453C,
        0xBDCB, 0xAC42, 0x9ED9, 0x8F50, 0xFBEF, 0xEA66, 0xD8FD, 0xC974,
        0x4204, 0x538D, 0x6116, 0x709F, 0x0420, 0x15A9, 0x2732, 0x36BB,
        0xCE4C, 0xDFC5, 0xED5E, 0xFCD7, 0x8868, 0x99E1, 0xAB7A, 0xBAF3,
        0x5285, 0x430C, 0x7197, 0x601E, 0x14A1, 0x0528, 0x37B3, 0x263A,
        0xDECD, 0xCF44, 0xFDDF, 0xEC56, 0x98E9, 0x8960, 0xBBFB, 0xAA72,
        0x6306, 0x728F, 0x4014, 0x519D, 0x2522, 0x34AB, 0x0630, 0x17B9,
        0xEF4E, 0xFEC7, 0xCC5C, 0xDDD5, 0xA96A, 0xB8E3, 0x8A78, 0x9BF1,
        0x7387, 0x620E, 0x5095, 0x411C, 0x35A3, 0x242A, 0x16B1, 0x0738,
        0xFFCF, 0xEE46, 0xDCDD, 0xCD54, 0xB9EB, 0xA862, 0x9AF9, 0x8B70,
        0x8408, 0x9581, 0xA71A, 0xB693, 0xC22C, 0xD3A5, 0xE13E, 0xF0B7,
        0x0840, 0x19C9, 0x2B52, 0x3ADB, 0x4E64, 0x5FED, 0x6D76, 0x7CFF,
        0x9489, 0x8500, 0xB79B, 0xA612, 0xD2AD, 0xC324, 0xF1BF, 0xE036,
        0x18C1, 0x0948, 0x3BD3, 0x2A5A, 0x5EE5, 0x4F6C, 0x7DF7, 0x6C7E,
        0xA50A, 0xB483, 0x8618, 0x9791, 0xE32E, 0xF2A7, 0xC03C, 0xD1B5,
        0x2942, 0x38CB, 0x0A50, 0x1BD9, 0x6F66, 0x7EEF, 0x4C74, 0x5DFD,
        0xB58B, 0xA402, 0x9699, 0x8710, 0xF3AF, 0xE226, 0xD0BD, 0xC134,
        0x39C3, 0x284A, 0x1AD1, 0x0B58, 0x7FE7, 0x6E6E, 0x5CF5, 0x4D7C,
        0xC60C, 0xD785, 0xE51E, 0xF497, 0x8028, 0x91A1, 0xA33A, 0xB2B3,
        0x4A44, 0x5BCD, 0x6956, 0x78DF, 0x0C60, 0x1DE9, 0x2F72, 0x3EFB,
        0xD68D, 0xC704, 0xF59F, 0xE416, 0x90A9, 0x8120, 0xB3BB, 0xA232,
        0x5AC5, 0x4B4C, 0x79D7, 0x685E, 0x1CE1, 0x0D68, 0x3FF3, 0x2E7A,
        0xE70E, 0xF687, 0xC41C, 0xD595, 0xA12A, 0xB0A3, 0x8238, 0x93B1,
        0x6B46, 0x7ACF, 0x4854, 0x59DD, 0x2D62, 0x3CEB, 0x0E70, 0x1FF9,
        0xF78F, 0xE606, 0xD49D, 0xC514, 0xB1AB, 0xA022, 0x92B9, 0x8330,
        0x7BC7, 0x6A4E, 0x58D5, 0x495C, 0x3DE3, 0x2C6A, 0x1EF1, 0x0F78
        ]


    def _crc16(self, data, crc, table):
        """Calculate CRC16 using the given table.
        `data`      - data for calculating CRC, must be bytes
        `crc`       - initial value
        `table`     - table for caclulating CRC (list of 256 integers)
        Return calculated value of CRC
        """
        for byte in data:
            crc = (crc >> 8) ^ table[(crc ^ byte) & 0xff]

        crc = (crc & 0xffff) ^ 0xffff  # integer

        #crc = reverse_bit_order((crc).to_bytes(2, 'big'))  # revert crc bit in byte
        crc = self.bytes_to_bitstring((crc).to_bytes(2, 'big'))

        first = crc[:8]

        last = crc[8:]

        crc = last + first  # swap the two crc byte

        return int(crc,2).to_bytes(2,'big')


    def crc16xmodem(self, data, crc=65535):  # 0xffff
        """Calculate CRC-CCITT (XModem) variant of CRC16.
        `data`      - data for calculating CRC, must be bytes
        `crc`       - initial value
        Return calculated value of CRC
        """
        return self._crc16(data, crc, self.CRC16_XMODEM_TABLE)

    def bytes_to_bitstring(self, bytes):

        return bin(int.from_bytes(bytes, 'big'))[2:].rjust(len(bytes)*8,'0')  # converts bytes to string of bits   b'\x04'   ->   "00000100"

    def bitStuffing(self, bitstring):

        consecutives = 0
        for i in range(len(bitstring)):
            if bitstring[i] == '1':
                consecutives += 1
            else: consecutives = 0

            if consecutives == 5:
                bitstring = bitstring[:i+1] + '0' + bitstring[i+1:]

        return bitstring

    def padd_frame(self, frame, length=256):
        return frame.ljust(length, '0')

    def nrz_to_nrzi(self, input):
        prev_nrzi_bit = 0
        length = len(input)
        result = [0]*length

        for i in range(length):
            nrz_bit = input[i]
            
            if nrz_bit == '0':
                nrzi_bit = prev_nrzi_bit ^ 1
            else:
                nrzi_bit = prev_nrzi_bit
            
            result[i] = str(nrzi_bit)
            prev_nrzi_bit = nrzi_bit

        return ''.join(result)

    def reverse_bit_order(self, bytes):

        bitstring = self.bytes_to_bitstring(bytes)

        for i in range(0,len(bitstring),8):
            block = bitstring[i:i+8]
            bitstring = bitstring[:i] + block[::-1] + bitstring[i+8:]

        return bitstring

    def append_bytes_together(self, bytes1, bytes2):
        result = bytearray(bytes1)
        for byte in bytes2:
            result.append(byte)

        return result
    
    def bitstring_to_bytes(self, bitstring):
        result = bytearray()

        for i in range(0, len(bitstring), 8):
            single = int(bitstring[i:i+8],2).to_bytes(1, 'big')
            result = self.append_bytes_together(result, single)

        return result
        
    def build_frame(self):
        global result
        
        preamble = "101010101010101010101010"
        start_flag = "01111110"
        end_flag = start_flag

        bitstring_payload = self.generate_payload(self.longitude, self.latitude)
        int_payload = int(bitstring_payload, 2)
        byte_payload = int_payload.to_bytes(len(bitstring_payload)//8,'big')

        crc = self.crc16xmodem(byte_payload)

        payload_crc = self.append_bytes_together(byte_payload, crc)

        payload_crc = self.reverse_bit_order(payload_crc)

        stuffed_payload = self.bitStuffing(payload_crc)

        padded_frame = self.padd_frame(preamble+start_flag+stuffed_payload+end_flag)

        final_frame = self.nrz_to_nrzi(padded_frame)
        
        result = [k for k in self.bitstring_to_bytes(final_frame)]

    def work(self, input_items, output_items):
    
        #print("Buffer:  "+ str(len(output_items[0])))
        
        time.sleep(1)
        
        global result
        
        self.build_frame()
        
        if len(output_items[0]) >= len(result):
        
            for i in range(len(result)):
                output_items[0][i] = result[i]
            
            output_length = len(result)
            
        else:
            output_length = 0
        
        return output_length
        
