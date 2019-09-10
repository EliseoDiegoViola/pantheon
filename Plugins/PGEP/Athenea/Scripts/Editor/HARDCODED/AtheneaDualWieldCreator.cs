//using System.Collections;
//using System.Collections.Generic;
//using UnityEngine;
//using UnityEditor;
//using Ergo.SenseSystem;
//using ElementSpace;

//public class AteneaDualWieldCreator : EditorWindow {
    
//    [MenuItem("Tools/Artists/DualWield Creator")]
//    static void Init()
//    {
//        EditorWindow.GetWindow<AteneaDualWieldCreator>("DualWield Creator");
//    }

//    private string prefabName = "NewDualWieldWeapon";
//    private GameObject mainWeapon;
//    private GameObject offHandWeapon;
//    private bool allSetted = false;
//    private Transform mainWeaponOffHandTarget;

//    private void OnGUI()
//    {
//        prefabName = EditorGUILayout.TextField("Prefab Name: ", prefabName);

//        mainWeapon = EditorGUILayout.ObjectField("Main Hand:", mainWeapon, typeof(GameObject), true) as GameObject;
//        offHandWeapon = EditorGUILayout.ObjectField("Offhand Hand:", offHandWeapon, typeof(GameObject), true) as GameObject;
//        mainWeaponOffHandTarget = EditorGUILayout.ObjectField("Offhand Container:", mainWeaponOffHandTarget, typeof(Transform), true) as Transform;

//        allSetted = true;
//        if (offHandWeapon == null || mainWeapon == null)
//        {
//            allSetted = false;
//        }

//        if (!allSetted)
//        {
//            EditorGUILayout.HelpBox("Fill both weapon slots to create the dual wield weapon", MessageType.Info);
//            if (!string.IsNullOrEmpty(prefabName))
//                prefabName = "";
//        } else
//        {
//            if (string.IsNullOrEmpty(prefabName))
//                prefabName = mainWeapon.name + "_Final";
//        }

//        EditorGUI.BeginDisabledGroup(!allSetted);
//        if (GUILayout.Button("Create Dual Wield Weapon"))
//        {
//            CreateWeapon();
//        }
//        EditorGUI.EndDisabledGroup();
//    }

//    void CreateWeapon()
//    {
//        //CREATE A COPY OF BOTH WEAPONS
//        GameObject mainWeaponCopy = Instantiate<GameObject>(mainWeapon);
//        GameObject offHandWeaponCopy = Instantiate<GameObject>(offHandWeapon);
//        offHandWeaponCopy.name = offHandWeapon.name;

//        //REMOVE UNNECESARY COMPONENTS
//        if (offHandWeaponCopy.GetComponent<MeleeWeapon>())
//            DestroyImmediate(offHandWeaponCopy.GetComponent<MeleeWeapon>());

//        //REPARENT THE OFFHAND COPY TO THE CONTAINER IN THE MAIN HAND
//        Transform offHandContainer;
//        if (mainWeaponOffHandTarget == null)
//        {
//            mainWeaponOffHandTarget = mainWeaponCopy.transform.FindDeepChild("leftHandTarget");
//            if (mainWeaponOffHandTarget == null)
//            {
//                Debug.LogError("AteneaDualWieldCreator | ERROR: Esta mal seteado el container de la offset weapon!");
//                return;
//            }
//            offHandContainer = mainWeaponOffHandTarget;
//        } else
//        {
//            offHandContainer = mainWeaponCopy.transform.FindDeepChild(mainWeaponOffHandTarget.name);
//        }

//        offHandWeaponCopy.transform.SetParent(offHandContainer, false);
//        offHandWeaponCopy.transform.localRotation = Quaternion.identity;

//        mainWeaponCopy.name = prefabName;

//        GameObject originalPrefab = mainWeapon;
//        if (PrefabUtility.GetPrefabType(mainWeapon) == PrefabType.PrefabInstance)
//        {
//            originalPrefab = PrefabUtility.GetPrefabParent(mainWeapon) as GameObject;
//        }

//        string originalPrefabPath = AssetDatabase.GetAssetPath(originalPrefab);
//        string prefabFolder = PathHelper.GetDirectoryFromPath(originalPrefabPath);
//        string prefabPath = prefabFolder + prefabName + ".prefab";
//        if (!prefabPath.ToLower().Contains(AppSettings.ARTMASTERS_PATH.ToLower())) {
//            //ESTAS QUERIENDO GUARDAR UN PREFAB DE ARTMASTERS EN UNA CARPETA FUERA DE ARTMASTERS
//            //PEDIRLE AL USUARIO QUE DE UN PATH CORRECTO!
//            string defaultPath = Application.dataPath + "/" + AppSettings.ARTMASTERS_PATH + "Weapons";
//            prefabPath = EditorUtility.SaveFilePanelInProject("Save Prefab", prefabName, "prefab", "Enter prefab name", defaultPath);
//            if (prefabPath.Length == 0)
//            {
//                Debug.Log("AteneaDualWieldCreator | No path specified, returning!");
//                return;
//            }              
//        }

//        GameObject oldPrefab = (AssetDatabase.LoadAssetAtPath<GameObject>(prefabPath));
//        if (oldPrefab != null)
//            PrefabUtility.ReplacePrefab(mainWeaponCopy, oldPrefab, ReplacePrefabOptions.ConnectToPrefab);
//        else
//            PrefabUtility.CreatePrefab(prefabPath, mainWeaponCopy, ReplacePrefabOptions.ConnectToPrefab);

//        DestroyImmediate(mainWeaponCopy);
//    }
//}
