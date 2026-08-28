def test_ev_fleet_iq_smoke():
    vehicle_id = "EV001"
    battery_soc = 85.5

    assert vehicle_id.startswith("EV")
    assert 0 <= battery_soc <= 100
