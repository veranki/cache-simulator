# Notes Cache Simulator

* allocation of new block
* victim

* Placement Policy
	- Determines where a block can be placed in the cache: any line in cache or restricted to single line.
	- Direct: Restricted to single location,
	- Fully Associative: Any location
	- Set Associative: N-way means can go in N-possible locations
	- Sectored

* Generic Cache
	- Every Cache with x-blocks is an n-way set-associative
		+ Direct Mapped: 1-way set-associative, 1-set has all x-blocks
		+ N-Way Set Associative: x blocks div. into n-sets, 1-set has n-blocks
		+ Fully Associative:  x-blocks-way set associative, x-blocks = x-sets, 1-set has 1-block

* Hit or Miss ?
	- Direct Mapped
		+ Check Index - Match ? No => Miss, Yes =>
		+ Check Tag - Match ? No => Miss(Replace), Yes => Hit
	- Set Associative
		+ Check Index - Match ? No => Miss, Yes =>
		+ Check Tag in all sets - Match ? No => Miss(Replace), Yes => Hit

* Misses:(**3Cs**)
	- Compulsory Misses: Cold misses
	- Conflict Misses: Data was in cache previously, but got evicted
	- Capacity Misses: Occurs due to limited size of cache
	- Can be extended to **4Cs** & **5Cs** Coherence & Coverage misses in multi-processor systems

* Fetch Policy
	- Determines when info. is loaded into the cache.

* Replacement Rule/ Eviction Policy
	- Determines what entries to purge when space is needed for new entry.
	- LRU
	- LFU

* Write Policy
	- Determines how soon info. is written to lower level of mem. hierarchy
	- Is just the cache updated with new data or lower levels of mem. are also updated at same time?
	- Do we allocate a new block in the cache if write misses?
	- Write back vs write through
	- WA vs WNA
	- victim cache
	- Write-Hit Policies:
		+ write-through/store-through: write to M.mem when write is performed to cache
		+ write-back/store-in/copy-back: write to M.mem when block is purged from cache
	- Write-Miss Policies:
		+ write-allocate vs no-write-allocate: If a write misses, do/do not allocate a line in cache for the data written
		+ fetch-on-write vs no-fetch-on-write: Write miss causes/ does not cause block to be fetched from lower level.
		+ write-before-hit vs no-write-before-hit: data is written only after checking tags.