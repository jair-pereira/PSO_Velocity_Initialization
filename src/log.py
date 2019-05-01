import os

class Log(object):
    if not os.path.isdir("./results"):
        os.mkdir("./results")

    def __init__(self, exp_name, sep=",", end="\n"):
        self._path = Log.mkdir("./results/"+exp_name)
    
        self._file = open(self._path+"/log.txt", 'w') #nfe, count_repair, best_fitness
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