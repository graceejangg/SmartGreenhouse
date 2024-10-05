(define (domain smart-garden)
    (:requirements :typing :negative-preconditions)

    (:types
        moisture-sensor humidity-sensor temperature-sensor light-sensor - sensor
        pump - actuator
        plant
    )

    (:predicates
        (sensor-value-low ?s - sensor)
        (sensor-value-normal ?s - sensor)
        (sensor-value-high ?s - sensor)
    )

    (:action increase-value
        :parameters (?s - sensor)
        :precondition (sensor-value-low ?s)
        :effect (and (sensor-value-normal ?s) (not (sensor-value-low ?s)))
    )

    (:action decrease-value
        :parameters (?s - sensor)
        :precondition (sensor-value-high ?s)
        :effect (and (sensor-value-normal ?s) (not (sensor-value-high ?s)))
    )
)