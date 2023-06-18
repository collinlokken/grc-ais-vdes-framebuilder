


def short_data_message(sourceID, destinationID, text):
    type = '{0:b}'.format(92).rjust(8,'0') #set to 74, 1 byte syze
    #length, total size in bytes, variable, set at last
    #source ID, provided automaticcaly by AIS. Uniquely identified
    #numerical identifier. according to https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.585-9-202205-I!!PDF-E.pdf
    #M_1 I_2 D_3 X_4 .... X_9
    #MID represent maritime identification digits
    #X_4 .... X_9 any value from 0 to 9. 
    #dont have access to any, 123456789 is used to examplify, as in ASM messages
    sourceID = '{0:b}'.format(sourceID).rjust(32, '0')
    
    sessionID = '{0:b}'.format(0).rjust(8, '0') #set for future use
    
    destinationID = '{0:b}'.format(destinationID).rjust(32, '0') #MMSI 9 digit number
    
    #number of fragments: 1-14, I suppuse if only the start fragment is sent set to 1
    #nr_fragment = '{0:b}'.format(1).rjust(8, '0')
    
    #fragment_nr = '{0:b}'.format(0).rjust(8, '0') #start at 0 index, increment with 1
    
    retrans_nr = '{0:b}'.format(0).rjust(8, '0')  #star with 0, increment every retransmission

    variable = encode_string(text)

    variable = text_using_6_bit_ascii(variable,0,1)

    length_1 = len(type+sourceID+sessionID+
                   destinationID+retrans_nr+
                   variable)

    length_1_bin = '{0:b}'.format(length_1)

    length = length_1 +len(length_1_bin)

    length = '{0:b}'.format(length).rjust(2,'0')

    return(type+length+sourceID
           +sessionID+destinationID+retrans_nr+
           variable)

'''Generate payload to be sent in the start fragment'''

def text_using_6_bit_ascii(text, text_sequence_nr, last_sequence):

    vpfi = '{0:b}'.format(2).rjust(16,'0') #identification of the content
    
    messageID = '{0:b}'.format(0).rjust(16,'0')
    
    ack_req = '{0:b}'.format(0).rjust(1,'0') #1 for required, 0 for not required

    #value from 0-3, nr of retries, sets it to 0 since its not resent https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.1371-5-201402-I!!PDF-E.pdf annex 2: 5.3.1
    sequence_nr = '{0:b}'.format(0).rjust(2,'0')

    text_sequence_nr_bin = '{0:b}'.format(text_sequence_nr).rjust(11,'0') #sequence nr to be incremented, if only one all 0s, set to 0 in this case

    last_sequence = '{0:b}'.format(last_sequence).rjust(1,'0') #set to 1 if this is the last message in the sequenc

    #text string: shoudl be 6-bit ascii encoded as defined in ITU-R M.1371-5, Table 47 Annex 8.

    text_string = encode_string(text)

    spare_bits = len(text_string)%8
    
    spare_bits = '{0:b}'.format(0).rjust(spare_bits,'0') #byte boundary padding, 
        
    almost_done = vpfi+messageID+ack_req+sequence_nr+text_sequence_nr_bin+last_sequence+text_string+spare_bits

    total_number_bits = '{0:b}'.format(len(almost_done))

    return almost_done+total_number_bits



    



#copied from AIS_TX, AIVDM encoder: https://github.com/trendmicro/ais/blob/master/AIVDM_Encoder.py
def encode_string(string):
	vocabolary = "@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^- !\"#$%&'()*+,-./0123456789:;<=>?"
	encoded_string = ""
	for c in string.upper():
		index = vocabolary.find(c)
		encoded_string += '{0:b}'.format(index).rjust(6,'0')
	return encoded_string


print(short_data_message(123456789, 987654321, 'Test'))


print(len('010111001001010010000011101011011110011010001010100000000001110101101111001101000101100010000000000000000000000100000000000000000000000000000001110000110001110000110001110000110000110000110000110000110001110000110001110000110001110000110000110001110001110000110001110000110001110000110000011000000'))
