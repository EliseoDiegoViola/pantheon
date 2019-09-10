using UnityEngine;
using UnityEditor;
using System.Collections.Generic;
using System.Linq;
using System;
public static class ExtensionToolsMethodsEditor{

	public static void ChangeStaticStateRecursively(this GameObject go, bool value)
	{
		go.isStatic = value;
		foreach (Transform child in go.transform)
		{
			child.gameObject.ChangeStaticStateRecursively(value);
		}
	}

	public static void ChangeStaticStateRecursively(this GameObject go, StaticEditorFlags value)
	{
		GameObjectUtility.SetStaticEditorFlags(go, value);
		foreach (Transform child in go.transform)
		{
			child.gameObject.ChangeStaticStateRecursively(value);
		}
	}

	public static void ChangeNavMeshLayerRecursively(this GameObject go, int value)
	{
		GameObjectUtility.SetNavMeshArea(go, value);
		foreach (Transform child in go.transform)
		{
			child.gameObject.ChangeNavMeshLayerRecursively(value);
		}
	}
}
