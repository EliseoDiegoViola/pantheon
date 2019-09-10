using System;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

namespace Athenea
{
    public static class UnityExtensions
    {
        //HAVE TO BE REWORKED


        
        

        /// <summary>
        /// Finds named childs or grandchilds of a Transform.
        /// </summary>
        /// <param name="aParent"></param>
        /// <param name="aName"></param>
        /// <returns></returns>
        public static IEnumerable<GameObject> FindInnerChilds(this Transform aParent, string aName)
        {

            //CHECK SAME OBJECT FIRST
            if (aParent.name.ToLower().Equals(aName.ToLower()))
                yield return aParent.gameObject;

            foreach (Transform child in aParent)
            {
                foreach (var foundChild in child.FindInnerChilds(aName))
                {
                    yield return foundChild;
                }
            }
        }

        /// <summary>
        /// Finds named childs or grandchilds of a GameObject.
        /// </summary>
        /// <param name="aParent"></param>
        /// <param name="aName"></param>
        /// <returns></returns>
        public static IEnumerable<GameObject> FindInnerChilds(this GameObject aParent, string aName)
        {
            return aParent.transform.FindInnerChilds(aName);
        }

        /// <summary>
        /// Finds named childs or grandchilds of a Transform.
        /// </summary>
        /// <param name="aParent"></param>
        /// <param name="aName"></param>
        /// <returns></returns>
        public static IEnumerable<GameObject> FindInnerChildsNot(this Transform aParent, string aName)
        {

            //CHECK SAME OBJECT FIRST
            if (!aParent.name.ToLower().Equals(aName.ToLower()))
                yield return aParent.gameObject;

            foreach (Transform child in aParent)
            {
                foreach (var foundChild in child.FindInnerChildsNot(aName))
                {
                    yield return foundChild;
                }
            }
        }

        /// <summary>
        /// Finds named childs or grandchilds of a GameObject.
        /// </summary>
        /// <param name="aParent"></param>
        /// <param name="aName"></param>
        /// <returns></returns>
        public static IEnumerable<GameObject> FindInnerChildsNot(this GameObject aParent, string aName)
        {
            return aParent.transform.FindInnerChildsNot(aName);
        }

        /// <summary>
        /// Finds named childs or grandchilds of a Transform.
        /// </summary>
        /// <param name="aParent"></param>
        /// <param name="aName"></param>
        /// <returns></returns>
        public static IEnumerable<GameObject> FindInnerChildsContains(this Transform aParent, string aName)
        {

            //CHECK SAME OBJECT FIRST
            if (aParent.name.ToLower().Contains(aName.ToLower()))
                yield return aParent.gameObject;

            foreach (Transform child in aParent)
            {
                foreach (var foundChild in child.FindInnerChildsContains(aName))
                {
                    yield return foundChild;
                }
            }
        }

        /// <summary>
        /// Finds named childs or grandchilds of a GameObject.
        /// </summary>
        /// <param name="aParent"></param>
        /// <param name="aName"></param>
        /// <returns></returns>
        public static IEnumerable<GameObject> FindInnerChildsContains(this GameObject aParent, string aName)
        {
            return aParent.transform.FindInnerChildsContains(aName);
        }

        /// <summary>
        /// Finds named childs or grandchilds of a Transform.
        /// </summary>
        /// <param name="aParent"></param>
        /// <param name="aName"></param>
        /// <returns></returns>
        public static IEnumerable<GameObject> FindInnerChildsNotContains(this Transform aParent, string aName)
        {

            //CHECK SAME OBJECT FIRST
            if (!aParent.name.ToLower().Contains(aName.ToLower()))
                yield return aParent.gameObject;

            foreach (Transform child in aParent)
            {
                foreach (var foundChild in child.FindInnerChildsNotContains(aName))
                {
                    yield return foundChild;
                }
            }
        }

        /// <summary>
        /// Finds named childs or grandchilds of a GameObject.
        /// </summary>
        /// <param name="aParent"></param>
        /// <param name="aName"></param>
        /// <returns></returns>
        public static IEnumerable<GameObject> FindInnerChildsNotContains(this GameObject aParent, string aName)
        {
            return aParent.transform.FindInnerChildsNotContains(aName);
        }

        /// <summary>
        /// Finds a named child or grandchild of a Transform.
        /// </summary>
        /// <param name="aParent"></param>
        /// <param name="aName"></param>
        /// <returns></returns>
        public static GameObject FindInnerChildContains(this Transform aParent, string aName)
        {
            //CHECK SAME OBJECT FIRST
            if (aParent.name.ToLower().Contains(aName.ToLower()))
                return aParent.gameObject;

            foreach (Transform child in aParent)
            {
                return aParent.FindInnerChildContains(aName);
            }
            return null;
        }

        /// <summary>
        /// Finds named childs or grandchilds of a GameObject.
        /// </summary>
        /// <param name="aParent"></param>
        /// <param name="aName"></param>
        /// <returns></returns>
        public static IEnumerable<GameObject> FindInnerChildContains(this GameObject aParent, string aName)
        {
            return aParent.FindInnerChildContains(aName);
        }

        /// <summary>
        /// Finds a named child or grandchild of a Transform.
        /// </summary>
        /// <param name="aParent"></param>
        /// <param name="aName"></param>
        /// <returns></returns>
        public static GameObject FindInnerChild(this Transform aParent, string aName)
        {
            //CHECK SAME OBJECT FIRST
            if (aParent.name.ToLower().Equals(aName.ToLower()))
                return aParent.gameObject;

            foreach (Transform child in aParent)
            {
                return aParent.FindInnerChildContains(aName);
            }
            return null;
        }

        /// <summary>
        /// Finds named childs or grandchilds of a GameObject.
        /// </summary>
        /// <param name="aParent"></param>
        /// <param name="aName"></param>
        /// <returns></returns>
        public static IEnumerable<GameObject> FindInnerChild(this GameObject aParent, string aName)
        {
            return aParent.FindInnerChild(aName);
        }

        /// <summary>
        /// Finds a named child or grandchild of a Transform.
        /// </summary>
        /// <param name="aParent"></param>
        /// <param name="aName"></param>
        /// <returns></returns>
        public static GameObject FindInnerChildNotContains(this Transform aParent, string aName)
        {
            //CHECK SAME OBJECT FIRST
            if (aParent.name.ToLower().Contains(aName.ToLower()))
                return aParent.gameObject;

            foreach (Transform child in aParent)
            {
                return aParent.FindInnerChildContains(aName);
            }
            return null;
        }

        /// <summary>
        /// Finds named childs or grandchilds of a GameObject.
        /// </summary>
        /// <param name="aParent"></param>
        /// <param name="aName"></param>
        /// <returns></returns>
        public static IEnumerable<GameObject> FindInnerChildNotContains(this GameObject aParent, string aName)
        {
            return aParent.FindInnerChildNotContains(aName);
        }

        /// <summary>
        /// Finds a named child or grandchild of a Transform.
        /// </summary>
        /// <param name="aParent"></param>
        /// <param name="aName"></param>
        /// <returns></returns>
        public static GameObject FindInnerChildNot(this Transform aParent, string aName)
        {
            //CHECK SAME OBJECT FIRST
            if (aParent.name.ToLower().Equals(aName.ToLower()))
                return aParent.gameObject;

            foreach (Transform child in aParent)
            {
                return aParent.FindInnerChildContains(aName);
            }
            return null;
        }

        /// <summary>
        /// Finds named childs or grandchilds of a GameObject.
        /// </summary>
        /// <param name="aParent"></param>
        /// <param name="aName"></param>
        /// <returns></returns>
        public static IEnumerable<GameObject> FindInnerChildNot(this GameObject aParent, string aName)
        {
            return aParent.FindInnerChildNot(aName);
        }

        public static void SetValue(this SerializedProperty sProperty, object value, Type type)
        {
            if (type == typeof(int))
            {
                sProperty.intValue = (int)value;
            }
            else if (type == typeof(long))
            {
                sProperty.longValue = (long) value;
            }
            else if (type == typeof(float))
            {
                sProperty.floatValue = (float)value;
            }
            else if (type == typeof(double))
            {
                sProperty.doubleValue = (double)value;
            }
            else if (type == typeof(bool))
            {
                sProperty.boolValue = (bool)value;
            }
            else if (type == typeof(string))
            {
                sProperty.stringValue = (string)value;
            }
            else if (type == typeof(Vector2))
            {
                sProperty.vector2Value = (Vector2)value;
            }
            else if (type == typeof(Vector3))
            {
                sProperty.vector3Value = (Vector3)value;
            }
            else if (type == typeof(Vector4))
            {
                sProperty.vector4Value = (Vector4)value;
            }
            else if (type == typeof(Color))
            {
                sProperty.colorValue = (Color)value;

            }
            else if (type == typeof(Bounds))
            {
                sProperty.boundsValue = (Bounds)value;
            }
            else if (type == typeof(UnityEngine.Object))
            {
                sProperty.objectReferenceValue = (UnityEngine.Object)value; 
            }
        }

        public static object GetValue<T>(this SerializedProperty sProperty)
        {
            if (typeof(T) == typeof(int))
            {
                return sProperty.intValue;
            }
            else if (typeof(T) == typeof(long))
            {
                return sProperty.longValue;
            }
            else if (typeof(T) == typeof(float))
            {
                return sProperty.floatValue;
            }
            else if (typeof(T) == typeof(double))
            {
                return sProperty.doubleValue;
            }
            else if (typeof(T) == typeof(bool))
            {
                return sProperty.boolValue;
            }
            else if (typeof(T) == typeof(string))
            {
                return sProperty.stringValue;
            }
            else if (typeof(T) == typeof(Vector2))
            {
                return sProperty.vector2Value;
            }
            else if (typeof(T) == typeof(Vector3))
            {
                return sProperty.vector3Value;
            }
            else if (typeof(T) == typeof(Vector4))
            {
                return sProperty.vector4Value;
            }
            else if (typeof(T) == typeof(Color))
            {
                return sProperty.colorValue;

            }
            else if (typeof(T) == typeof(Bounds))
            {
                return sProperty.boundsValue;
            }
            else if (typeof(T) == typeof(UnityEngine.Object))
            {
                return sProperty.objectReferenceValue;
            }
            return default(T);
        }



    }

}

