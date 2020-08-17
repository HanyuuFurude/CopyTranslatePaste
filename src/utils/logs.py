import logging
# debug() 调试级别，一般用于记录程序运行的详细信息
# info() 事件级别，一般用于记录程序的运行过程
# warnning() 警告级别，，一般用于记录程序出现潜在错误的情形
# error() 错误级别，一般用于记录程序出现错误，但不影响整体运行
# critical 严重错误级别 ， 出现该错误已经影响到整体运行

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(filename)s \n [line:%(lineno)d] %(levelname)s %(funcName)s %(message)s',
    datefmt='%Y/%b/%d %H:%M:%S',
    filename='log.log',
    filemode='a'
)

log = logging.getLogger()
