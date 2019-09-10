using UnityEngine;

public static class TransformExtensions {

    /// <summary>
    /// Finds a named child or grandchild of a Transform.
    /// </summary>
    /// <param name="aParent"></param>
    /// <param name="aName"></param>
    /// <returns></returns>
    public static Transform FindDeepChild(this Transform aParent, string aName)
    {
        //CHECK SAME OBJECT FIRST
        if (aParent.name.ToLower().Equals(aName.ToLower()))
            return aParent;
        //THEN CHECK ALL CHILDRENS
        var result = aParent.Find(aName);
        if (result != null)
            return result;
        foreach (Transform child in aParent)
        {
            result = child.FindDeepChild(aName);
            if (result != null)
                return result;
        }
        return null;
    }

    

    /// <summary>
    /// Gets a component in a children with name == name parameter
    /// </summary>
    /// <typeparam name="T"></typeparam>
    /// <param name="t">Root transform</param>
    /// <param name="name">Child Name</param>
    /// <returns>Component</returns>
    public static T GetComponentByName<T>(this Transform t, string name) where T : Component
    {
        T[] components = t.GetComponentsInChildren<T>(true);
        for (int i = 0; i < components.Length; i++)
        {
            if (components[i].name == name)
                return components[i];
        }
        return (T)((object)null);
    }

    /// <summary>
    /// Apply matrix to transform 
    /// </summary>
    /// <param name="transform">Root transform</param>
    /// <param name="matrix">Matrix to apply</param>
    public static void FromMatrix(this Transform transform, Matrix4x4 matrix)
    {
        transform.localScale = matrix.ExtractScale();
        transform.rotation = matrix.ExtractRotation();
        transform.position = matrix.ExtractPosition();
    }

}
