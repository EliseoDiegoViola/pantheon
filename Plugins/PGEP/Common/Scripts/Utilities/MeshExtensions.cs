using UnityEngine;

public static class MeshExtensions {
	public static Bounds CalculatBoundsWithMatrix(this Mesh mesh, Matrix4x4 mtx){
			Vector3[] vertices = mesh.vertices;
			Vector3 min, max;
			min = max = mtx.MultiplyPoint(vertices[0]);
			for (int i = 1; i < vertices.Length; i++)
			{
				Vector3 V = mtx.MultiplyPoint(vertices[i]);
				for (int n = 0; n < 3; n++)
				{
					if (V[n] > max[n])
						max[n] = V[n];
					if (V[n] < min[n])
						min[n] = V[n];
				}
			}
			Bounds B = new Bounds();
			B.SetMinMax((min), (max));
			return B;
		}
}
