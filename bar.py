# -*- coding: utf-8 -*-
from PowerGate import StrategyBase
from PowerGate import StrategyConfig
from PowerGate import Resolution

class BarDemo(StrategyBase):
    def __init__(self, *args, **kwargs):
        super(BarDemo, self).__init__(*args, **kwargs)

    def onBar(self, bar):
        print('Instrument:%s, DateTime:%s, Resolution:%d, Interval:%d' % \
        (bar.getInstrument(), bar.getDateTime(), bar.getResolution(), bar.getInterval()))

if __name__ == '__main__':
    config = StrategyConfig()
    config.setName('BarDemo')
    config.subscribe('rb1710', Resolution.MINUTE, 1)
    config.subscribe('ag1712', Resolution.MINUTE, 2)
    config.subscribe('IF1706', Resolution.SECOND, 5)

    strategy = BarDemo()
    strategy.run(config)

    raw_input()

    strategy.stop()