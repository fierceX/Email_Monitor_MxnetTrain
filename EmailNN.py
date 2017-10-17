import time
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
        cmdana.Analy(sub, msg)
        a += 1
