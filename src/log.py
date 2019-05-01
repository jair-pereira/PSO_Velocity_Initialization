import os

class Log(object):
    def __init__(self, exp_name, exp_name2, sep=",", end="\n"):
        exp_name = str(exp_name)
        exp_name2 = str(exp_name2)
    
        if not os.path.isdir("./results"):
            os.mkdir("./results")
    
        if not os.path.isdir("./results/"+exp_name):
            os.mkdir("./results/"+exp_name)
        
        self._path = "./results/"+exp_name+"/"
    
        self._file = open(self._path+exp_name2+".txt", 'w') #nfe, count_repair, best_fitness
        self._sep  = sep
        self._end  = end

    def __call__(self, information):
        self.write(information)
    
    def write(self, information):
        self._file.write(self._sep.join(map(str,information))+self._end)
        self._file.flush()
        
    def close(self):
        self._file.close()
    
    @staticmethod
    def mkdir(dir_name):
        i = 0
        while os.path.isdir(dir_name+f'_{i:03}'):
            i+=1
            
        s = dir_name+f'_{i:03}'
        os.mkdir(s)
        return s