import sched, time
from threading import Timer, Thread, Event

tick_interval = 0.1 # seconds

def tick():
  print('tick')
  s.enter(tick_interval, 1, tick)

class Tick:
  def monitor(self):
    # Run every tick_interval
    print('tick')
    #Timer(tick_interval, self.monitor, ()).start()
    self.t.start()

  def run(self):
    """ Event loop """
    #self.callback = callback
    #Timer(tick_interval, self.monitor, ()).start()
    self.t = Timer(tick_interval, self.monitor)
    self.t.start()

def printTick():
  print("tick")

class MyThread(Thread):
    def __init__(self, callback, tick_interval):
        Thread.__init__(self)
        self.stopped = Event()
        self.callback = callback
        self.tick_interval = tick_interval

    def run(self):
        while not self.stopped.wait(self.tick_interval):
            self.callback()

if __name__ == '__main__':
  if 0: 
    #using sched
    s = sched.scheduler(time.time, time.sleep)

    s.enter(tick_interval, 1, tick)
    s.run()
  else:
    # using threading
    #T = Tick()
    #T.run()
    #stopFlag = Event()
    thread = MyThread(printTick, tick_interval)
    thread.start()
    # this will stop the timer
    #stopFlag.set()