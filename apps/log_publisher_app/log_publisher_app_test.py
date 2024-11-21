import pytest
from log_publisher_app import LogPublisherApp
from signals import Signals

def test_app():
    # Test case for add_numbers
    signal1 = Signals(
        vehicle_id=1,
        timestamp=1633072800,
        speed=60.0,
        speedDisplayed=60.0,
        speedPerWheel=[60.0, 60.0, 60.0, 60.0],
        longAcc=0.0,
        latAcc=0.0,
        yawrate=0.0,
        steeringWheelAngle=0.0,
        steeringWheelAngleSpeed=0.0,
        drvSteerTorque=0.0,
        timeSinceLastClick=0.0,
        wheelSteeringAngleFront=0.0,
        wheelSteeringAngleRear=0.0
    )
    signal2 = Signals(
        vehicle_id=2,
        timestamp=1633072900,
        speed=70.0,
        speedDisplayed=70.0,
        speedPerWheel=[70.0, 70.0, 70.0, 70.0],
        longAcc=0.1,
        latAcc=0.1,
        yawrate=0.1,
        steeringWheelAngle=0.1,
        steeringWheelAngleSpeed=0.1,
        drvSteerTorque=0.1,
        timeSinceLastClick=0.1,
        wheelSteeringAngleFront=0.1,
        wheelSteeringAngleRear=0.1
    )

    assert isinstance(signal1.to_dict(), dict)
    assert isinstance(signal2.to_dict(), dict)


def test_signals():
    # Test case for add_numbers
    signal1 = Signals(
        vehicle_id=1,
        timestamp=1633072800,
        speed=60.0,
        speedDisplayed=60.0,
        speedPerWheel=[60.0, 60.0, 60.0, 60.0],
        longAcc=0.0,
        latAcc=0.0,
        yawrate=0.0,
        steeringWheelAngle=0.0,
        steeringWheelAngleSpeed=0.0,
        drvSteerTorque=0.0,
        timeSinceLastClick=0.0,
        wheelSteeringAngleFront=0.0,
        wheelSteeringAngleRear=0.0
    )
    signal2 = Signals(
        vehicle_id=2,
        timestamp=1633072900,
        speed=70.0,
        speedDisplayed=70.0,
        speedPerWheel=[70.0, 70.0, 70.0, 70.0],
        longAcc=0.1,
        latAcc=0.1,
        yawrate=0.1,
        steeringWheelAngle=0.1,
        steeringWheelAngleSpeed=0.1,
        drvSteerTorque=0.1,
        timeSinceLastClick=0.1,
        wheelSteeringAngleFront=0.1,
        wheelSteeringAngleRear=0.1
    )

    assert isinstance(signal1.to_dict(), dict)
    assert isinstance(signal2.to_dict(), dict)


