using UnityEditor;
using UnityEngine;

namespace Athenea
{

    public class MaterialPicker : Editor
    {

        //private static bool picking = false;

        //[ErgoMenuItem("GET MATERIAL FROM OBJECT")]
        //static void Pick(Event e)
        //{
        //    Debug.Log(e.mousePosition);
        //    int i;
        //    GameObject goPick = HandleUtility.PickGameObject(e.mousePosition, out i);

        //    Debug.Log(goPick);
        //    Debug.Log(i);
        //}


        [MenuItem("Window/Scene GUI/Material Picker %Q")]
        public static void Pick()
        {
            SceneView.onSceneGUIDelegate += OnScene;

        }

        private static void OnScene(SceneView sceneview)
        {
            int i;
            GameObject goPick = HandleUtility.PickGameObject(Event.current.mousePosition, out i);

            if (goPick != null && goPick.GetComponent<Renderer>() != null) {
                Renderer r = goPick.GetComponent<Renderer>();
                Material m = r.sharedMaterials[i];
                EditorGUIUtility.PingObject(m.GetInstanceID());
                
            }
            
            SceneView.onSceneGUIDelegate -= OnScene;
            


        }
    }
}

