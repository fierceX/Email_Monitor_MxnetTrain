from mxnet import gluon
from mxnet.gluon import nn
import matplotlib.pyplot as plt
from mxnet import autograd as autograd
from mxnet import nd
import mxnet as mx
import os


def try_gpu():
    """If GPU is available, return mx.gpu(0); else return mx.cpu()"""
    try:
        ctx = mx.gpu()
        _ = nd.zeros((1,), ctx=ctx)
    except:
        ctx = mx.cpu()
    return ctx


ctx = try_gpu()


def transform(data, label):
    return data.astype('float32') / 255, label.astype('float32')


def GetDate():
    fashion_train = gluon.data.vision.FashionMNIST(
        root='./', train=True, transform=transform)
    fashion_test = gluon.data.vision.FashionMNIST(
        root='./', train=True, transform=transform)
    return fashion_train, fashion_test


def accuracy(output, label):
    return nd.mean(output.argmax(axis=1) == label).asscalar()


def evaluate_accuracy(data_iterator, net):
    acc = 0.
    test_loss = 0.
    softmax_cross_entropy = gluon.loss.SoftmaxCrossEntropyLoss()
    for data, label in data_iterator:
        data = data.as_in_context(ctx)
        label = label.as_in_context(ctx)
        output = net(nd.transpose(data, (0, 3, 1, 2)))
        loss = softmax_cross_entropy(output, label)
        acc += accuracy(output, label)
        test_loss += nd.mean(loss).asscalar()
    return acc / len(data_iterator), test_loss / len(data_iterator)


def GetNN():
    net = nn.HybridSequential()
    with net.name_scope():
        net.add(gluon.nn.Conv2D(channels=20, kernel_size=5, activation='relu'))
        net.add(gluon.nn.MaxPool2D(pool_size=2, strides=2))
        net.add(gluon.nn.Conv2D(channels=50, kernel_size=3, activation='relu'))
        net.add(gluon.nn.MaxPool2D(pool_size=2, strides=2))
        net.add(gluon.nn.Flatten())
        net.add(gluon.nn.Dense(10))
    net.initialize(init=mx.init.Xavier(), ctx=ctx)
    net.hybridize()
    return net


def NN_Train(net, train_data, test_data,params,nameparams):
    msg = ''

    epochs = int(params['ep'])
    batch_size = int(params['bs'])
    learning_rate = params['lr']
    weight_decay = params['wd']

    train_loss = []
    train_acc = []
    dataset_train = gluon.data.DataLoader(train_data, batch_size, shuffle=True)
    test_loss = []
    test_acc = []
    dataset_test = gluon.data.DataLoader(test_data, batch_size, shuffle=True)

    trainer = gluon.Trainer(net.collect_params(), 'adam',
                            {'learning_rate': learning_rate,
                             'wd': weight_decay})
    softmax_cross_entropy = gluon.loss.SoftmaxCrossEntropyLoss()

    for epoch in range(epochs):
        _loss = 0.
        _acc = 0.
        t_acc = 0.
        for data, label in dataset_train:
            data = nd.transpose(data, (0, 3, 1, 2))
            data = data.as_in_context(ctx)
            label = label.as_in_context(ctx)
            with autograd.record():
                output = net(data)
                loss = softmax_cross_entropy(output, label)
            loss.backward()
            trainer.step(batch_size)

            _loss += nd.mean(loss).asscalar()
            _acc += accuracy(output, label)
        __acc = _acc / len(dataset_train)
        __loss = _loss / len(dataset_train)
        train_loss.append(__loss)
        train_acc.append(__acc)

        t_acc, t_loss = evaluate_accuracy(dataset_test, net)
        test_loss.append(t_loss)
        test_acc.append(t_acc)

        msg += ("Epoch %d. Train Loss: %f, Test Loss: %f, Train Acc %f, Test Acc %f\n" % (
            epoch, __loss, t_loss, __acc, t_acc))

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(train_loss, 'r')
    ax1.plot(test_loss, 'g')
    ax1.legend(['Train_Loss', 'Test_Loss'], loc=2)
    ax1.set_ylabel('Loss')

    ax2 = ax1.twinx()
    ax2.plot(train_acc, 'b')
    ax2.plot(test_acc, 'y')
    ax2.legend(['Train_Acc', 'Test_Acc'], loc=1)
    ax2.set_ylabel('Acc')

    plt.savefig(os.path.join(nameparams['dir'],nameparams['png']), dpi=600)
    net.save_params(os.path.join(nameparams['dir'],nameparams['params']))
    return msg
