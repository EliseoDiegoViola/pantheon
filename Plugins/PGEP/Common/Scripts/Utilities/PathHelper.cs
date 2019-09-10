using UnityEngine;
using System.IO;

public class PathHelper {
    
    public static string GetDirectoryFromPath(string path)
    {
        string newDirectory = path.Remove(path.LastIndexOf('/'), path.Length - path.LastIndexOf('/'));
        return newDirectory + "/";
    }
}
