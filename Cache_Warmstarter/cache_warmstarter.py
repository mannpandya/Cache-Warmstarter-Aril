# Cache Warmstarter Design by Aril
# Developer: Mann Pandya
# Date: 12/18/2020
# Info: Main body of Cache Warmstarter

import sys
import getopt
import random
import string

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
  cache_index = 4   # 00, 01, 10, 11

  my_seed = 2

  # Derive value from command-line arguments and overwrite default.
  argv = sys.argv[1:]

  opts, args = getopt.getopt(argv, "s:w:i:", ["seed=", "ways=", "index="])

  for opt, arg in opts:
    if opt in ['-s', '--seed']:
        my_seed = int(arg)
    elif opt in ['-w', '--ways']:
        way_supported = int(arg)
    elif opt in ['-i', '--index']:
        cache_index = int(arg)

  # random seed generation through command line argument.
  random.seed(my_seed)

  # extraction of Physical Address, Data, tag from the data structure provided.
  phaddr_list_hex = extract_address(DATA)
  phaddr_list_bin = hex_to_bin(phaddr_list_hex)

  index_list = get_index(phaddr_list_bin)

  tag_list = get_tag(phaddr_list_bin)

  dat_list = extract_data(DATA)

  # way randomization to support either of the ways for all 4 sets.
  least_way_used_per_idx = [random.randint(0, way_supported-1)] * cache_index

  # Initializing tag and data values.
  dtag = [["0" for c_idx in range(cache_index)] for ways in range(way_supported)]
  dcache = [["0" for c_idx in range(cache_index)] for ways in range(way_supported)]

  idx_list = []
  local_cnt = 0

  for idx in index_list:
    line = '%010x' % (int(tag_list[local_cnt], 2))  # convert binary tag data to hex with leading zeroes.
    data = dat_list[local_cnt]
    idx_val = int(idx, 2)   # convert index value from Binary to Integer

    for index in range(cache_index):
      if idx_val == index:
        dtag[least_way_used_per_idx[index]][index] = add_valid(line)  # assign tag with the Valid bit set to 1
        dcache[least_way_used_per_idx[index]][index] = data

    idx_list.append(idx)

    # Algorithm for Least way used to determine which way to be used to put the Tag and Data. Universal for 4-way or 8-way set Associative cache.
    if idx in idx_list:
      least_way_used_per_idx[idx_val] = least_way_used_per_idx[idx_val] + 1
      if least_way_used_per_idx[idx_val] == way_supported:
        least_way_used_per_idx[idx_val] = 0

    local_cnt = local_cnt + 1
  
  # Mapping range from A to Z for file creation
  if 0 < way_supported <= 26:
    count_tag = 0
    for alpha in string.ascii_uppercase[:way_supported]:
          with open("dtag"+alpha+".hex", "w+") as tag:
            for line in range(cache_index):
                tag.write(dtag[count_tag][line] + '\n')
          count_tag = count_tag + 1
    tag.close()

    count_cache = 0
    for alpha in string.ascii_uppercase[:way_supported]:
          with open("dcache"+alpha+".hex", "w+") as cache:
            for line in range(cache_index):
                cache.write(dcache[count_cache][line] + '\n')
          count_cache = count_cache + 1
    cache.close()
