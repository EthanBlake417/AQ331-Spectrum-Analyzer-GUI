from types import SimpleNamespace
import multiprocessing
from multiprocessing import Process, Event, Value
from Oven.oven import EzZone
from GraphingTool.slider_graphing_tool import slider_graphing_tool
from AQ6331SpectrumAnalyzer.spectrum_analyzer import spectrum_analyser
from NewportOpticalPowerMeter1830C.OPM import optical_power_meter
import time


def main(**kwargs):
    print(kwargs['hi'])
    kwargs['another'] = 4
    start_processes(**kwargs)


# def other(**kwargs):
#     print(kwargs)
#     n = SimpleNamespace(**kwargs)
#     print(n.another)


def start_processes(**kwargs):
    """ Starts all the processes at the same time """
    # start EZ Zone
    ez = EzZone()
    original_time = time.time()
    print("Beginning Test!")
    # creating processes
    e = Event()
    flag = Value('i', 1)
    ready_to_graph_flag = Value('i', 0)
    # add to kwargs
    kwargs['original_time'] = original_time
    kwargs['e'] = e
    kwargs['flag'] = flag
    kwargs['ready_to_graph_flag'] = ready_to_graph_flag

    p1 = Process(target=other2, kwargs=kwargs)
    p2 = Process(target=other3, kwargs=kwargs)

    # starting processes
    p1.start()
    p2.start()

    p1.join()
    e.set()
    p2.join()

    # all processes finished
    print("Done!")


def other2(**kwargs):
    print(kwargs)


def other3(**kwargs):
    n = SimpleNamespace(**kwargs)
    print(n.another, n.num*n.num2)



if __name__ == '__main__':
    main(hi="hello", num=5, num2=10)