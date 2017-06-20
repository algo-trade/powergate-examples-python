# -*- coding: utf-8 -*-
from PowerGate import StrategyBase
from PowerGate import StrategyConfig

class TimerDemo(StrategyBase):
    def __init__(self, *args, **kwargs):
        super(TimerDemo, self).__init__(*args, **kwargs)

    def onStart(self):
        self.registerTimer(1000)

    def onTimer(self, timerId):
        print(timerId)
        self.registerTimer(1000)

if __name__ == '__main__':
    config = StrategyConfig()
    config.setName('TimerDemo')

    strategy = TimerDemo()
    strategy.run(config)

    raw_input()

    strategy.stop()
