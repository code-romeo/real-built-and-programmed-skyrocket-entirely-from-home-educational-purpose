# Architecture Overview

## System layers

### 1. Simulation Layer
Generates an expected flight profile using simplified physics, atmosphere approximations, and recovery assumptions.

### 2. Avionics Layer
Consumes sensor inputs and estimates the vehicle state using filtering and fusion logic.

### 3. Telemetry Layer
Serializes state and health data into a structured schema for logging and transmission.

### 4. Analysis Layer
Scores anomalies, produces mission reports, and replays flight data for comparison.

## Data flow

`simulator -> sensors -> estimator -> telemetry -> logger -> analysis -> replay`

## Design principles

- modularity
- observability
- reproducibility
- educational clarity
- extensibility

## Strategic focus

The most important contribution is not raw propulsion detail. It is the ability to transform a flight into structured aerospace data that can be understood, replayed, and improved.
