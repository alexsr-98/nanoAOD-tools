while [ true ]; do
    for i in MC2018; do
        python checkcrab.py temp_postproc_2022_05_03_tercerpostproc$i -j 12 -v -nl -ar;
    done;
    sleep 45m;
done
