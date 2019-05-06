from multiprocessing import Pool
import subprocess
import os
import time

def run(img_file, group_id):
    cmd = 'th test_model_on_NYU_NO_CROP.lua -num_iter 50000 -prev_model_file ../results/hourglass3_softplus_margin_log/wn1_n5000_d10000_fullNYU/model_period3_100000.t7 -test_set {} -mode test -vis'.format(img_file)
    if os.path.exists('locks/{}.lock'.format(group_id)):
        return
    if os.path.exists('locks/{}.done'.format(group_id)):
        return
    os.makedirs('locks/{}.lock'.format(group_id))
    subprocess.call(cmd, shell=True)
    os.makedirs('locks/{}.done'.format(group_id))
    os.rmdir('locks/{}.lock'.format(group_id))

pool = Pool(5)

img_lists = os.listdir('img_lists')

for img_file in img_lists:
    if '.txt' not in img_file: 
        continue
    group_id = img_file[-12:-4]
    pool.apply_async(run, (os.path.join('img_lists', img_file), group_id, ))

pool.close()
pool.join()
    
