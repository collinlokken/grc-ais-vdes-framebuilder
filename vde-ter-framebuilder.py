"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import time


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block"""

    def __init__(self, LinkID=11, VDEMessage='0101000000001110101101111001101000101010011101011011110011010001011000100000000000000000001100100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='VDE-TER Framebuilder',   # will show up in GRC
            in_sig=None,
            out_sig=[np.byte]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        #self.example_param = example_param

        self.VDEMessage = VDEMessage
        self.LinkID = LinkID 
        '''Link ID should only be 11, 17, 19. 5 is only included, because we could not find
        examples of any other link ID frame generation. In order to validate the code, it was 
        neccessary to include link ID 5, the code also consists of modulation, so if link ID 19 
        is used, the code does not work, according to the technical specifications in ITU'''
    
    linkID_datagram_length = {11: 400, 17: 1840, 19: 5584, 5:256} #Datagram length that was determined by subtracting 32 from the FEC input
    

    def append_padding(self, LinkID, message, linkID_datagram_length):
        #only take account for messages shorter then the datagram. Fragmentation is not taken into account
        datagram_length = linkID_datagram_length[LinkID]
        if datagram_length != len(message):
            message = message + '0'*(datagram_length-len(message))
        return message
    
    #table and crc32 code from https://gist.github.com/Miliox/b86b60b9755faf3bd7cf
    CRC32_MPEG_TABLE = [
        0x00000000, 0x04c11db7, 0x09823b6e, 0x0d4326d9,
      0x130476dc, 0x17c56b6b, 0x1a864db2, 0x1e475005,
      0x2608edb8, 0x22c9f00f, 0x2f8ad6d6, 0x2b4bcb61,
      0x350c9b64, 0x31cd86d3, 0x3c8ea00a, 0x384fbdbd,
      0x4c11db70, 0x48d0c6c7, 0x4593e01e, 0x4152fda9,
      0x5f15adac, 0x5bd4b01b, 0x569796c2, 0x52568b75,
      0x6a1936c8, 0x6ed82b7f, 0x639b0da6, 0x675a1011,
      0x791d4014, 0x7ddc5da3, 0x709f7b7a, 0x745e66cd,
      0x9823b6e0, 0x9ce2ab57, 0x91a18d8e, 0x95609039,
      0x8b27c03c, 0x8fe6dd8b, 0x82a5fb52, 0x8664e6e5,
      0xbe2b5b58, 0xbaea46ef, 0xb7a96036, 0xb3687d81,
      0xad2f2d84, 0xa9ee3033, 0xa4ad16ea, 0xa06c0b5d,
      0xd4326d90, 0xd0f37027, 0xddb056fe, 0xd9714b49,
      0xc7361b4c, 0xc3f706fb, 0xceb42022, 0xca753d95,
      0xf23a8028, 0xf6fb9d9f, 0xfbb8bb46, 0xff79a6f1,
      0xe13ef6f4, 0xe5ffeb43, 0xe8bccd9a, 0xec7dd02d,
      0x34867077, 0x30476dc0, 0x3d044b19, 0x39c556ae,
      0x278206ab, 0x23431b1c, 0x2e003dc5, 0x2ac12072,
      0x128e9dcf, 0x164f8078, 0x1b0ca6a1, 0x1fcdbb16,
      0x018aeb13, 0x054bf6a4, 0x0808d07d, 0x0cc9cdca,
      0x7897ab07, 0x7c56b6b0, 0x71159069, 0x75d48dde,
      0x6b93dddb, 0x6f52c06c, 0x6211e6b5, 0x66d0fb02,
      0x5e9f46bf, 0x5a5e5b08, 0x571d7dd1, 0x53dc6066,
      0x4d9b3063, 0x495a2dd4, 0x44190b0d, 0x40d816ba,
      0xaca5c697, 0xa864db20, 0xa527fdf9, 0xa1e6e04e,
      0xbfa1b04b, 0xbb60adfc, 0xb6238b25, 0xb2e29692,
      0x8aad2b2f, 0x8e6c3698, 0x832f1041, 0x87ee0df6,
      0x99a95df3, 0x9d684044, 0x902b669d, 0x94ea7b2a,
      0xe0b41de7, 0xe4750050, 0xe9362689, 0xedf73b3e,
      0xf3b06b3b, 0xf771768c, 0xfa325055, 0xfef34de2,
      0xc6bcf05f, 0xc27dede8, 0xcf3ecb31, 0xcbffd686,
      0xd5b88683, 0xd1799b34, 0xdc3abded, 0xd8fba05a,
      0x690ce0ee, 0x6dcdfd59, 0x608edb80, 0x644fc637,
      0x7a089632, 0x7ec98b85, 0x738aad5c, 0x774bb0eb,
      0x4f040d56, 0x4bc510e1, 0x46863638, 0x42472b8f,
      0x5c007b8a, 0x58c1663d, 0x558240e4, 0x51435d53,
      0x251d3b9e, 0x21dc2629, 0x2c9f00f0, 0x285e1d47,
      0x36194d42, 0x32d850f5, 0x3f9b762c, 0x3b5a6b9b,
      0x0315d626, 0x07d4cb91, 0x0a97ed48, 0x0e56f0ff,
      0x1011a0fa, 0x14d0bd4d, 0x19939b94, 0x1d528623,
      0xf12f560e, 0xf5ee4bb9, 0xf8ad6d60, 0xfc6c70d7,
      0xe22b20d2, 0xe6ea3d65, 0xeba91bbc, 0xef68060b,
      0xd727bbb6, 0xd3e6a601, 0xdea580d8, 0xda649d6f,
      0xc423cd6a, 0xc0e2d0dd, 0xcda1f604, 0xc960ebb3,
      0xbd3e8d7e, 0xb9ff90c9, 0xb4bcb610, 0xb07daba7,
      0xae3afba2, 0xaafbe615, 0xa7b8c0cc, 0xa379dd7b,
      0x9b3660c6, 0x9ff77d71, 0x92b45ba8, 0x9675461f,
      0x8832161a, 0x8cf30bad, 0x81b02d74, 0x857130c3,
      0x5d8a9099, 0x594b8d2e, 0x5408abf7, 0x50c9b640,
      0x4e8ee645, 0x4a4ffbf2, 0x470cdd2b, 0x43cdc09c,
      0x7b827d21, 0x7f436096, 0x7200464f, 0x76c15bf8,
      0x68860bfd, 0x6c47164a, 0x61043093, 0x65c52d24,
      0x119b4be9, 0x155a565e, 0x18197087, 0x1cd86d30,
      0x029f3d35, 0x065e2082, 0x0b1d065b, 0x0fdc1bec,
      0x3793a651, 0x3352bbe6, 0x3e119d3f, 0x3ad08088,
      0x2497d08d, 0x2056cd3a, 0x2d15ebe3, 0x29d4f654,
      0xc5a92679, 0xc1683bce, 0xcc2b1d17, 0xc8ea00a0,
      0xd6ad50a5, 0xd26c4d12, 0xdf2f6bcb, 0xdbee767c,
      0xe3a1cbc1, 0xe760d676, 0xea23f0af, 0xeee2ed18,
      0xf0a5bd1d, 0xf464a0aa, 0xf9278673, 0xfde69bc4,
      0x89b8fd09, 0x8d79e0be, 0x803ac667, 0x84fbdbd0,
      0x9abc8bd5, 0x9e7d9662, 0x933eb0bb, 0x97ffad0c,
      0xafb010b1, 0xab710d06, 0xa6322bdf, 0xa2f33668,
      0xbcb4666d, 0xb8757bda, 0xb5365d03, 0xb1f740b4
        ]
    '''
    def crc32xmodem(self, data, crc=0xFFFFFFFF):  # 0xffff
        """Calculate CRC-CCITT (XModem) variant of CRC16.
        `data`      - data for calculating CRC, must be bytes
        `crc`       - initial value
        Return calculated value of CRC
        """
        return self._crc32(data, self.CRC32_MPEG_TABLE, crc)
    '''
    
    def _crc32(self, data, CRC32_MPEG_TABLE, crc=0xFFFFFFFF):

        """Calculate CRC16 using the given table.
        `data`      - data for calculating CRC, must be bytes
        `crc`       - initial value
        `table`     - table for caclulating CRC (list of 256 integers)
        Return calculated value of CRC in bin format. 
        """
        table = CRC32_MPEG_TABLE
        for byte in data: 
            crc = (crc << 8) ^ table[((crc >> 24) ^ byte) & 0xFF]
        
        #Take last 32 bits of the value 
        crc = (crc & 0xFFFFFFFF)
        
        #turn into binary
        #crc = format(crc, 'b') wrong
        crc = crc = '{0:b}'.format(crc).rjust(32,'0') #use to append 0 padding at the start
        return crc
    #Thanks to https://github.com/Michaelangel007/crc32 for demystifiying crc32
    #After the payload has been padded and appended a crc32 value, turbo encoding need to be done accordingly

    permutation_primes = {5: [47,17,233,127,239,139,199,163],
                          11: [127,191,241,5,83,109,107,179],
                          17: [211,61,227,239,181,79,73,193],
                          19: [137,101,223,41,67,131,61,47]} #List of permuatationn primes associated with a link ID
    k1_k2 = {5: [2,144],
             11: [2,216],
             17: [6,312],
             19: [16,351]} #k values associated with different link IDs

    def calculate_permutation(self,s, k1, k2, primes):
        '''
        Calculate the permutation numbers for s = (1,...,k)
        The operations are from the ITU specification for VDES.
        '''
        m = (s - 1) % 2
        i = ((s - 1) // (2*k2))
        j = ((s - 1) // 2) - i*k2
        t = (19*i + 1) % int((k1/2))
        q = t % 8 + 1
        c = (primes[q-1]*j + 21*m) % k2
        pi_s = 2*(t + c*k1//2 + 1) - m
        return int(pi_s)

    def interleave(self, input, k1, k2, primes):
        #create an empty list to contain the permutated indices
        permuted_indices = []
        #iterate with s values from 1-k, and use this to compute the permutated indice
        for s in range(1,k1*k2+1):
            #append the new permutated indices:
            #indices are from 1-k.
        
            permuted_indices.append(self.calculate_permutation(s,k1,k2,primes))
            #print(s)

        #check for duplicates in permuted indics
        if len(set(permuted_indices))!=len(permuted_indices):
            print("something is wrong, an duplication exists")
    
        #Generate a list of 0 same length as input. 
        interleaved_list = [0] * len(input)
        #print(interleaved_list)
        i = 0
        for permuted_indice in permuted_indices:
            #s bit read out should be pi(s), so if pi(1)=2 then input(2) should be the first 
            interleaved_list[i] = input[permuted_indice-1]
            i += 1
        
        interleaved_string = ''.join(interleaved_list)
        
        return interleaved_string



    def rsc_encode(self, input):
        '''
        Contains the Recursive Systematic Convultional (RSC) as described in the technical 
        specification of VDES. See https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.2092-1-202202-I!!PDF-E.pdf, 
        Annex 2 for more information
        '''
        #Initialize the feedback register, should allways start start with 0 in each register
        D = [0, 0, 0]
        

        #prepare output lists
        X = []
        Y1 = []
        Y2 = []
        xor = 0
        #Turn string into bits
        input_bits =[]
        
        for bit in input:
            input_bits.append(int(bit))

        # Iterate over input bits
        for bit in input_bits:
            #Compute first xor operations
            xor = D[2]^D[1]^bit


            # Calculate output bits
            x = bit
            y1 = xor ^ D[0] ^ D[2]
            y2 =  xor ^ D[0] ^ D[1] ^ D[2]

            #update the feedback register
            D.insert(0, xor)
            D.pop()
            #append the output bits to the appropriate list
            X.append(x)
            Y1.append(y1)
            Y2.append(y2)
        
        # After all the bits have been read in, the next step is to calculate the tail pattern. In this case no bit is shifted
        # in so the encoding need to be changed accordingly. The RSC calculates the final string correctly, without the tail bits. 
        # The next step is to figure out the corresponding tail bits. After k clocks. that is 288 in the test examples, and might
        # vary depenging on the link layer ID. For the 6 subsequent clocks, the switch is moved from position A to position B. 
        # This is done to ensure, that the shift register contains 3 0's. The tails are then 
        # Appended according to the tail puncturing pattern associated with a given link ID. 

        #prepare tail lists
        X_tail = []
        Y1_tail = []
        Y2_tail = []


        #print(D)
        for i in range(0,3):
            xor1 = D[1]^D[2]
            xor = xor1^xor1

            #compute the output bits for the tail
            x_tail = xor1
            y1_tail = xor ^ D[0] ^ D[2]
            y2_tail =  xor ^ D[0] ^ D[1] ^ D[2]
            #update the feedback register
            D.insert(0, xor)
            D.pop()
            #append output bits to the appropriate tail list
            X_tail.append(x_tail)
            Y1_tail.append(y1_tail)
            Y2_tail.append(y2_tail)

        #print(D)
        return X, Y1, Y2, X_tail, Y1_tail, Y2_tail
    
    puncture_pattern = {5: [[1,0,1,0,0,0], [1,0,0,0,0,0], [1,0,0,0,0,0], [1,0,0,0,0,0], [1,0,0,0,0,0], [1,0,0,0,0,1]],
                        11: [[1,1,0,0,0,0], [1,0,0,0,1,0]],
                        17: [[1,1,0,0,0,0], [1,0,0,0,1,0]],
                        19: [[1,0,1,0,0,0], [1,0,0,0,0,0], [1,0,0,0,0,0], [1,0,0,0,0,0], [1,0,0,0,0,0], [1,0,0,0,0,1]]}#puncture pattern for the k first clocks for linkIDs
    
    puncture_pattern_tail = {5: [[1,0,1,0,0,0], [1,0,1,0,0,0], [1,0,0,0,0,0], [0,0,0,1,0,1], [0,0,0,1,0,1], [0,0,0,1,0,0]],
                             11: [[1,1,0,0,0,0], [1,1,0,0,0,0], [1,0,0,0,0,0], [0,0,0,1,1,0], [0,0,0,1,1,0], [0,0,0,1,0,0]],
                             17: [[1,1,0,0,0,0], [1,1,0,0,0,0], [1,0,0,0,0,0], [0,0,0,1,1,0], [0,0,0,1,1,0], [0,0,0,1,0,0]],
                             19: [[1,0,1,0,0,0], [1,0,1,0,0,0], [1,0,1,0,0,0], [0,0,0,1,0,1], [0,0,0,1,0,1], [0,0,0,1,0,1]]}#puncture pattern for the 6 last clocks

    def puncturing(self, puncture_pattern, x, y0, y1, x_, y0_, y1_):
        '''
        Each RSC encoder produces three outputs per input bit. The first encoder produces
        x,y0,y1 and the second x',y0',y1'. The output should then be output if the puncture
        pattern contains 1, and be discarded if the puncture pattern is 0. The resulting output
        should be output in the following sequence: x,y0,y1,x',y0',y1'.  
        '''
        s = ""
        p = 0
        for i in range(len(x)):
            if puncture_pattern[p][0] == 1:
                s += str(x[i])
            if puncture_pattern[p][1] == 1:
                s += str(y0[i])
            if puncture_pattern[p][2] == 1:
                s += str(y1[i])
            if puncture_pattern[p][3] == 1:
                s += str(x_[i])
            if puncture_pattern[p][4] == 1:
                s += str(y0_[i])
            if puncture_pattern[p][5] == 1:
                s += str(y1_[i])
            
            p+=1
            if p == len(puncture_pattern):
                p = 0

        return s

    def puncturing_tail(self, puncture_pattern, x_tail, y0_tail, y1_tail, x_per_tail, y0_per_tail, y1_per_tail):
        '''
        After the entire input and interleaved string have been encoded and punctured, 
        switch in the RSC is switched. For the next three clocks only encoder 1 outputs data. 
        For the sequent 3 clocks only the second encoder should output data. 
        Depending on the pucnture pattern the first x bits should therefore be from encoder 1
        and the last x bits should be from encoder 2. 
        '''
        s = ""
        p = 0
        test = ""
        for i in range(len(x_tail)):
            if puncture_pattern[p][0] == 1:
                s += str(x_tail[i])
                test = test + 'x'
            if puncture_pattern[p][1] == 1:
                s += str(y0_tail[i])
                test = test + 'y0'
            if puncture_pattern[p][2] == 1:
                s += str(y1_tail[i])
                test = test + 'y1'
            p += 1
            
            
        for i in range(len(x_per_tail)): 
            if puncture_pattern[p][3] == 1:
                s += str(x_per_tail[i])
                test += "x'"
            if puncture_pattern[p][4] == 1:
                s += str(y0_per_tail[i])
                test += "y0'"
            if puncture_pattern[p][5] == 1:
                s += str(y1_per_tail[i])
                test += "y1'"
            p += 1

        #print(test)
        return s
    
    def bitscrambling(self, input_bits):
        #Initialize the initialization squence according to the ITU specification
        init_sequence = [1,0,0,1,0,1,0,1,0,0,0,0,0,0,0]

        #initialize empty output string
        output_bits = ''
        for bit in input_bits:
            input_bit = int(bit)
            
            #compute the feedback bit by XORing the specified bits in the polynomial, namely xor bit 14 and 15 from lfsr
            feedback_bit = 0
            feedback_bit = init_sequence[len(init_sequence)-2]^init_sequence[len(init_sequence)-1]
            
            #Update the initialization sequence, inserting the feedback bit at the left
            init_sequence.pop()
            init_sequence.insert(0, feedback_bit)
            
            #XOR the input bit with the feedback bit
            output_bit = input_bit ^ feedback_bit
            #append the output bit to the output string
            output_bits += str(output_bit)
        
        return output_bits
    
    
    def bitstring_to_bytes(self, bitstring):
        '''Turn bitstring to bytes from the ais frame builder'''
        result = bytearray()

        for i in range(0, len(bitstring), 8):
            single = int(bitstring[i:i+8],2).to_bytes(1, 'big')
            result = self.append_bytes_together(result, single)

        return result
    
    
    def append_bytes_together(self, bytes1, bytes2):
        '''Append bytes together from the ais frame builder'''
        result = bytearray(bytes1)
        for byte in bytes2:
            result.append(byte)

        return result
    
    #Dictionary containing vde-ter identification code for some linkID's
    
    linkID_identification_code = {5:'11010101111011010111111010111111',
                                  11:'11101101001011101100001001111100',
                                  17:'10000111001101110010010011100101',
                                  19:'10001111010010000010010000011010'}
                                  
    linkID_reverse = {11:'10110111011101000100001100111110',
                      17:'11100001111011000010010010100111',
                      19:'11110001000100100010010001011000'}
    
    mapping_purple = {'00': [-1,0],
                  '01': [0,1],
                  '10': [0,-1],
                  '11':[1,0]}#QPSK mapping from the ITU, purple points
    
    mapping_green = {'11': [0.7,0.7],
                 '01': [-0.7,0.7],
                 '00': [-0.7, -0.7],
                 '10': [0.7, -0.7]}#QPSK mapping from ITU, green points
    
    
    def compute_mapping_bytes(self,final):
        
        tmp = ""
        x = 0
        mapping = []
        for i in range(0,len(final)-1,2): #For every 2 bit
            #append the second bit
            tmp = final[i]+final[i+1]
            if x%2 == 0:
                #map every even bit index to green
                mapping.append(self.mapping_green[tmp])
            else: 
                #map every odd bit index to purple
                mapping.append(self.mapping_purple[tmp])
            x+= 1
        
            
        return mapping
    
    
    def bytes_to_bitstring(self, bytes):
        #turn byte to bitstring form ais framebuilder
        return bin(int.from_bytes(bytes, 'big'))[2:].rjust(len(bytes)*8,'0')
        
        
    def reverse_bit_order(self, bytes):
        #Reverse the bit order for a byte to ensure correct endiannes, from ais framebuilder
        bitstring = self.bytes_to_bitstring(bytes)

        for i in range(0,len(bitstring),8):
            block = bitstring[i:i+8]
            bitstring = bitstring[:i] + block[::-1] + bitstring[i+8:]

        return bitstring
                               
    
    def build_frame(self):
        #Syncword sequence for asm-ter and vde-ter
        syncword = '111111001101010000011001010'
        #1 maps to (1 1)
        #0 maps to (0,0)
        linkID_code = self.linkID_identification_code[self.LinkID]

        #append padding according to the linkID datagram length
        padded_input = self.append_padding(self.LinkID, self.VDEMessage, self.linkID_datagram_length)
        
        #compute crc
        
        
        int_payload = int(padded_input,2)
	
        byte_payload = int_payload.to_bytes(len(padded_input)//8, 'big')

        crc = self._crc32(byte_payload, self.CRC32_MPEG_TABLE)

        #append crc
        
        payload_crc = padded_input + crc
        
        #If linkID, 11, 17 or 19, apply endianess
        
        if self.LinkID != 5:
            #turn bitstring into bytes
            int_payload = int(payload_crc,2)
            byte_payload = int_payload.to_bytes(len(payload_crc)//8,'big')
            
            #reverse the bit order of the byte
            payload_crc = self.reverse_bit_order(byte_payload)
            #append the reverse bit order for each byte for syncword and link ID
            syncword = '001111110010101110011000010' 
            linkID_code = self.linkID_reverse[self.LinkID]
        
        
        

        #rearrange the input, according to the link ID parameters

        rearranged_input = self.interleave(payload_crc, self.k1_k2[self.LinkID][0], self.k1_k2[self.LinkID][1],self.permutation_primes[self.LinkID])

        #Compute the output for the RSC encoder, for the payload_crc and rearranged input

        x, y0, y1, x_tail, y0_tail, y1_tail  = self.rsc_encode(payload_crc)

        x_per, y0_per, y1_per, x_per_tail, y0_per_tail, y1_per_tail = self.rsc_encode(rearranged_input)  

        #compute the output data, using the puncturing pattern

        turbo_encoded_output = self.puncturing(self.puncture_pattern[self.LinkID], x, y0, y1, x_per, y0_per, y1_per)
        
        #print(turbo_encoded_output=="001010000000000010110101111011111000110010000101110100111010101111011110010110100000101010000101000000000100000101000001101001000100000100000000000000010100000001000000010000000000000001000000000000000000000001000001010000000100000100000001010000010000000100000001010000000100000001000000000000010100000000000001000000010100000101000000010000010011011011100010100000011011011001101011")

        #compute the tail bits

        tailbits = self.puncturing_tail(self.puncture_pattern_tail[self.LinkID], x_tail, y0_tail, y1_tail, x_per_tail, y0_per_tail, y1_per_tail)
        
        

        #append the tail bits to the turbo encoded output

        turbo_encoding_done = turbo_encoded_output + tailbits

        #scramble the data

        scrambled_data = self.bitscrambling(turbo_encoding_done)
        

        syncword_2x = ""
        
        #double every digit in syncword, since 1 maps to qpsk(1 1), and 0 maps to qpsk(0 0)
        for bit in syncword:
                syncword_2x += 2*(bit)
                
        
        final = syncword_2x + linkID_code + scrambled_data
        
        print(scrambled_data)
        print("done")
        
        
        #mapping = self.compute_mapping_bytes(final)
        
        #print(mapping)
        
        tmp = ""
        extra_bit = "" 
        x = 0
        for i in range(0,len(final)-1,2):
            tmp = final[i]+final[i+1]
            if x%2 == 0:
                #mapping.append(mapping_green[tmp])
                tmp += "0"
                #print(tmp)
                extra_bit = extra_bit + tmp
            else:
                #mapping.append(mapping_purple[tmp])
                tmp += "1"
                extra_bit = extra_bit + tmp
            x += 1

        #11011111011111011100000111011100011100011100000100000100011111000100011100011100011101001

        #where the syncword bits are 11x or 00x, where x states if it is to be mapped to green or purple. 

        #linkword and scrambled data is 00x, 01x, 10x, 11x,

        #(len(extra_bit)==len(final)*3/2)

        
        
        #print(mapping)
        
	
        
        return extra_bit

    

    def work(self, input_items, output_items):
        
        time.sleep(5)

        final_frame = self.build_frame()
        
        final_frame = [k for k in self.bitstring_to_bytes(final_frame)]


        if len(output_items[0]) >= len(final_frame):
        
            for i in range(len(final_frame)):
                output_items[0][i] = final_frame[i]
            
            output_length = len(final_frame)
            
        else:
            output_length = 0
        
        return output_length
