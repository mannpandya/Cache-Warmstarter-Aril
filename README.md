# Cache-Warmstarter-Aril

Cache Warmstarter design by Aril.

It is 128B 2-way set associative cache with 16B line size.

## Files Included
The code is split in 2 files, Main body and the functions file.
```bash
cache_warmstarter.py
utility.py
```
The output hex files are generated upon running the "cache_warmstarter.py"


## Run
```bash
python cache_warmstarter.py --seed 2 --ways 2 --index 4
```
The code runs with a seed value, ways supported and the index (calculated from the given cache specifications) input from the Command Line as an argument.

The code also runs with default values. (No Command line arguments needed)
