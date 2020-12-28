# Cache Warmstarter Design by Aril
# Developer: Mann Pandya
# Date: 12/18/2020
# Info: Main body of Cache Warmstarter

import sys
import random

from utility import extract_address
from utility import hex_to_bin
from utility import get_tag
from utility import get_index
from utility import extract_data
from utility import add_valid

if __name__ == "__main__":
  # Input data structure
  DATA = [
    (0x000_80010050, "aabbccdd_80010040_55667788_99aabbcc"),
    (0x000_80010060, "11223344_80010050_99aabbcc_aabbccdd"),
    (0x000_80410090, "ff000000_80410080_99aabbcc_aabbccdd"),
  ]

  # Cache Parameter constants
  way_supported = 2   # Way A/B
  cache_index = 4     # 00, 01, 10, 11

  # random seed generation through command line argument.
  random.seed(int(sys.argv[1]))     # sys.argv[1] determines the argument after ".py"

  # extraction of Physical Address, Data, tag from the data structure provided.
  phaddr_list_hex = extract_address(DATA)
  phaddr_list_bin = hex_to_bin(phaddr_list_hex)

  index_list = get_index(phaddr_list_bin)

  tag_list = get_tag(phaddr_list_bin)

  dat_list = extract_data(DATA)

  # open the hex files to be written on.
  tagA_write = open("dtagA.hex", 'w+')
  tagB_write = open("dtagB.hex", 'w+')
  dataA_write = open("dcacheA.hex", 'w+')
  dataB_write = open("dcacheB.hex", 'w+')

  # way randomization to support either of the ways for all 4 sets.
  least_way_used_per_idx = [random.randint(0, way_supported-1)] * cache_index

  # Initializing all the tag and data values to be 0 for all 4 sets.
  dtagA = ["0"] * cache_index

  dtagB = ["0"] * cache_index

  dataA = ["0"] * cache_index

  dataB = ["0"] * cache_index

  idx_list = []
  local_cnt = 0

  for idx in index_list:
    line = '%010x' % (int(tag_list[local_cnt], 2))  # convert binary tag data to hex with leading zeroes.

    data = dat_list[local_cnt]

    idx_val = int(idx, 2)   # convert index value from Binary to Integer

    if idx_val == 0:
      if least_way_used_per_idx[idx_val] == 0:
        dtagA[idx_val] = add_valid(line)  # assign tag with the Valid bit set to 1
        dataA[idx_val] = data
      else:
        dtagB[idx_val] = add_valid(line)
        dataB[idx_val] = data
      idx_list.append(idx)

    elif idx_val == 1:
      if least_way_used_per_idx[idx_val] == 0:
        dtagA[idx_val] = add_valid(line)
        dataA[idx_val] = data
      else:
        dtagB[idx_val] = add_valid(line)
        dataB[idx_val] = data
      idx_list.append(idx)

    elif idx_val == 2:
      if least_way_used_per_idx[idx_val] == 0:
        dtagA[idx_val] = add_valid(line)
        dataA[idx_val] = data
      else:
        dtagB[idx_val] = add_valid(line)
        dataB[idx_val] = data
      idx_list.append(idx)

    elif idx_val == 3:
      if least_way_used_per_idx[idx_val] == 0:
        dtagA[idx_val] = add_valid(line)
        dataA[idx_val] = data
      else:
        dtagB[idx_val] = add_valid(line)
        dataB[idx_val] = data
      idx_list.append(idx)

    # Algorithm for Least way used to determine which way to be used to put the Tag and Data. Universal for 4-way or 8-way set Associative cache.
    if idx in idx_list:
      least_way_used_per_idx[idx_val] = least_way_used_per_idx[idx_val] + 1
      if least_way_used_per_idx[idx_val] == way_supported:
        least_way_used_per_idx[idx_val] = 0

    local_cnt = local_cnt + 1

  tagA_lines = []
  tagB_lines = []
  dataA_lines = []
  dataB_lines = []

  for val in range(cache_index):
    tagA_lines.append(dtagA[val] + "\n")
    tagB_lines.append(dtagB[val] + "\n")
    dataA_lines.append(dataA[val] + "\n")
    dataB_lines.append(dataB[val] + "\n")


  # Write into the ".hex" files.
  tagA_write.writelines(tagA_lines)
  dataA_write.writelines(dataA_lines)
  tagB_write.writelines(tagB_lines)
  dataB_write.writelines(dataB_lines)

  tagA_write.close()  # Close the file.









