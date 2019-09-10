using System;
using System.Collections.Generic;
using System.Diagnostics;
using UnityEngine;
using UnityEditor;
using UnityEditor.Animations;
using System.IO;
using System.Linq;
using Hermes;
using Debug = UnityEngine.Debug;

namespace Athenea
{
	public class ImportUtilities{


        public struct AnimationData{
			public string animName;
		}


		#region Editor Utilities
		#if UNITY_EDITOR
        // #ATHENEA METHOD#
        #endif
        #endregion

        public struct UnityFile<T> where T : UnityEngine.Object
        {
            public T file;
            public string path;
        }

        public static UnityFile<T> FindFileInParents<T>(string fileName, string startDirectory, string subFolder = "") where T : UnityEngine.Object
        {

            string directoryCache = startDirectory;
            string searchPatttern = directoryCache + subFolder;
            UnityFile<T> uFile = new UnityFile<T>();

            T foundFile = AssetDatabase.LoadAssetAtPath<T>(searchPatttern + "/" + fileName);
            if (foundFile != null)
            {
                uFile.file = foundFile;
                uFile.path = searchPatttern + "/" + fileName;
                return uFile;
            }

            while ((foundFile == null) && !(GetParentFolder(directoryCache).Equals(directoryCache)))
            {
                directoryCache = GetParentFolder(directoryCache);
                searchPatttern = directoryCache + subFolder;
                foundFile = AssetDatabase.LoadAssetAtPath<T>(searchPatttern + "/" + fileName);

                if (foundFile != null)
                {
                    uFile.file = foundFile;
                    uFile.path = searchPatttern + "/" + fileName;
                    return uFile;
                }
            }

            uFile.file = null;
            uFile.path = "";
            return uFile;
        }

        public static string GetParentFolder(string folder)
        {
            int slashIndex = folder.LastIndexOf("/");
            folder = slashIndex < 0 ? folder : folder.Remove(slashIndex);
            int backslashIndex = folder.LastIndexOf("\\");
            folder = backslashIndex < 0 ? folder : folder.Remove(backslashIndex);
            return folder;
        }

        public static void SetColliders(GameObject root, ColliderData[] cols) {
            if (cols != null)
            {
                foreach (var collider in cols)
                {
                    Transform child = root.transform.FindDeepChild(collider.meshName);
                    if (child != null)
                    {
                        if (collider.colType == ColliderType.BOX) {
                            child.gameObject.AddComponent<BoxCollider>();

                            MeshFilter mfilter = child.gameObject.GetComponent<MeshFilter>();
                            if (mfilter) GameObject.DestroyImmediate(mfilter);
                        } else {
                            MeshFilter mfilter = child.gameObject.GetComponent<MeshFilter>();
                            child.gameObject.AddComponent<MeshCollider>().sharedMesh = mfilter.sharedMesh;
                        }

                        Renderer rend = child.gameObject.GetComponent<Renderer>();
                        if (rend) GameObject.DestroyImmediate(rend);
                    }
                    else
                    {
                        Debug.LogError("Cannot set Colliders " + collider.meshName);
                    }
                }
            }
        }
        public static void SetStaticTags(GameObject root, StaticFlagData[] staFlags) {
            if (staFlags != null)
            {
                foreach (var staticFlags in staFlags)
                {
                    Transform child = root.transform.FindDeepChild(staticFlags.meshName);
                    if (child != null)
                    {
                        StaticEditorFlags flags = 0;

                        if (staticFlags.batchingStatic) { flags = flags | StaticEditorFlags.BatchingStatic; }
                        if (staticFlags.lightmapStatic) { flags = flags | StaticEditorFlags.LightmapStatic; }
                        if (staticFlags.navigationStatic) { flags = flags | StaticEditorFlags.NavigationStatic; }
                        if (staticFlags.occludeeStatic) { flags = flags | StaticEditorFlags.OccludeeStatic; }
                        if (staticFlags.occluderStatic) { flags = flags | StaticEditorFlags.OccluderStatic; }
                        if (staticFlags.offMeshLinkGeneration) { flags = flags | StaticEditorFlags.OffMeshLinkGeneration; }
                        if (staticFlags.reflectionProbeStatic) { flags = flags | StaticEditorFlags.ReflectionProbeStatic; }

						child.gameObject.ChangeStaticStateRecursively(flags);
                    }
                    else {
                        Debug.LogError("Cannot set Tags " + staticFlags.meshName);
                    }
                }
            }
        }
        public static void SetNavmesh(GameObject root, NavMeshLayerData[] navData) {
            if (navData != null)
            {
                foreach (var navmeshLayer in navData)
                {
                    Transform child = root.transform.FindDeepChild(navmeshLayer.meshName);
                    if (child != null)
                    {
                        child.gameObject.ChangeNavMeshLayerRecursively(navmeshLayer.navmeshLayer);
                    }
                    else
                    {
                        Debug.LogError("Cannot set NavMesh " + navmeshLayer.meshName);
                    }
                }
            }

        }
        public static void SetLayer(GameObject root, LayerData[] layDatas) {
            if (layDatas != null)
            {
                foreach (var layer in layDatas)
                {
                    Transform child = root.transform.FindDeepChild(layer.meshName);
                    if (child != null)
                    {
						child.ChangeLayersRecursively (layer.layer);
                    }
                    else
                    {
                        Debug.LogError("Cannot set Layer to" + layer.meshName);
                    }
                }
            }
        }

        public static void CreateOverrideController(GameObject root, bool uniqueness, RuntimeAnimatorController baseAnimator) {

            Animator animator = root.GetComponent<Animator>();
            if (animator == null)
            {
                Debug.LogError(root.name + " HAS NO ANIMATOR?");
                return;
            }
            string assetPath = AssetDatabase.GetAssetPath(animator.avatar);
            AnimationClip[] clips = AteneaExtensions.LoadAllAssetsAtPath<AnimationClip>(assetPath);

            if (uniqueness)
            {
                string assetFolderPath = Path.GetDirectoryName(assetPath);
                AnimatorController newAnimator = AnimatorController.CreateAnimatorControllerAtPath(assetFolderPath + "/" + root.name + "_controller_.controller");

                //newAnimator.AddMotion(new Motion())
                //Si es unico , crear el  animator y consfigurarlo terminar.

                animator.runtimeAnimatorController = newAnimator;

            }
            else
            {

                AnimatorOverrideController dummyOverride = new AnimatorOverrideController
                {
                    runtimeAnimatorController = baseAnimator
                };

                List<KeyValuePair<AnimationClip, AnimationClip>> overrides = new List<KeyValuePair<AnimationClip, AnimationClip>>();
                foreach (var originalClip in dummyOverride.animationClips) {
                    var found = clips.FirstOrDefault((clip) => originalClip.name.Equals(clip.name));
                    KeyValuePair <AnimationClip, AnimationClip> pair = new KeyValuePair<AnimationClip, AnimationClip>(originalClip, found);
                    overrides.Add(pair);
                }

                dummyOverride.ApplyOverrides(overrides);

                string assetFolderPath = Path.GetDirectoryName(assetPath);
                UnityEditor.AssetDatabase.CreateAsset(dummyOverride, assetFolderPath + "/" + root.name + "_Override.overrideController");
                animator.runtimeAnimatorController = dummyOverride;
            }
            
        }
        public static void SetUpDestructibleCover(GameObject root, GameObject rootDestroyed, GameObject[] dynamics) {
            
            rootDestroyed.gameObject.SetActive(false);
            if (dynamics == null) return;
            foreach (GameObject dyn in dynamics) {
                MeshCollider col = dyn.AddComponent<MeshCollider>();
                col.convex = true;
                col.sharedMesh = dyn.GetComponent<MeshFilter>().sharedMesh;
                dyn.AddComponent<Rigidbody>();
            }
        }



	    // ON IMPORT
        public static void BlendShapeClipProcess(UnityEditor.ModelImporter assetImporter)
        {            
            string pataSelection = assetImporter.assetPath;
            string copyPath = Path.GetDirectoryName(pataSelection) + "/";
            UnityEngine.Object[] objs = AssetDatabase.LoadAllAssetsAtPath(assetImporter.assetPath).Where(x => (x is AnimationClip && !x.name.Contains("__preview__"))).ToArray();
            string assetPath = assetImporter.assetPath;//AssetDatabase.GetAssetPath(fbxFile);
            foreach (AnimationClip src in objs)
            {
                AnimationClip outputAnimClip = AssetDatabase.LoadMainAssetAtPath(copyPath + src.name + ".anim") as AnimationClip;
                if (outputAnimClip != null)
                {
                    EditorUtility.CopySerialized(src, outputAnimClip);
                    AssetDatabase.SaveAssets();
                }
                else
                {
                    outputAnimClip = new AnimationClip();
                    EditorUtility.CopySerialized(src, outputAnimClip);
                    AssetDatabase.CreateAsset(outputAnimClip, copyPath + src.name + ".anim");
                }
                AssetDatabase.Refresh();
                EditorCurveBinding[] curveDatas = AnimationUtility.GetCurveBindings(src);
                int totalBlenshapes = 24;
                int currentBlendshapeCount = 0;
                for (int i = 0; i < curveDatas.Length; i++)
                {
                    AnimationCurve ac = AnimationUtility.GetEditorCurve(src, curveDatas[i]);
                    if (curveDatas[i].propertyName.Contains("BS"))
                    {
                        curveDatas[i].type = typeof(SkinnedMeshRenderer);
                        curveDatas[i].path = "c_meshes_00_grp/HEAD";
                        curveDatas[i].propertyName = "blendShape.c_Head_00_bsh." + curveDatas[i].propertyName;
                        currentBlendshapeCount++;
                    }

                    AnimationUtility.SetEditorCurve(outputAnimClip, curveDatas[i], ac);
                    if (currentBlendshapeCount >= totalBlenshapes)
                    {
                        break;
                    }
                }

            }
            (assetImporter as UnityEditor.ModelImporter).importAnimation = false;
            (assetImporter as UnityEditor.ModelImporter).animationType = ModelImporterAnimationType.None;
            AssetDatabase.WriteImportSettingsIfDirty(assetPath);
            AssetDatabase.ImportAsset(assetPath, ImportAssetOptions.ForceUpdate);


        }
    }

}