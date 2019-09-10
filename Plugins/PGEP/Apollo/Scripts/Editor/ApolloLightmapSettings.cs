using UnityEditor;
using UnityEngine;

namespace Apollo
{

    public class ApolloLightmapSettings : ScriptableObject
    {

        public float indirectResolution;
        public int lightmapPadding;
        public float lightmapResolution;
        public LightmapSize lightmapSize;
        public LightmapParameters lightmapParameters;

        public enum LightmapSize
        {
            Size_32 = 0,
            Size_64 = 1,
            Size_128 = 2,
            Size_256 = 3,
            Size_512 = 4,
            Size_1024 = 5,
            Size_2048 = 6,
            Size_4096 = 7,
        }

        public static int[] LightmapSizeValues = new int[]
        {
            32,
            64,
            128,
            256,
            512,
            1024,
            2048,
            4096
        };

        [MenuItem("Assets/Create/Apollo/Apollo Lightmap Settings")]
        public static void CreateMyAsset()
        {
            ApolloLightmapSettings asset = ScriptableObject.CreateInstance<ApolloLightmapSettings>();

            AssetDatabase.CreateAsset(asset, AssetDatabase.GetAssetPath(Selection.objects[0]) + "/NewApolloSettings.asset");
            AssetDatabase.SaveAssets();

            EditorUtility.FocusProjectWindow();

            Selection.activeObject = asset;
        }
    }
}
