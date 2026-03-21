using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class HandReceiver : MonoBehaviour
{
    UdpClient udpClient;
    Thread receiveThread;
    public Vector3[] landmarks = new Vector3[21];
    string latestData = "";

    void Start()
    {
        udpClient = new UdpClient(5052);
        receiveThread = new Thread(ReceiveData);
        receiveThread.IsBackground = true;
        receiveThread.Start();
    }

    void ReceiveData()
    {
        while (true)
        {
            try
            {
                IPEndPoint ep = new IPEndPoint(IPAddress.Any, 0);
                byte[] data = udpClient.Receive(ref ep);
                latestData = Encoding.UTF8.GetString(data);
            }
            catch { }
        }
    }

    void Update()
    {
        if (latestData == "") return;
        try
        {
            var raw = JsonUtility.FromJson<LandmarkWrapper>
                      ("{\"lm\":" + latestData + "}");
            for (int i = 0; i < raw.lm.Length; i++)
            {
                landmarks[i] = new Vector3(
                    raw.lm[i].x * 10f - 5f,
                    -(raw.lm[i].y * 10f - 5f),
                    -raw.lm[i].z * 10f
                );
            }
        }
        catch { }
    }

    void OnDestroy()
    {
        udpClient?.Close();
        receiveThread?.Abort();
    }
}

[System.Serializable]
public class LandmarkData { public float x, y, z; }

[System.Serializable]
public class LandmarkWrapper { public LandmarkData[] lm; }