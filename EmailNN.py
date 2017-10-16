import multiprocessing
from multiprocessing import Process
import time
import threading
import NN_Train
import EmailTool
import CmdAnalysis
import Global





if __name__ == '__main__':
    Global.running = False
    cmdana = CmdAnalysis.CmdAnaly()
    print('Start')
    a = 1
    while(True):
        time.sleep(10)
        print(a, Global.running)
        try:
            msg, sub, date = EmailTool.ReEmail()
        except TimeoutError as e:
            print('TimeoutError')

        #if sub == 'train':
        #    print('train')
        #    if running == False:
        #        t = threading.Thread(target=run, args=(msg,))
        #        t.start()
        #    else:
        #        EmailTool.SentEmail('Training is underway',
        #                            'Training is underway',
        #                            image=False)
        #if sub == 'exit':
        #    break
        cmdana.Analy(sub,msg)
        a += 1
