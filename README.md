# Email_Monitor_MxnetTrain
## 使用Email监控Mxnet训练
受到小伙伴们的使用微信监控训练的启发，就动手做了个使用邮件监控Mxnet训练的例子  
刚开始使用Pyhton，有些地方可能写的不太好。轻喷  
由于在查多线程的时候，发现Python的多线程受到GIL的影响，多线程会有一些性能局限。所以在这里我另开了一个进程来训练，为了保证训练性能不受影响。  
- EmailNN  
  主要启动代码,包含循环监控邮箱,启动训练进程等
- EmailTool  
  自己封装的一些处理邮件的函数
- NN_Train  
  深度学习训练主要代码

## 使用
在EmailTool里配置好自己的邮箱地址,密码和pop,smtp地址  
在NN_Train配置好需要训练的网络和数据等
在EmailNN里可以修改命令接受和解析  
最后启动EmailNN即可 
 
邮件发送:  
- 训练  
    - 主题为: train  
    - 参数设置  
    各个训练参数和参数值中间空一空格,每个参数和参数值一行
        - ep:  
        epoch
        - lr:  
        learning_rate
        - bs:  
        batch_size
        - wd:  
        weight_decay  
- 终止监控:
    - 主题为: exit

## 效果

发送的命令

![1](./1.PNG)

正在训练的时候在发送会提示训练正在进行中

![2](./2.PNG)

训练结束会发送训练日志和曲线图以及使用的参数

![3](./3.PNG)

训练曲线图

![4](./4.PNG)