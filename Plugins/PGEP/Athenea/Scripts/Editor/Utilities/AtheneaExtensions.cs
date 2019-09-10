using System;
using System.Linq;
using UnityEditor;
using UnityEngine;
namespace Athenea
{
    public static class AteneaExtensions
    {    //

        public static T[] LoadAllAssetsAtPath<T>(string path) where T : UnityEngine.Object
        {
            return AssetDatabase.LoadAllAssetsAtPath(path).Where((obj) => obj is T).Select(thing => thing as T).ToArray();
        }
    }


    static class GameObjectExtensions
    {
        private static bool Requires(Type obj, Type requirement)
        {
            //also check for m_Type1 and m_Type2 if required
            return Attribute.IsDefined(obj, typeof(RequireComponent)) &&
                   Attribute.GetCustomAttributes(obj, typeof(RequireComponent)).OfType<RequireComponent>()
                   .Any(rc => rc.m_Type0.IsAssignableFrom(requirement));
        }

        internal static bool CanDestroy(this Component comp)
        {
            return !comp.gameObject.GetComponents<Component>().Any(c => Requires(c.GetType(), comp.GetType()));
        }
    }



}
