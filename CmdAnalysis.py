import multiprocessing
from multiprocessing import Process
import time
import threading
import os
import NN_Train
import EmailTool
import Global


def nn(params,nameparams):
    train, test = NN_Train.GetDate()
    print(params)
    print(nameparams)
    msg = ('%s\n') % str(params)
    msg += ('%s\n') % str(nameparams)
    msg += NN_Train.NN_Train(
        NN_Train.GetNN(),
        train_data=train,
        test_data=test,
        params = params,
        nameparams = nameparams)
    EmailTool.SentEmail(msg, 'TrainResult',os.path.join(nameparams['dir'],nameparams['png']))


def run():
    p = Process(target=nn,args=(Global.params,Global.nameparams,))
    print('TrainStrart')
    Global.running = True
    p.start()
    p.join()
    Global.running = False


class BaseCmd:
    def __init__(self, cmd):
        self.Next = None
        self.cmd = cmd

    def SetNext(self, n):
        self.Next = n

    def DoAnalysis(self, cmd, params):
        if cmd == self.cmd:
            self.Work(params)
        elif self.Next is not None:
            self.Next.DoAnalysis(cmd, params)

    def Work(self, params):
        pass


class TrainCmd(BaseCmd):
    def __init__(self, cmd):
        BaseCmd.__init__(self, cmd)

    def Work(self, msg):
        print('train')
        if Global.running == False:
            xx = msg.split('\r\n')
            for k in xx:
                ks = k.split(' ')
                if len(ks) > 1:
                    Global.params[ks[0]] = float(ks[1])
            t = threading.Thread(target=run)
            t.start()
        else:
            message = ('Training is underway\n%s\n%s') % (str(Global.params),str(Global.nameparams))
            EmailTool.SentEmail(message,
                                'Training is underway',
                                None)


class ExitCmd(BaseCmd):
    def __init__(self, cmd):
        BaseCmd.__init__(self, cmd)

    def Work(self, params):
        print('exit')
        os._exit(0)

class SetNameParamsCmd(BaseCmd):
    def __init__(self,cmd):
        BaseCmd.__init__(self,cmd)
    
    def Work(self,msg):
        xx = msg.split('\r\n')
        for k in xx:
             ks = k.split(' ')
             if len(ks) > 1:
                 Global.nameparams[ks[0]] = ks[1]
        print(Global.nameparams)
        EmailTool.SentEmail(str(Global.nameparams),'NameParams',None)


class CmdAnaly:
    def __init__(self):
        self.CmdList = []
        self.Add(ExitCmd('exit'))
        self.Add(TrainCmd('train'))
        self.Add(SetNameParamsCmd('setname'))

    def Add(self, cmd):
        self.CmdList.append(cmd)
        if len(self.CmdList) > 1:
            self.CmdList[len(self.CmdList) - 2].SetNext(self.CmdList[len(self.CmdList) - 1])

    def Analy(self, cmd, params):
        self.CmdList[0].DoAnalysis(cmd, params)
