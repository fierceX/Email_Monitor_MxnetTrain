import multiprocessing
from multiprocessing import Process
import time
import threading
import NN_Train
import EmailTool


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
    global running
    running = True
    p.start()
    p.join()
    running = False


if __name__ == '__main__':
    global running
    running = False
    print('Start')
    a = 1
    while(True):
        time.sleep(10)
        print(a, running)
        try:
            msg, sub, date = EmailTool.ReEmail()
        except TimeoutError as e:
            print('TimeoutError')

        if sub == 'train':
            print('train')
            if running == False:
                t = threading.Thread(target=run, args=(msg,))
                t.start()
            else:
                EmailTool.SentEmail('Training is underway',
                                    'Training is underway',
                                    image=False)
        if sub == 'exit':
            break
        a += 1
