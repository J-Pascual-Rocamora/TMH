import argparse
import threading

from services.meter import Meter
from services.photovoltaic import PVSimulator


def commandLineArgs():
    '''
    Handles the arguments
    '''
    
    parser = argparse.ArgumentParser(
									formatter_class=argparse.RawTextHelpFormatter,
									prog = "Photovoltaic system simulator",    
									description="""Simulates a home power comsuption and a photovoltaic system power generation""",
									)
    
    parser.add_argument('--version', action = 'version', version = 'PV Simulator 0.0.1')
    parser.add_argument('-v',        action = 'version', version = 'PV Simulator 0.0.1')
    
    parser.add_argument("-p", action='store', type=int,
						dest='port_number', default=5672,
						help='''rabbitmq port number. Default=5672''')

    parser.add_argument("-R", action='store_true', dest='real_time', default=False,
						help='''Simulation in real time. Default=False''')
    return parser.parse_args()
    
def start_pv(port_number):
    try:
        p = PVSimulator(port_number)
        p.start_consuming()
    except KeyboardInterrupt:
        p.close_connection()
    return

def start_meter(port_number, real_time_flag):
    try:
        m = Meter(port_number, real_time_flag)
        m.start_casting()
    except KeyboardInterrupt:
        m.close_connection()
    return

def main():
    args = commandLineArgs()
    port_number = args.port_number
    real_time = args.real_time
    try:
        meter_thread = threading.Thread(target=start_meter, args=(port_number, real_time,))
        pv_thread = threading.Thread(target=start_pv, args=(port_number, ))
        meter_thread.start()
        pv_thread.start()
    except KeyboardInterrupt:
        meter_thread.join()
        pv_thread.join()

    return


if __name__ == "__main__":
    main()