using System;
using System.IO;
using Athenea;
using Helios;
using Hermes;
using SimpleJSON2;
using UnityEditor;
using UnityEngine;
using ModelImporter = Athenea.ModelImporter;

namespace MyNamespace
{
    public class GenericGenerator
    {

        [MenuItem("Assets/Pantheon/HARDCODED/Generate Generic")]
        public static void GenerateGenericPrefab()
        {
            for (int i = 0; i < Selection.objects.Length; i++)
            {
                var activeObject = Selection.objects[i];
                AssetImporter assetImporter = AssetImporter.GetAtPath(AssetDatabase.GetAssetPath(activeObject));
                UnityEditor.ModelImporter modelImporter = assetImporter as UnityEditor.ModelImporter;
                //string importedAssetPath = modelImporter.assetPath.Replace("Assets", "");
                string modelFolderPath = modelImporter.assetPath.Remove(modelImporter.assetPath.LastIndexOf('/'), modelImporter.assetPath.Length - modelImporter.assetPath.LastIndexOf('/'));
                string assetName = Path.GetFileNameWithoutExtension(modelImporter.assetPath);

                string[] pendingFiles = new string[1];
                pendingFiles[0] = Application.dataPath.Replace("Assets", "") + modelFolderPath + "/" + assetName + ".pending";
                RawModel[] models = ModelImporter.CreateRawModelFromPending(pendingFiles);

                foreach (RawModel rawModel in models)
                {
                    try
                    {
                        rawModel.objectData[0].AsObject["type"].Value = "Prop";
                        rawModel.objectData[0].AsObject["subType"].Value = "Generic";
                        rawModel.objectData[0].AsObject["name"].Value = rawModel.objectData[0].AsObject["name"] + "_AUTO_PROP";

                        if (ModelImporter.ProcessObjects(rawModel))
                        {
                            HermesLogger.Log("Processed FBX  " + rawModel.fbxName);
                            File.Delete(rawModel.pendingFile);
                            ExportLogs.ExportData[] exportedObjectDatas = new ExportLogs.ExportData[rawModel.objectData.Count];
                            for (int j = 0; j < rawModel.objectData.Count; j++)
                            {
                                exportedObjectDatas[j] = new ExportLogs.ExportData();

                                JSONObject importedObjectData = rawModel.objectData[j].AsObject;

                                string objectType = importedObjectData["type"].Value;
                                string objectSubType = importedObjectData["subType"].Value;
                                string objectName = importedObjectData["name"].Value;

                                exportedObjectDatas[j].name = objectName;
                                exportedObjectDatas[j].exportType = objectType;
                                exportedObjectDatas[j].exportSubType = objectSubType;
                            }
                            ExportLogs.ExportLog expLog = new ExportLogs.ExportLog();
                            expLog.filename = rawModel.fbxName;
                            expLog.command = "CreateAvatarFromPendingFiles";
                            expLog.objects = exportedObjectDatas;
                            ExportLogs.CreateLogExport(expLog);
                        }
                    }
                    catch (Exception e)
                    {
                        //CLEAR PROGRESS BAR IF ERROR ENCOUNTERED;
                        EditorUtility.ClearProgressBar();

                        string errmorMsgSimple = "Cannot create prefab for " + rawModel.fbxPath;
                        string errorMsgFull = errmorMsgSimple + "\n\n ----EXCEPTION : " + e.ToString();
                        Debug.LogError(errorMsgFull);
                        ErrorLogs.ErrorLog errLog = new ErrorLogs.ErrorLog();
                        errLog.filename = rawModel.fbxName;
                        errLog.level = "CRASH";
                        errLog.errorMessage = errorMsgFull;
                        errLog.errorCode = 100;
                        ErrorLogs.CreateLogError(errLog);

                        EditorUtility.DisplayDialog("Athenea Step 2 Error", errmorMsgSimple, "OK");
                        //AteneaLogger.AddErrorToCache(errorMsg);
                    }
                }


            }


        }
    }


}
