import sys, time, json, logging, os

import ecal.core.core as ecal_core
import requests
from ecal.core.subscriber import StringSubscriber
from enum import Enum
from signals import Signals, parse_signals
from report_dto import ReportDTO
from collections import deque
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger("Log Publisher App")
stdout = logging.StreamHandler(stream=sys.stdout)
stdout.setLevel(logging.INFO)
logger.addHandler(stdout)
logger.setLevel(logging.INFO)


'''
negative acc for brake
we have timestamp
if the speed change from 50 to 10 in small amount of time.

collection of records
'''

class LogPublisherApp(object):
    executor = ThreadPoolExecutor(max_workers=5)
    test_val = float(os.getenv("THRESHOLD_VALUE", 40))
    criticial_speed_thresholds = {20: 1, 30: 2, test_val: 3}
    vehicle_dynamics_samples = deque(maxlen=50)

    reports = deque()

    def __init__(self):
        self.executor.submit(self.publish_reports)

        
    def run(self):
        vehicle_dynamics_sub = StringSubscriber("vehicle_dynamics")
        vehicle_dynamics_sub.set_callback(self.vehicle_dynamics_callback)

        # object_detection_sub = StringSubscriber("object_detection") # to detect the construction site sign
        # object_detection_sub.set_callback(object_detection_callback)
        
        while ecal_core.ok():
            time.sleep(0.5)

    def publish_reports(self):
        print("Started side service")
        while True:
            while len(self.reports) > 0:
                report = self.reports.pop()
                try:
                    self.publish_report(report)
                except Exception as e:
                    print(f"Exception: {e}")

            time.sleep(1)

    def publish_report(self, report):
        report_json = json.dumps(report.to_dict())
        url = "http://172.16.1.41:5010/api/reports"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers, data=report_json)
        print("sent")
        
    
    # Callback for receiving vehicle_dynamics messages
    def vehicle_dynamics_callback(self, topic_name, msg, time):
        def add_signal():
            signal_schema: Signals = parse_signals(msg)
            self.vehicle_dynamics_samples.append(signal_schema)
            # print([sample.speed for sample in self.vehicle_dynamics_samples])

        def detect_trigger() -> int:
            if len(self.vehicle_dynamics_samples) < 50:
                return 0
            else:
                #TODO: extract method
                curr_signal = self.vehicle_dynamics_samples[-1]
                last_signal = self.vehicle_dynamics_samples[0]

                if curr_signal.speed < last_signal.speed:
                    speed_diff = last_signal.speed - curr_signal.speed
                    for key, value in self.criticial_speed_thresholds.items():
                        if speed_diff >= key:
                            return value
                return 0

        try:
            add_signal()
            critical_level = detect_trigger()
            if critical_level > 0:
                report = ReportDTO(
                    schema_version="1.0",
                    vehicle_id="XYZ123", 
                    stop_timestamp=time, 
                    criticality_level=critical_level, 
                    vehicle_dynamics=self.vehicle_dynamics_samples
                )
                self.reports.append(report)

        except json.JSONDecodeError:
            logger.error(f"Error: Could not decode message: '{msg}'")
        except Exception as e:
            logger.error(f"Error: {e}")

def main():
    logger.info("Starting Log Publisher App")
    ecal_core.initialize(sys.argv, "Log Publisher App")
    log_publisher_app = LogPublisherApp()
    log_publisher_app.run()
    ecal_core.finalize()


if __name__ == "__main__":
    # main()
    main()
