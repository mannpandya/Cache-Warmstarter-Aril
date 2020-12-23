# Cache Warmstarter Design by Aril
# Developer: Mann Pandya
# Date: 12/18/2020
# Info: Functions used in Cache Warmstarter


# Extract Address from the data structure with Leading Zeroes.
def extract_address(list_tuples):
  if len(list_tuples) == 0:
    pass
  else:
    addr_list = []
    for address in list_tuples:
      addr_list.append('%011x' % (address[0]))
    return addr_list


# Extract Data from the data structure
def extract_data(list_tuples):
  if len(list_tuples) == 0:
    pass
  else:
    data_list = []
    for data in list_tuples:
      data_list.append(data[1])
    return data_list


# Hex to Binary conversion with leading Zeroes.
def hex_to_bin(hex_list):
  bin_list = []
  for hex_num in hex_list:
    bin_num = bin(int('1' + hex_num, 16))[3:]
    bin_list.append(bin_num)
  return bin_list


# Extract the Index bits from the Physical Address extracted
def get_index(bin_list):
  index = []
  for bin_num in bin_list:
    binary = bin_num
    end = len(binary) - 5
    start = end - 2 + 1
    index.append(binary[start:end+1])
  return index


# Extract Tag bits from the Physical Address, and add external Valid bit.
def get_tag(bin_list):
  tag = []
  for bin_num in bin_list:
    binary = bin_num
    tag_add = "0"
    end = len(binary) - 7
    tag.append(tag_add + binary[:end+1])
  return tag


# Set the Valid bit and append back to the Tag.
def add_valid(tag_data):
  val = list(bin(int('1' + tag_data, 16))[3:])
  val[1] = "1"
  val = "".join(val)
  val = '%010x' % (int(val, 2))
  return val
