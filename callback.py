# -*- coding: utf-8 -*-
import logging
import Tkinter
from Tkinter import Frame
from Tkinter import Label
from Tkinter import Button
from Tkinter import Entry
from PowerGate import StrategyBase
from PowerGate import StrategyConfig

class Callback(StrategyBase):
    def __init__(self, logger):
        StrategyBase.__init__(self)
        self.logger = logger

    def onCreate(self):
        self.logger.info('onCreate')

    def onSetParameter(self, name, type, value, isLast):
        self.logger.info('onSetParameter: %s, %d, %s' % (name, type, value))

    def onStart(self):
        self.logger.info('onStart')

    def onPause(self):
        self.logger.info('onPause')

    def onResume(self):
        self.logger.info('onResume')

    def onTick(self, tick):
        pass
        #self.logger.info('onTick: %s @ %d %d.%d, price:%d' % (tick.instrument, tick.date, tick.time, tick.millis, tick.lastPrice))

    def onBar(self, bar):
        self.logger.info('onBar')

    def onOrderSubmitted(self, order):
        self.logger.info('onOrderSubmitted: %s', order.clOrdId)

    def onOrderRejected(self, order):
        self.logger.info('onOrderRejected: %s', order.clOrdId)

    def onOrderCancelled(self, order):
        self.logger.info('onOrderCancelled: %s', order.clOrdId)

    def onOrderFilled(self, order):
        self.logger.info('onOrderFilled: %s', order.clOrdId)

    def onCommand(self, command):
        self.logger.info('onCommand: %s' % command)
        words = command.split()
        if len(words) == 2:
            action = words[0]
            inst = words[1]

            if action == 'sub':
                self.subscribe(inst)

            return

        if len(words) == 3:
            action = words[0]
            inst = words[1]
            try:
                qty = float(words[2])
            except ValueError:
                return

            if action == 'buy':
                self.buy(inst, qty, self.getAskPrice(inst))
            elif action == 'sell':
                self.sell(inst, qty, self.getBidPrice(inst))
            elif action == 'short':
                self.sellShort(inst, qty, self.getBidPrice(inst))
            elif action == 'cover':
                self.buyToCover(inst, qty, self.getAskPrice(inst))


    def onStop(self):
        self.logger.info('onStop')

class GUI(object):
    class TextHandler(logging.Handler):
        def __init__(self, text):
            logging.Handler.__init__(self)
            self.text = text

        def emit(self, record):
            msg = self.format(record)
            def append():
                self.text.configure(state='normal')
                self.text.insert(Tkinter.END, msg + '\n')
                self.text.configure(state='disabled')
                self.text.yview(Tkinter.END)
            self.text.after(0, append)

    def __init__(self):
        root = self.root = Tkinter.Tk()
        root.title('Callback')
        root.protocol("WM_DELETE_WINDOW", self.on_closing)
        root.bind('<Return>', self.send_command)

        self.build_gui()
        self.run_strategy()

    def build_gui(self):
        import ScrolledText

        st = ScrolledText.ScrolledText(self.root, state='disabled')
        st.configure(font='TkFixedFont')
        st.grid(row=0, column=0, padx=2, pady=5)

        frame = Frame(self.root, height=20)
        frame.grid(row=1)

        Label(frame, text="Command:").grid()
        self.entry = Entry(frame, width=70)
        self.entry.grid(row=0, column=1)
        self.entry.focus_set()

        btn = Button(frame, text='Send')
        btn.grid(row=0, column=2)
        btn.bind('<Button-1>', self.send_command)

        text_handler = self.TextHandler(st)

        logger = self.logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.addHandler(text_handler)

    def send_command(self, event):
        text = self.entry.get()
        if text == 'pause':
            self.strategy.pause()
        elif text == 'resume':
            self.strategy.resume()
        else:
            self.strategy.sendCommand(text)

        self.entry.delete(0, Tkinter.END)

    def run_strategy(self):
        config = StrategyConfig()
        config.setName('Callback')
        config.setUserParameter('Bool', False);
        config.setUserParameter('Int', 10);
        config.setUserParameter('Double', 3.14);
        config.setUserParameter('String', 'param');
        config.subscribe('rb1710')

        self.strategy = Callback(self.logger)
        self.strategy.run(config)

    def on_closing(self):
        self.strategy.stop()

        self.root.destroy()

if __name__ == '__main__':
    gui = GUI()
    gui.root.mainloop()