Cache Warmstarter Design
========================
Goal: initialize CPU cache memories to a warmed-up state before
starting simulation.

How: create a series of *.hex files, one per RAM, which the testbench
will load at simulation startup via $readmemh().

Cache Configuration
-------------------
The data cache is 128 bytes, 2-way set associative, 16 byte line
size. Each way is composed of two RAMs: tag and data, with 4 entries
each.

The design looks up an entry in the cache based on a 44-bit physical
address like so:

* paddr[3:0]: offset within line
* paddr[5:4]: index into cache arrays
* paddr[43:6]: tag

Each tag is 39 bits wide:
* tag[38]: valid
* tag[37:0]: paddr[43:6]

Input
-----
A Python data structure: list of tuples of (address, data_string). For example:

```
DATA = [
    (0x000_80010050, "aabbccdd_80010040_55667788_99aabbcc"),
    (0x000_80010060, "11223344_80010050_99aabbcc_aabbccdd"),
    (0x000_80410090, "ff000000_80410080_99aabbcc_aabbccdd"),
]
```

Output
------
Four files, each with 4 lines of hex numbers:
* dtagA.hex
* dtagB.hex
* dcacheA.hex
* dcacheB.hex

Each line in each file corresponds to a set in the cache: line 1 of
each file is set 0, line 2 of each file is set 1, etc. A/B are the
two ways.

Possible output for the sample input provided above:

dtagA.hex:
```
0
4002000401
4002000401
0
```
dcacheA.hex:
```
0
aabbccdd_80010040_55667788_99aabbcc
11223344_80010050_99aabbcc_aabbccdd
0
```
dtagB.hex:
```
0
4002010402
0
0
```
dcacheB.hex:
```
0
ff000000_80410080_99aabbcc_aabbccdd
0
0
```


Evaluation Criteria
-------------------
1. Correctness: no lines should be in an incorrect index; the cache
should be as full as possible.

2. Maintainability: the code should be easy to understand; changes to
cache parameters should be relatively straightforward.

Bonus Points
------------
1. Show your work on github (or similar).

2. Randomize way selection. It must be repeatable, based on a seed
value accepted via command-line argument.

3. Accept a "hit percent" value via command-line argument, and
randomly leave out some lines based on this, which will trigger more
cache misses during simulation.
