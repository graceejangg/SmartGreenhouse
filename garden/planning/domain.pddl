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
        (dummy-goal-achieved)
    )

    (:action increase_
        :parameters (?s - sensor)
        :precondition (sensor-value-low ?s)
        :effect (and (sensor-value-normal ?s) (not (sensor-value-low ?s)))
    )

    (:action decrease_
        :parameters (?s - sensor)
        :precondition (sensor-value-high ?s)
        :effect (and (sensor-value-normal ?s) (not (sensor-value-high ?s)))
    )

    (:action achieve-dummy-goal
        :parameters ()
        :precondition (not (dummy-goal-achieved))
        :effect (dummy-goal-achieved)
    )
)