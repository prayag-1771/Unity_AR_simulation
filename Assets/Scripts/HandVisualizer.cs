using UnityEngine;

public class HandVisualizer : MonoBehaviour
{
    public HandReceiver receiver;
    GameObject[] joints = new GameObject[21];
    LineRenderer[] bones;

    int[][] connections = new int[][] {
        new int[]{0,1}, new int[]{1,2}, new int[]{2,3}, new int[]{3,4},
        new int[]{0,5}, new int[]{5,6}, new int[]{6,7}, new int[]{7,8},
        new int[]{0,9}, new int[]{9,10}, new int[]{10,11}, new int[]{11,12},
        new int[]{0,13}, new int[]{13,14}, new int[]{14,15}, new int[]{15,16},
        new int[]{0,17}, new int[]{17,18}, new int[]{18,19}, new int[]{19,20},
        new int[]{5,9}, new int[]{9,13}, new int[]{13,17}
    };

    void Start()
    {
        // Create joint spheres
        for (int i = 0; i < 21; i++)
        {
            joints[i] = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            joints[i].transform.localScale = Vector3.one * 0.15f;
            var mat = new Material(Shader.Find("Standard"));
            mat.color = new Color(0f, 0.4f, 1f);
            mat.EnableKeyword("_EMISSION");
            mat.SetColor("_EmissionColor", new Color(0f, 0.4f, 1f) * 2f);
            joints[i].GetComponent<Renderer>().material = mat;
        }

        // Create bone lines
        bones = new LineRenderer[connections.Length];
        for (int i = 0; i < connections.Length; i++)
        {
            var go = new GameObject("Bone" + i);
            var lr = go.AddComponent<LineRenderer>();
            lr.startWidth = lr.endWidth = 0.05f;
            lr.material = new Material(Shader.Find("Sprites/Default"));
            lr.startColor = lr.endColor = new Color(0f, 0.6f, 1f, 0.8f);
            lr.positionCount = 2;
            bones[i] = lr;
        }
    }

    void Update()
    {
        if (receiver == null) return;
        
        for (int i = 0; i < 21; i++)
            joints[i].transform.position = receiver.landmarks[i];

        for (int i = 0; i < connections.Length; i++)
        {
            bones[i].SetPosition(0, receiver.landmarks[connections[i][0]]);
            bones[i].SetPosition(1, receiver.landmarks[connections[i][1]]);
        }
    }
}