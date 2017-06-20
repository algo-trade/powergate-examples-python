# -*- coding: utf-8 -*-
import math
from PowerGate import StrategyBase     #策略基类
from PowerGate import StrategyConfig   #策略配置
from PowerGate import MA               #均线
from PowerGate import Cross            #均线穿越验证

class MACross(StrategyBase):
    def __init__(self, *args, **kwargs):
        super(MACross, self).__init__(*args, **kwargs)
        self.ma_short = MA()
        self.ma_long = MA()

    def onStart(self):
        #获取Tick最新价数据序列,Tick数据序列会被系统自动填充
        self.series = self.getTickSeries().getLastPriceDataSeries()

        #以Tick最新价数据序列和相应周期初始化两根均线
        self.ma_short.init(self.series, 10)
        self.ma_long.init(self.series, 40)

    def onTick(self, tick):
        #如果均线还没有可用的计算值，直接返回
        #ma_short的周期参数为10，当Tick最新价数据序列被10个Tick填充时，ma_short获得第一个MA值
        if math.isnan(self.ma_short[0]):
            return

        #ma_long的周期参数为40，当Tick最新价数据序列被40个Tick填充时，ma_short获得第一个MA值
        if math.isnan(self.ma_long[0]):
            return

        #打印Tick及两条均线的最新值
        print ('CLOSE=%f  MA[10]=%f  MA[40]=%f' % (tick.lastPrice,
                                                  self.ma_short[0],
                                                  self.ma_long[0]))
        #短均线上穿长均线
        if Cross.crossAbove(self.ma_short, self.ma_long):
            print('Cross Above')
            #以策略订阅的主合约为标的，做多1手
            self.openLong(self.getMainInstrument(), 1)
        #短均线下穿长均线
        elif Cross.crossBelow(self.ma_short, self.ma_long):
            print('Cross Below')
            #以策略订阅的主合约为标的，做空1手
            self.openShort(self.getMainInstrument(), 1)

if __name__ == '__main__':
    config = StrategyConfig()
    #设置策略名称，每个策略必须有一个名称
    config.setName('MACross')
    #如果只订阅一个合约，那么该合约就是策略主合约，否则第一个订阅的合约为策略主合约
    config.subscribe("rb1710")

    #策略实例
    strategy = MACross()
    #运行策略
    strategy.run(config)
    #等待用户输入
    raw_input()
    #停止策略
    strategy.stop()