import unittest


class TestSimulator(unittest.TestCase):

    def test_pv_value_one(self):
        from services.photovoltaic import PVSimulator
        p = PVSimulator(port_numer=5672)
        power = p.get_power(7*3600+15*60)
        msg = 'Unexpected value for PV power generated at 7:15'
        self.assertEqual(power, 257.49146432340723, msg=msg)

    def test_pv_value_two(self):
        from services.photovoltaic import PVSimulator
        p = PVSimulator(port_numer=5672)
        power = p.get_power(11*3600+55*60)
        msg = 'Unexpected value for PV power generated at 11:55'
        self.assertEqual(power, 3403.947108289752, msg=msg)

    def test_pv_value_three(self):
        from services.photovoltaic import PVSimulator
        p = PVSimulator(port_numer=5672)
        power = p.get_power(15*3600+40*60)
        msg = 'Unexpected value for PV power generated at 15:40'
        self.assertEqual(power, 103.94136258302278, msg=msg)


if __name__ == "__main__":
    unittest.main()