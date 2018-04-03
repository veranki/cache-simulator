#!/bin/bash
# PartA

mkdir -p test_results
# cd test_results
# cd ../
echo running all tests..
#
echo ValidationRun1
python cache_sim.py 16 16384 1 0 0 gcc_trace.txt>test_results/out_ValidationRun1.txt
diff -iw test_results/out_ValidationRun1.txt ValidationRun1.txt>test_results/diff_ValidationRun1.txt
#
echo ValidationRun2
python cache_sim.py 128 2048 8 0 1 go_trace.txt>test_results/out_ValidationRun2.txt
diff -iw test_results/out_ValidationRun2.txt ValidationRun2.txt>test_results/diff_ValidationRun2.txt
#
echo ValidationRun3
python cache_sim.py 32 4096 4 0 1 perl_trace.txt>test_results/out_ValidationRun3.txt
diff -iw test_results/out_ValidationRun3.txt ValidationRun3.txt>test_results/diff_ValidationRun3.txt
#
echo ValidationRun4
python cache_sim.py 64 8192 2 1 0 gcc_trace.txt>test_results/out_ValidationRun4.txt
diff -iw test_results/out_ValidationRun4.txt ValidationRun4.txt>test_results/diff_ValidationRun4.txt
#
echo ValidationRun5
python cache_sim.py 32 1024 4 1 1 go_trace.txt>test_results/out_ValidationRun5.txt
diff -iw test_results/out_ValidationRun5.txt ValidationRun5.txt>test_results/diff_ValidationRun5.txt

# for file in *_trace.txt
# do
#     echo checking $file ..
#     echo writing result to "out_$file" ..
#     python cache_sim.py 16 16384 1 0 0 $file>test_results/"out_$file"
# done

echo "check results :)"
