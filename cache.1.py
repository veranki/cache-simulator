import math
from trace_parse import traceParse
##################################################################
# defining cache class & methods
##################################################################


class Cache(object):
    def __init__(self, blockSize, cacheSize, associativity, replacementPolicy, writePolicy):
        self.config = {}
        self.config['blockSize'] = blockSize
        self.config['cacheSize'] = cacheSize
        self.config['associativity'] = associativity
        self.config['replacementPolicy'] = replacementPolicy
        self.config['writePolicy'] = writePolicy
        self.config['numBlocks'] = cacheSize / blockSize
        self.config['numWays'] = associativity
        self.config['numSets'] = cacheSize / (blockSize * associativity)

        # cache variables
        self.stats = {}
        self.stats['Reads'] = 0
        self.stats['ReadHits'] = 0
        self.stats['ReadMisses'] = 0
        self.stats['Writes'] = 0
        self.stats['WriteHits'] = 0
        self.stats['WriteMisses'] = 0
        self.stats['WriteBacks'] = 0
        self.stats['MemTraffic'] = 0

        # state matrices
        self.rows = self.config['numSets']
        self.cols = self.config['numWays']
        self.TAG_MAT = [([long(1)] * self.cols) for row in xrange(self.rows)]
        self.VALID_MAT = [([0] * self.cols) for row in xrange(self.rows)]
        self.DIRTY_MAT = [([0] * self.cols) for row in xrange(self.rows)]
        self.LRU_MAT = [([0] * self.cols) for row in xrange(self.rows)]
        self.LFU_MAT = [([0] * self.cols) for row in xrange(self.rows)]

    # TODO: issue read function
    def issueRead(self, address):
        self.stats['MemTraffic'] += 1
        return None

    # TODO: issue write function
    def issueWrite(self, address):
        self.stats['MemTraffic'] += 1
        return None

    def decodeAddress(self, address):
        # calclating length of tag, index & offset from cache configuration
        lenAddr = 32
        lenOffset = int(math.log(self.config['blockSize'], 2))
        lenIndex = int(math.log(self.config['numSets'], 2))
        lenTag = lenAddr - lenOffset - lenIndex
        # exctracting tag, index & offset from address
        trace = (int(address, 16))
        maskTag = int(('1' * lenTag + '0' *
                       lenIndex + '0' * lenOffset), 2)
        tag = (trace & maskTag) >> (
            lenIndex + lenOffset)
        maskIndex = int(('0' * lenIndex + '1' *
                         lenIndex + '0' * lenOffset), 2)
        index = (trace & maskIndex) >> (lenOffset)
        # maskOffset = int(('0' * lenOffset + '0' *
        #                   lenOffset + '1' * lenOffset), 2)
        # offset = (trace & maskOffset)
        return (tag, index)

    def encodeAddress(self, tag, index):
        lenOffset = int(math.log(self.config['blockSize'], 2))
        lenIndex = int(math.log(self.config['numSets'], 2))
        address = (tag << (lenIndex + lenOffset)) + (index << lenOffset)
        return address

    def updateBlockUsed(self, index, way):
        # 0 for LRU, 1 for LFU
        if self.config['replacementPolicy'] == 0:
            self.LRU_MAT[index][way] = max(self.LRU_MAT[index]) + 1
        elif self.config['replacementPolicy'] == 1:
            self.LFU_MAT[index][way] = self.LFU_MAT[index][way] + 1
        return None

    def chooseBlockToEvict(self, index):
        # 0 for LRU, 1 for LFU
        if self.config['replacementPolicy'] == 0:
            lru = min(self.LRU_MAT[index])
            lru_way = self.LRU_MAT[index].index(lru)
            return lru_way
        elif self.config['replacementPolicy'] == 1:
            lfu = min(self.LFU_MAT[index])
            lfu_way = self.LFU_MAT[index].index(lfu)
            return lfu_way

    # read method
    def readFromAddress(self, currentAddress):
        (currentTag, currentIndex) = self.decodeAddress(currentAddress)
        self.stats['Reads'] += 1
        if (currentTag in self.TAG_MAT[currentIndex]) and self.VALID_MAT[currentIndex][self.TAG_MAT[currentIndex].index(currentTag)]:
            # Read Hit
            self.stats['ReadHits'] += 1
            foundWay = self.TAG_MAT[currentIndex].index(currentTag)
            # update matirces and counters
            self.updateBlockUsed(currentIndex, foundWay)
            return 1
        else:
            # Read Miss
            self.stats['ReadMisses'] += 1
            # if unused block, bring in block from next level, set V=1 & D=0
            if 0 in self.VALID_MAT[currentIndex]:
                foundWay = self.VALID_MAT[currentIndex].index(0)
                # bring in the block from next level
                self.issueRead(self.encodeAddress(currentTag, currentIndex))
                # update matirces and counters
                self.VALID_MAT[currentIndex][foundWay] = 1
                self.TAG_MAT[currentIndex][foundWay] = currentTag
                self.updateBlockUsed(currentIndex, foundWay)
            else:
                # if no unused block, evict LRU/LFU, allocate block, set V=1 & D=0, assign tag
                foundWay = self.chooseBlockToEvict(currentIndex)
                foundTag = self.TAG_MAT[currentIndex][foundWay]
                # Policy =0 =WBWA, V=1, D=0, issue read from  next level
                if self.DIRTY_MAT[currentIndex][foundWay] == 1:
                    # if block dirty, first writeback
                    self.issueWrite(self.encodeAddress(foundTag, currentIndex))
                    self.stats['WriteBacks'] += 1
                    self.DIRTY_MAT[currentIndex][foundWay] = 0
                # if block not dirty, no worries, just bring in the block from next level
                self.issueRead(self.encodeAddress(currentTag, currentIndex))
                # update matirces and counters
                self.VALID_MAT[currentIndex][foundWay] = 1
                self.DIRTY_MAT[currentIndex][foundWay] = 0
                self.TAG_MAT[currentIndex][foundWay] = currentTag
                self.updateBlockUsed(currentIndex, foundWay)
            return 0

    def writeToAddress(self, currentAddress):
        (currentTag, currentIndex) = self.decodeAddress(currentAddress)
        self.stats['Writes'] += 1
        if (currentTag in self.TAG_MAT[currentIndex]) and self.VALID_MAT[currentIndex][self.TAG_MAT[currentIndex].index(currentTag)]:
            self.stats['WriteHits'] += 1
            foundWay = self.TAG_MAT[currentIndex].index(currentTag)
            # Policy =0 =WBWA, D=1, write to cache, no write to next level
            self.DIRTY_MAT[currentIndex][foundWay] = 1
            # update matirces and counters
            self.updateBlockUsed(currentIndex, foundWay)
            return 1
        else:
            # Write Miss
            self.stats['WriteMisses'] += 1
            # if unused block, allocate block, set V=1 & D=0, assign tag
            if 0 in self.VALID_MAT[currentIndex]:
                foundWay = self.VALID_MAT[currentIndex].index(0)
                # Policy =0 =WBWA, bring in the block, D=1, V=1, write to cache, no write to next level
                # bring in the block from next level
                self.issueRead(self.encodeAddress(currentTag, currentIndex))
                # update matirces and counters
                self.VALID_MAT[currentIndex][foundWay] = 1
                self.DIRTY_MAT[currentIndex][foundWay] = 1
                self.TAG_MAT[currentIndex][foundWay] = currentTag
                self.updateBlockUsed(currentIndex, foundWay)
            else:
                foundWay = self.chooseBlockToEvict(currentIndex)
                foundTag = self.TAG_MAT[currentIndex][foundWay]
                # update matirces and counters
                # Policy =0 =WBWA
                if self.DIRTY_MAT[currentIndex][foundWay] == 1:
                    # if block dirty, first writeback, write to cache
                    self.stats['WriteBacks'] += 1
                    self.issueWrite(self.encodeAddress(foundTag, currentIndex))
                elif self.DIRTY_MAT[currentIndex][foundWay] == 0:
                    # if block not dirty, write to cache
                    self.DIRTY_MAT[currentIndex][foundWay] = 1
                # bring in the block from next level
                self.issueRead(self.encodeAddress(currentTag, currentIndex))
                self.TAG_MAT[currentIndex][foundWay] = currentTag
                self.updateBlockUsed(currentIndex, foundWay)
            return 0

    def printStats(self):
        print "\n" "TAG matrix is\n", self.TAG_MAT
        print "\n" "LRU matrix is\n", self.LRU_MAT
        print "\n" "LFU matrix is\n", self.LFU_MAT
        print "\n" "VALID matrix is\n", self.VALID_MAT
        print "\n" "DIRTY matrix is\n", self.DIRTY_MAT
        print "\n" "Cache Stats are\n", self.stats
        return None


##################################################################
# testing cache members & methods
##################################################################
# L1 = Cache(blockSize=4, cacheSize=32, associativity=4,
#            replacementPolicy=0, writePolicy=1)
# # L1.printStats()
# instr_list = traceParse('gcc_trace.txt')
# print "\n" "Total number of instructions is \n", len(instr_list)
# for i in instr_list:
#     if i[0] is 'r':
#         L1.readFromAddress(i[1])
#     elif i[0] is 'w':
#         L1.writeToAddress(i[1])
# L1.printStats()
# print instr_list[0][1]
# val = L1.encodeAddress(L1.decodeAddress(instr_list[0][1])[0], L1.decodeAddress(instr_list[0][1])[1])
# print hex(val)
