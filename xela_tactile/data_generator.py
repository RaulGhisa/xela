import random
import time


MOCK_DATA_FROM_MANUAL = {
    "message": 49090,
    "time": 1708406349.5611684,
    "sendtime": 1708406349.5616164,
    "sensors": 3,
    "type": "routine",
    "1": {
        "time": 1708406349.5593173,
        "sensor": "1",
        "data": "8246,81A8,8A58,...",
        "model": "XR1944",
        "taxels": 16,
        "tempraw": [33337, 33205, 35607],
        "temp": [307.53],
        "ups": [105.17100960863372],
        "calibrated": [0.059, 0.021, 0.15],
    }
}


def get_mock_data(n=100, freq=133):
    msg_counter = random.randint(0, int(1e6))

    # convert from frequency to period
    time_increment = 1 / freq
    time_counter = 0
    time_start = time.time()

    data = []
    for _ in range(n):
        mock = {
            "message": msg_counter,
            "time": time.time(),
            "sendtime": time_start + time_counter,
            "sensors": 1,
            "type": "routine",
            "1": {
                "time": time.time(),
                "sensor": "1",
                "data": get_mock_readings(),
                "model": "uSPa44",
                "taxels": 16,
                "tempraw": [33337, 33205, 35607],
                "temp": [307.53],
                "ups": [105.17100960863372],
                "calibrated": [0.059, 0.021, 0.15],
            }
        }
        data.append(mock)
        msg_counter += 1
        time_counter += time_increment

    return data


def get_mock_readings(n=3*4*4):
    """
        n: (X, Y, Z) readings for a 4 x 4 grid of tactile sensors
    """
    data = ""
    for _ in range(n):
        # 2 bytes are received on the CAN
        value = random.randint(0, 2**16)
        # fill with zeroes if the representation is smaller than 4 bytes
        data += f'{value:X}'.zfill(4) + ','

    return data[:-1]


if __name__ == '__main__':
    mock_data = get_mock_data()

    for x in mock_data:
        print(x)

    print(mock_data[11]["sendtime"] - mock_data[10]["sendtime"])
