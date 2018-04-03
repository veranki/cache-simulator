# Cache Simulator

A generic cache simulator written in python.

## Running the simulator
	usage: sim_cache.py <BLOCKSIZE> <SIZE> <ASSOC> <REPLACEMENT_POLICY> <WRITE_POLICY> <TRACE_FILE>
	<BLOCKSIZE>          Block size in bytes. Positive Integer, Power of two
	<SIZE>               Total CACHE size in bytes. Positive Integer
	<ASSOC>              Associativity, 1 if direct mapped, N if fully associative
	<REPLACEMENT_POLICY> 0 for LRU, 1 for LFU
	<WRITE_POLICY>       0 for WBWA, 1 for WTNA

## Example 
	$ python cache_sim.py 4 32 4 0 1 gcc_trace.txt
8KB 4-way set-associative cache with 32B block size, LRU replacement policy and WTNA write policy, gcc_trace.txt as input file.

## Interpreting the result
Simulator prints average memory access time, cache statistics and cache contents.

	  ===== Simulator configuration =====
	  L1_BLOCKSIZE:                     4
	  L1_SIZE:                         32
	  L1_ASSOC:                         4
	  L1_REPLACEMENT_POLICY:            0
	  L1_WRITE_POLICY:                  1
	  trace_file:            gcc_trace.txt
	  ===================================
	  
	===== L1 contents =====
	set0:   800026b         8007044         800026c         800026d
	set1:   800026b         8000269         800026c         800026a
	
	  ====== Simulation results (raw) ======
	  a. number of L1 reads:           63640
	  b. number of L1 read misses:     35693
	  c. number of L1 writes:          36360
	  d. number of L1 write misses:    31495
	  e. L1 miss rate:                0.6719
	  f. number of writebacks from L1:     0
	  g. total memory traffic:         72053
	  
	  ==== Simulation results (performance) ====
	  1. average access time:         13.7876 ns
	  
