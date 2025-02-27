from testing.mock_xela_client import MockXelaClient
import time
import t_utils


def test_xela_driver():
    t_utils.start_websocket_server()

    time.sleep(3)  # wait for the server to start properly

    mock_xela = MockXelaClient()
    mock_xela.start()

    while not mock_xela.is_ready():
        time.sleep(0.01)

    mock_xela.start_data_collection()

    time.sleep(1)

    mock_xela.stop_data_collection()

    data = mock_xela.get_data()
    assert len(data) != 0

    mock_xela.stop_and_clean_up()

    while not mock_xela.is_stopped():
        time.sleep(0.01)
