using SimpleJSON2;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Athenea
{
    public enum ColliderType { BOX, MESH };

    public struct RawModel
    {
        public string relativeDirectory;
        public string fbxPath;
        public string fbxName;
        public JSONArray materialsData;
        public JSONArray objectData;
        public string pendingFile;
    }

    public struct ColliderData
    {
        public ColliderType colType;
        public string meshName;
        public int id;
    }

    public struct LayerData
    {
        public string meshName;
        public int layer;
    }

    public struct StaticFlagData
    {
        public string meshName;
        public bool batchingStatic;
        public bool lightmapStatic;
        public bool navigationStatic;
        public bool occluderStatic;
        public bool occludeeStatic;
        public bool offMeshLinkGeneration;
        public bool reflectionProbeStatic;
    }

    public struct NavMeshLayerData
    {
        public string meshName;
        public int navmeshLayer;
    }

    public struct SeeThroughGroup
    {
        public string id;
        public SeeThroughBox[] boxes;

    }

    public struct SeeThroughBox
    {
        public GameObject box;
        public ColliderType colType;

    }

    public struct ImportedRoom
    {
        public GameObject box;
        public string id;
    }
}
