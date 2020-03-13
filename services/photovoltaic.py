import os
import math
import json
import pika
import threading
import numpy as np

from services.models import READINGS, TIMES


class PVSimulator(object):

    def __init__(self, port_numer):
        self._fit_curve()
        self._output_path = os.path.join(os.getcwd(), 'output.csv')
        print('Output path:')
        print(self._output_path)
        self._initialize_output()
        self._initialie_connection(port_numer)

    def __repr__(self):
        return '<PVSimulator: 3.25kW>'

    def _initialie_connection(self, port_numer):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=port_numer))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue='pv_simulation', durable=True)
        self._channel.basic_qos(prefetch_count=1)
        self._channel.basic_consume(on_message_callback=self._callback, queue='pv_simulation', auto_ack=True) 
        return

    def start_consuming(self):
        self._channel.start_consuming()
        return

    def _callback(self, ch, method, properties, body):
        data = json.loads(body)
        # get the time of the day in seconds
        time_in_seconds = data['time']['hour']*3600 + data['time']['minute']*60 + data['time']['second']
        ph_power = self.get_power(time_in_seconds)
        power_sum = ph_power + data['meter_reading']
        net_value = ph_power - data['meter_reading']
        self._append_output(data['time'], data['meter_reading'], ph_power, power_sum, net_value)

    def get_power(self, x):
        # gets the cell power
        # This is separated from the model, in case noise is added
        return 1000*self.calculate_power(x)

    def _fit_curve(self):
        # Calculates the polynomial parameters for the fitted curve
        reduction_factor = max(READINGS)/3.25   
        x_values = [x/reduction_factor for x in READINGS]
        const = np.polyfit(TIMES, x_values, 3)
        self._const = const[::-1]
        return

    def calculate_power(self, x):
        # Calculates the cell power for a time x of the day based on the fitted polynomial
        if x < 5.5*3600:
            return 0
        elif 5.5*3600 < x < 7*3600+15*60:
            return (x-5.5*3600) * (0.245846065896488)/(105*60)
        elif 17*3600 > x > 15*3600+40*60:
            return (17*3600-x) * 0.09924047440601624/(80*60)
        elif x > 17*3600:
            return 0
        value = 0
        for index, c in enumerate(self._const):
            value += c * (x ** index)
        return value

    def _initialize_output(self):
        with open(self._output_path, 'w') as f:
            f.write('"Time Stamp","Meter (W)", "PV (W)", "Meter + PV (W)", "PV - Meter (W)"\n')
        return

    def _append_output(self, time_dict, meter, pv, power_sum, net_value):
        timestmp = '{}-{}-{} {}:{}:{}'.format(time_dict['year'], time_dict['month'], time_dict['day'], time_dict['hour'], time_dict['minute'], time_dict['second'])
        with open(self._output_path, 'a') as f:
            f.write('"{}","{}", "{}", "{}", "{}"\n'.format(timestmp, meter, pv, power_sum, net_value))
        return
    
    def close_connection(self):
        self._connection.close()
        return