//using System.Collections;
//using System.Collections.Generic;
//using UnityEngine;
//using UnityEditor;

//public class NavMeshFixerEditor{

//    [MenuItem ("Assets/Navmesh/MAKE - WALKABLE")]
//    public static void MakeWalkable(){
//        GameObject[] allPrefabs = Selection.gameObjects;
//        for(int i = 0; i < allPrefabs.Length; i++){
//            allPrefabs[i].ChangeStaticStateRecursively(StaticEditorFlags.BatchingStatic | 
//                StaticEditorFlags.LightmapStatic | 
//                StaticEditorFlags.NavigationStatic | 
//                StaticEditorFlags.OccludeeStatic |
//                StaticEditorFlags.OccluderStatic |
//                StaticEditorFlags.ReflectionProbeStatic);

//            allPrefabs[i].layer = LayerMask.NameToLayer("LAYOUT_FLOOR");

//            if(! allPrefabs[i].GetComponent<MeshCollider>())
//            {
//                allPrefabs[i].AddComponent<MeshCollider>().sharedMesh = allPrefabs[i].GetComponent<MeshFilter>().sharedMesh;
//            }
                

//            StaticEditorFlags objFlag = StaticEditorFlags.OffMeshLinkGeneration;
//            objFlag = objFlag | StaticEditorFlags.BatchingStatic;
//            objFlag = objFlag | StaticEditorFlags.LightmapStatic;
//            objFlag = objFlag | StaticEditorFlags.NavigationStatic;
//            objFlag = objFlag | StaticEditorFlags.OccludeeStatic;
//            objFlag = objFlag | StaticEditorFlags.OccluderStatic;
//            objFlag = objFlag | StaticEditorFlags.ReflectionProbeStatic;

//            allPrefabs[i].gameObject.ChangeStaticStateRecursively(objFlag);

//            GameObjectUtility.SetNavMeshArea(allPrefabs[i],0);


//        }
//    }

//    [MenuItem ("Assets/Navmesh/MAKE - NOT WALKABLE")]
//    public static void MakeNOTWalkable(){
//        GameObject[] allPrefabs = Selection.gameObjects;
//        for(int i = 0; i < allPrefabs.Length; i++){
//            allPrefabs[i].ChangeStaticStateRecursively(StaticEditorFlags.BatchingStatic | 
//                StaticEditorFlags.LightmapStatic | 
//                StaticEditorFlags.NavigationStatic | 
//                StaticEditorFlags.OccludeeStatic |
//                StaticEditorFlags.OccluderStatic |
//                StaticEditorFlags.ReflectionProbeStatic);

//            allPrefabs[i].layer = LayerMask.NameToLayer("LAYOUT_FLOOR");

//            if(! allPrefabs[i].GetComponent<MeshCollider>())
//            {
//                allPrefabs[i].AddComponent<MeshCollider>().sharedMesh = allPrefabs[i].GetComponent<MeshFilter>().sharedMesh;
//            }

//            StaticEditorFlags objFlag = StaticEditorFlags.OffMeshLinkGeneration;
//            objFlag = objFlag | StaticEditorFlags.BatchingStatic;
//            objFlag = objFlag | StaticEditorFlags.LightmapStatic;
//            objFlag = objFlag | StaticEditorFlags.NavigationStatic;
//            objFlag = objFlag | StaticEditorFlags.OccludeeStatic;
//            objFlag = objFlag | StaticEditorFlags.OccluderStatic;
//            objFlag = objFlag | StaticEditorFlags.ReflectionProbeStatic;

//            allPrefabs[i].gameObject.ChangeStaticStateRecursively(objFlag);

//            GameObjectUtility.SetNavMeshArea(allPrefabs[i],1);


//        }
//    }
        
//}
