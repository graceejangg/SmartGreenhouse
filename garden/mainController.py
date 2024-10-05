import json
from executor.planExecute import PlanExecutor
import mqtt.mqttClient as mqtt
import logging
import subprocess
import os
from pddl.logic import Predicate
from pddl.logic.base import And
from pddl.core import Problem
from pddl.formatter import problem_to_string
from pddl import parse_domain, parse_problem


plannumber = 17

mqtt_hostname = "mosquitto"
mqtt_port = 1883
sensorValues = {}

planExecutor = None


def getPlannumber():
    global plannumber
    if plannumber > 16:
        plannumber = 0
    else:
        plannumber += 1
    return plannumber


def run_fast_downward(domain_file, problem_file, plan_file="/planning/out"):
    downward_dir = "downward"
    downward_command = [
        os.path.join(downward_dir, "fast-downward.py"),
        "--alias", "seq-sat-lama-2011", "--plan-file", plan_file,
        domain_file,
        problem_file
    ]

    try:
        result = subprocess.run(
            downward_command, capture_output=True, text=True, check=True)
        print(result.stdout)

        # Read the plan file
        if os.path.exists(plan_file+".1"):
            with open(plan_file+".1", 'r') as file:
                plan = file.readlines()
            return plan
        else:
            print("Plan file not found.")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error running Fast Downward: {e}")
        print(e.stdout)
        print(e.stderr)
        return None


def createPlan(sensor_type, sensor_value):
    logging.debug(f"Creating plan for {sensor_type} with value {sensor_value}")

    domain_path = '/planning/domain.pddl'
    problem_path = "/planning/prob01.pddl"
    domain = parse_domain(domain_path)
    problem = parse_problem(problem_path)

    objects = {obj.name: obj for obj in list(problem.objects)}
    sensor = objects[sensor_type]
    state = 'normal'
    
    sensor_thresholds = {
        'temperature': (21, 29),
        'moisture': (300, 700),
        'humidity': (60, 70),
        'light': (300, 700)
    }

    lower, upper = sensor_thresholds[sensor_type]
    
    if sensor_value < lower:
        state = 'low'
    elif sensor_value > upper:
        state = 'high'
    else:
        state = 'normal'

    problem = Problem(
        name=problem.name,
        domain=domain,
        objects=problem.objects,
        init=[Predicate(f"sensor-value-{state}", sensor)],
        goal=Predicate("dummy-goal-achieved") & Predicate("sensor-value-normal", sensor)
    )

    with open(problem_path, 'w') as f:
        f.write(problem_to_string(problem))
        
    return run_fast_downward(domain_path, problem_path, f"/planning/out_{getPlannumber()}")


def actOnMessage(topic, payload):
    print(f"Received message on topic {topic}: {payload}")

    sensor_types = ['temperature', 'humidity', 'moisture', 'light']
    sensor_type = topic.split("/")[-1]

    if sensor_type in sensor_types:
        sensor_value = json.loads(payload)['value']
        plan = createPlan(sensor_type, sensor_value)
        if plan:
            planExecutor.executePlan(plan)
        else:
            logging.debug("Planning failed.")


def main():
    global planExecutor

    client = mqtt.MqttClient(mqtt_hostname, mqtt_port)
    logging.debug("Start")

    planExecutor = PlanExecutor(client)

    client.callback = actOnMessage
    client.subscribe("garden/+")

    while True:
        pass


# Example usage
if __name__ == "__main__":
    main()
