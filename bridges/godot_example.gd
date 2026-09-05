extends Node
## Research-only Godot bridge.
## Use WebSocket to subscribe to PNEVMA metrics.

var server_url := "ws://localhost:8000/ws/metrics"

func request_insight(context: String):
    print("NEXUS context: ", context)
