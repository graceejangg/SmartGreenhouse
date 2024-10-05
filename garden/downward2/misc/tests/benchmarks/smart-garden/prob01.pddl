(define (problem smart-garden)
    (:domain smart-garden)
    (:requirements :negative-preconditions :typing)
    (:objects
        humiditySensor - humidity-sensor
        lightSensor - light-sensor
        moistureSensor - moisture-sensor
        temperatureSensor - temperature-sensor
    )
    (:init
        (sensor-value-normal humiditySensor)
        (sensor-value-normal lightSensor)
        (sensor-value-normal moistureSensor)
        (sensor-value-normal temperatureSensor)
    )
    (:goal
        (and (sensor-value-normal humiditySensor)
            (sensor-value-normal lightSensor)
            (sensor-value-normal moistureSensor)
            (sensor-value-normal temperatureSensor)
        )
    )
)