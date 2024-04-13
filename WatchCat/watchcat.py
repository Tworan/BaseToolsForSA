import os
import json
import time
import requests
import subprocess
import threading

class storage_limited_stack:
    def __init__(self, max_number=100):
        self.stack = []
        self.numbers = max_number

    def pop(self):
        if len(self.stack) > 0:
            self.stack.pop()
            self.numbers -= 1
            return True
        
        else:
            return False 
    
    def append(self, elem):
        if len(self.stack) < self.numbers:
            self.stack.append(elem)
            self.numbers += 1
        
        else:
            self.stack.pop(0)
            self.stack.append(elem)
    
    def mean(self, start=0, end=-1):
        sums = 0
        for elem in self.stack[start:end]:
            sums += elem 
        
        mean = sums / (max(1, self.numbers))
        return mean 
    


class WatchCat:
    """
    æç»ï¼ watchcatç¨äºå®¢æ·ç«¯çæ§GPUä½¿ç¨æåµï¼GPUæ¾å­å©ç¨æåµãGPUä¸æ´»è·çç¨åºãGPUä½¿ç¨çç¨æ·ãæä½¿ç¨çGPUå¡å·ç­ãéè¿åç»åçæå¡å¨éä¿¡ï¼åæ¶ç»è®°æå¡å¨GPUä½¿ç¨çæåµï¼æ¹ä¾¿åç»§å»ºè®¾ã
    æµç¨:   
            1. åå§åï¼è·åå½åæå¡å¨ææçGPUï¼                cmd: nvidia-smi --query-gpu=count --format=csv,noheader -f gpu_counts.rec
            2. éè¿ç³»ç»è°ç¨è·åå½åæå¡å¨GPUä½¿ç¨æåµï¼          cmd: nvidia-smi -i gpu_idx --query-compute-apps=pid,process_name,used_memory --format=csv,noheader -f gpu_status.rec
            3. éè¿ç½ç»éä¿¡ï¼å°ä½¿ç¨æåµä¸ä¼ è³æå¡å¨ï¼           tcpéä¿¡ï¼æå¡å¨flaskæ¥å
            4. æå¡å¨ç­å¤ï¼
            5. éå¤2ã3ã4ï¼
    """
    def __init__(self, home_addr, home_port, cat_name, gpu_count_path="gpu_counts.rec", gpu_status_path="gpu_status.rec"):
        
        self.home_addr = home_addr
        self.home_port = home_port
        self.cat_name = cat_name

        self.gpu_count_path = gpu_count_path
        self.gpu_status_path = gpu_status_path

        self.gpu_counts = None

        self.gpu_utils = []
        

    def initial(self):
        
        init_cmds = "nvidia-smi --query-gpu=count --format=csv,noheader -f {}".format(self.gpu_count_path)
        
        os.system(init_cmds)

        f = open(self.gpu_count_path, 'r')
        self.gpu_counts = int(f.readline())
        self.gpu_utils = [storage_limited_stack(120) for _ in range(self.gpu_counts)]

    def get_user(self, pid):
        
        output = os.popen("ps -p {} -o user".format(pid)).read().split('\n')[1]

        return output

    def get_gpu_status(self):
        # éåææGPUæ¥çæåµå¹¶ä¸æ¨éè³æå¡å¨
        gpu_status = {}
        for gpu_idx in range(self.gpu_counts):
            idx_gpu_status = []
            get_stauts_cmd = "nvidia-smi -i {} --query-compute-apps=pid,process_name,used_memory --format=csv,noheader -f {}".format(gpu_idx, self.gpu_status_path)
            
            os.system(get_stauts_cmd)

            f = open(self.gpu_status_path)

            for line in f.readlines():
                # unpack info
                idx_gpu_status.append(line.replace('\n', '').split(',')) # pid, preocess_name, memoery, user, gpu_utils
                idx_gpu_status[-1].append(self.get_user(idx_gpu_status[-1][0]))
                idx_gpu_status[-1].append(int(self.gpu_utils[gpu_idx].mean()))

            # å®æå½åGPUä¿¡æ¯è·å, å°å¶ä¿å­
            gpu_status[gpu_idx] = idx_gpu_status
        
        return gpu_status
     
    def take_status_home(self, status):

        info = {
            'cat_name': self.cat_name,
            'counts': self.gpu_counts,
            'cat_info': status,
            'persistence': '0',
        }

        # åéè¯·æ± todo
        ret = requests.post(self.home_addr+':'+str(self.home_port)+'/cathome', json=json.dumps(info))

    def rec_gpu_utils(self, time_step=1):
        while(True):
            time.sleep(time_step)
            for i in range(self.gpu_counts):
                command = "nvidia-smi -i {} --query-gpu=utilization.gpu  --format=csv,noheader".format(i)
                gpu_utils = subprocess.check_output(command, shell=True).decode().split(" ")[0]
                self.gpu_utils[i].append(int(gpu_utils))

    def main_loop(self, sleep_time=60):
        
        self.initial()
        
        gpu_utils_thread = threading.Thread(target=self.rec_gpu_utils, kwargs={"time_step": 1})
        gpu_utils_thread.start()

        while(True):
            gpu_status = self.get_gpu_status()
            try:
                self.take_status_home(gpu_status)
            except:
                print("[error]: failed to fetch {}\n".format(self.home_addr))

            time.sleep(sleep_time)

        gpu_utils_thread.join(1)

if __name__ == '__main__':
    MyCat = WatchCat('http://120.55.64.125', 5701, '1080ti')
    MyCat.main_loop(90)



