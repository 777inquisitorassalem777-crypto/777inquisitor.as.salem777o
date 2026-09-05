// Research-only Unity bridge.
// Connects to PNEVMA NEXUS metrics over WebSocket.
// No actuator/weapon-control interface is exposed.

using System;
using UnityEngine;

[Serializable]
public class PnevmaMetrics {
    public float resonance;
    public float coherence;
    public float energy;
}

public class PnevmaNexusBridge : MonoBehaviour {
    public string serverUrl = "ws://localhost:8000/ws/metrics";

    // Bind your WebSocket client here and map incoming metrics to UI/simulation.
    public void OnMetrics(string json) {
        var metrics = JsonUtility.FromJson<PnevmaMetrics>(json);
        Debug.Log($"Pnevma resonance={metrics.resonance}, coherence={metrics.coherence}");
    }
}
