using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Helios;
using Hermes;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

namespace Apollo
{
    public class ApolloRunner
    {
        public const string manifestSuffix = "_BAKE_MANIFEST.json";


        private static bool uploadFlag = false;
        private static bool quitFlag = false;

        private static Queue<ApolloJob> pendingJobs = null;

        [MenuItem("Pantheon/Apollo/Bake jobs and upload")]
        public static void RunAllJobsUpload()
        {
            uploadFlag = true;
            RunAllBakeJobs();
        }

        //[MenuItem("Apollo/RunAllBakeJobs")]
        public static void RunAllBakeJobs()
        {
            Lightmapping.giWorkflowMode = Lightmapping.GIWorkflowMode.OnDemand;
            string[] allJobsGUIDS = AssetDatabase.FindAssets("t:ApolloJob");
            string[] allJobsPaths = allJobsGUIDS.Select(AssetDatabase.GUIDToAssetPath).ToArray();
            RunBakeJobs(allJobsPaths);
        }

        public static void RunBakeJobs(string[] jobNames)
        {
            string[] allJobsGUIDS = AssetDatabase.FindAssets("t:ApolloJob");
            string[] allJobsPaths = allJobsGUIDS.Select(AssetDatabase.GUIDToAssetPath).ToArray();

            pendingJobs = new Queue<ApolloJob>();
            for (var i = 0; i < jobNames.Length; i++)
            {

                string jobName = jobNames[i];
                string jobpath = allJobsPaths.FirstOrDefault(jp => jp.Contains(jobName));
                if (!string.IsNullOrEmpty(jobpath))
                {
                    ApolloJob job = AssetDatabase.LoadAssetAtPath<ApolloJob>(jobpath);
                    job.OnBakeCompleted = BakeJobCompleted;
                    job.OnBakeFailed = BakeJobFailed;
                    pendingJobs.Enqueue(job);
                }
                else
                {
                    Debug.LogError(string.Format("{0} job NOT FOUND", jobName));
                }



            }
            RunNextBakeJob();
        }

        public static void RunBakeJob(ApolloJob job)
        {
            job.Start();
        }


        public static void RunNextBakeJob()
        {

            if (pendingJobs.Count > 0)
            {

                ApolloJob job = pendingJobs.Dequeue();
                HermesLogger.LogSlack(string.Format("Running {0} baking job", job.name),HermesLogger.ReportLevel.GOOD);
                RunBakeJob(job);
            }
            else
            {
                if (quitFlag)
                {
                    HermesLogger.LogSlack("All jobs finished... quitting",HermesLogger.ReportLevel.GOOD);
                    EditorApplication.Exit(0);
                }
            }


        }


        public static void RunBakeJobsCommand()
        {
            HermesLogger.LogSlack("Starting Bake Process", HermesLogger.ReportLevel.GOOD);
            string[] commands = System.Environment.GetCommandLineArgs();
            quitFlag = true;
            string uploadCommand = commands.FirstOrDefault(com => com.Contains("upload="));
            if (uploadCommand != null)
            {
                bool uploadValue = false;
                bool.TryParse(uploadCommand.Replace("upload=", ""), out uploadValue);
                uploadFlag = uploadValue;
                HermesLogger.LogSlack(string.Format("Upload set to {0}", uploadFlag.ToString()),HermesLogger.ReportLevel.GOOD);
            }

            string jobsCommand = commands.FirstOrDefault(com => com.Contains("jobs="));
            if (jobsCommand != null)
            {
                string[] jobs = jobsCommand.Replace("jobs=", "").Split(',');
                RunBakeJobs(jobs);
            }

            
        }

        private static void BakeJobCompleted(ApolloJob.BakeResult result, FileInfo[] files, ApolloJob job)
        {
            if (result == ApolloJob.BakeResult.COMPLETED)
            {
                if (uploadFlag)
                {
                    foreach (FileInfo file in files)
                    {
                        FTPService.UploadFileSync(file, job.BakeScene.name);
                    }
                }
                //HermesLogger.LogSlack(string.Format("JOB COMPLETED"), HermesLogger.ReportLevel.GOOD);
                Debug.Log("Job Completed");
                RunNextBakeJob();
            }
            else if (result == ApolloJob.BakeResult.ERROR)
            {
                HermesLogger.LogSlack(string.Format("completed with errors"), HermesLogger.ReportLevel.WARN);
                Debug.Log("Job Completed with errors");
                RunNextBakeJob();
            }
        }

        private static void BakeJobFailed(ApolloJob.BakeResult result, Exception exception)
        {
            Debug.LogError(exception.Message);
        }

        [MenuItem("Pantheon/Apollo/Apply job on current scene")]
        public static void ApplyJob()
        {
            string bakeSceneName = EditorSceneManager.GetActiveScene().name;
            string[] apolloJobsGUIDs = AssetDatabase.FindAssets("t:ApolloJob");
            foreach (string apolloJobsGUID in apolloJobsGUIDs)
            {
                ApolloJob job = AssetDatabase.LoadAssetAtPath<ApolloJob>(AssetDatabase.GUIDToAssetPath(apolloJobsGUID));
                if (job.BakeScene.name.Equals(bakeSceneName))
                {
                    job.ApplyJobData();
                    break;

                }
            }
        }

        [MenuItem("Assets/Pantheon/Apollo/Run Job")]
        public static void RunSelectedJob()
        {
            RunBakeJob(Selection.activeObject as ApolloJob);
        }

        [MenuItem("Pantheon/Apollo/Apply all jobs and save")]
        public static void ApplyAllJobsAndSave()
        {
            HermesLogger.LogSlack("Loading all saved bakes",HermesLogger.ReportLevel.GOOD);
            string[] apolloJobsGUIDs = AssetDatabase.FindAssets("t:ApolloJob");
            foreach (string apolloJobsGUID in apolloJobsGUIDs)
            {
                
                ApolloJob job = AssetDatabase.LoadAssetAtPath<ApolloJob>(AssetDatabase.GUIDToAssetPath(apolloJobsGUID));
                HermesLogger.LogSlack(string.Format("Loading {0} job", job.ToString()), HermesLogger.ReportLevel.GOOD);
                job.ApplyJobData();
                EditorSceneManager.SaveOpenScenes();

            }
        }

    }
}
