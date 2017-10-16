
import multiprocessing
from multiprocessing import Process
import time
import threading
import os
import NN_Train
import EmailTool
import Global


def nn(params):
    train, test = NN_Train.GetDate()
    msg = ('%s\n') % str(params)
    msg += NN_Train.NN_Train(
        NN_Train.GetNN(),
        train_data=train,
        test_data=test,
        epochs=int(params['ep']),
        batch_size=int(params['bs']),
        learning_rate=params['lr'],
        weight_decay=params['wd'])
    EmailTool.SentEmail(msg, 'TrainResult')


def run(msg):

    params = {'ep': 10, 'lr': 0.002, 'bs': 128, 'wd': 0.0}
    xx = msg.split('\r\n')
    for k in xx:
        ks = k.split(' ')
        if len(ks) > 1:
            params[ks[0]] = float(ks[1])
    print(params)

    p = Process(target=nn, args=(params,))
    print('TrainStrart')
    Global.running = True
    p.start()
    p.join()
    Global.running = False


class BaseCmd:
    def __init__(self,cmd):
        self.Next = None
        self.cmd = cmd
    def SetNext(self,n):
        self.Next = n
    def DoAnalysis(self,cmd,params):
        if cmd == self.cmd:
            self.Work(params)
        elif self.Next is not None:
            self.Next.DoAnalysis(cmd,params)
    def Work(self,params):
        pass

class TrainCmd(BaseCmd):
    def __init__(self,cmd):
        BaseCmd.__init__(self,cmd)
    def Work(self,params):
        print('train')
        if Global.running == False:
            t = threading.Thread(target=run, args=(params,))
            t.start()
        else:
            EmailTool.SentEmail('Training is underway',
            'Training is underway',
            mage=False)
class ExitCmd(BaseCmd):
    def __init__(self,cmd):
        BaseCmd.__init__(self,cmd)
    def Work(self,params):
        print('exit')
        os._exit(0)

class CmdAnaly:
    def __init__(self):
        self.exitcmd = ExitCmd('exit')
        self.traincmd = TrainCmd('train')
        self.exitcmd.SetNext(self.traincmd)
    def Analy(self,cmd,params):
        self.exitcmd.DoAnalysis(cmd,params)