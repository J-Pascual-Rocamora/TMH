import json
import pika
import time
import random

class Meter(object):

    def __init__(self, port_numer, real_time_flag, conneection_interval=1800):
        self._current_value = random.uniform(0, 9000)
        self._connection_interval = 1800
        self._initialize_connection(port_numer)
        self._real_time_flag = real_time_flag

    def __repr__(self):
        return '<Meter>'

    def _initialize_connection(self, port_numer):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=port_numer))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue='pv_simulation', durable=True)
        return

    def start_casting(self):
        if self._real_time_flag is False:
            current_time = 0
            time_str = time.localtime()
            current_hour = 0
            current_minute = 0
            current_second = 0
            while current_time < 86400:
                time_dict = {
                    'year':int(time.strftime('%Y', time_str)),
                    'month':int(time.strftime('%m', time_str)),
                    'day':int(time.strftime('%d', time_str)),
                    'hour':current_hour,
                    'minute':current_minute,
                    'second':current_second
                }
                self.measure(current_time)
                self._send_measurement(time_dict, self._current_value)
                # Update counters
                current_time += 2
                current_second += 2
                if current_second == 60:
                    current_second = 0
                    current_minute += 1
                if current_minute == 60:
                    current_minute = 0
                    current_hour += 1
        else:
            while True:
                time_str = time.localtime()
                time_dict = {
                    'year':int(time.strftime('%Y', time_str)),
                    'month':int(time.strftime('%m', time_str)),
                    'day':int(time.strftime('%d', time_str)),
                    'hour':int(time.strftime('%H', time_str)),
                    'minute':int(time.strftime('%M', time_str)),
                    'second':int(time.strftime('%S', time_str))
                }
                time_in_seconds = time_dict['hour'] * 3600 + time_dict['minute']*60 + time_dict['second']
                self.measure(time_in_seconds)
                self._send_measurement(time_dict, self._current_value)
                time.sleep(2)
        return

    def measure(self, time):
        if time % self._connection_interval == 0:
            self._current_value = random.uniform(0, 9000)
        return self._current_value

    def _send_measurement(self, time, measurement):
        message = {
            'meter_reading': measurement,
            'time': time
            }
        self._channel.basic_publish(exchange='',
              routing_key='pv_simulation',
              body=json.dumps(message),
              properties=pika.BasicProperties(
                 delivery_mode = 2,
              ))
        return

    def close_connection(self):
        self._connection.close()
        return

    def get_current_value(self):
        return self._current_value