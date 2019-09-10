using UnityEngine;
using System.Collections.Generic;
using System.Linq;
using System;

public static class ExtensionToolsMethods
{

    public static void ChangeLayersRecursively(this Transform trans, int layer)
    {
        trans.gameObject.layer = layer;
        foreach (Transform child in trans)
        {
            child.ChangeLayersRecursively(layer);
        }
    }

    public static void ChangeLayersRecursively(this Transform trans, string name)
    {
        trans.gameObject.layer = LayerMask.NameToLayer(name);
        foreach (Transform child in trans)
        {
            child.ChangeLayersRecursively(name);
        }
    }

    public static void ChangeComponentValueRecursively<T>(this Transform go, Action<T> change) where T : Component
    {
        T comp = go.GetComponent<T>();
        if (comp != null)
        {
            change(comp);
        }
        foreach (Transform child in go)
        {
            child.ChangeComponentValueRecursively<T>(change);
        }

    }

    

    //public static bool ContainBounds(this Bounds bounds, Bounds target)
    //{
    //    return bounds.Contains(target.min) && bounds.Contains(target.max);
    //}

    //public static float GetContainPercentage(this Bounds bounds, Bounds target)
    //{

    //    if (bounds.Contains(target.min) && bounds.Contains(target.max))
    //    {
    //        return 1;
    //    }
    //    else if (!bounds.Contains(target.min) && !bounds.Contains(target.max))
    //    {
    //        return 0;
    //    }
    //    else if (!bounds.Contains(target.min) && bounds.Contains(target.max))
    //    {
    //        return 0;
    //    }
    //    else if (bounds.Contains(target.min) && !bounds.Contains(target.max))
    //    {
    //        return 0;

    //    }
    //    return -1;
    //}

    //private static bool Inter(this Bounds bounds, Bounds target)
    //{
    //    if ((double)bounds.min.x <= (double)target.max.x && (double)bounds.max.x >= (double)target.min.x && ((double)bounds.min.y <= (double)target.max.y && (double)bounds.max.y >= (double)target.min.y) && (double)bounds.min.z <= (double)target.max.z)
    //        return (double)bounds.max.z >= (double)target.min.z;
    //    return false;
    //}

    public static List<Vector3[]> IntersectsDebug(this Bounds bounds1, Bounds bounds2, Transform transform1, Transform transform2)
    {

        Vector3[] bounds1Points = bounds1.EnumeratePoints().Select<Vector3, Vector3>(p => transform1.localToWorldMatrix.MultiplyPoint(p)).ToArray(); 
        Vector3[] bounds2Points = bounds2.EnumeratePoints().Select<Vector3, Vector3>(p => transform2.localToWorldMatrix.MultiplyPoint(p)).ToArray();
        List<Vector3[]> transformedBounds = new List<Vector3[]>
        {
            bounds1Points,
            bounds2Points
        };
        return transformedBounds;
    }


        public static bool Intersects(this Bounds bounds1, Bounds bounds2, Transform transform1, Transform transform2)
    {

        Vector3[] bounds1Points = bounds1.EnumeratePoints().Select<Vector3,Vector3>(p => transform1.localToWorldMatrix.MultiplyPoint(p)).ToArray(); 
        Vector3[] bounds2Points = bounds2.EnumeratePoints().Select<Vector3, Vector3>(p => transform2.localToWorldMatrix.MultiplyPoint(p)).ToArray();

        Func<Vector3[], Vector3[], bool> isInside = (b1, b2) => //Test a better way to check inner points?
        {

            var u = b1[0] - b1[6];
            var v = b1[0] - b1[2];
            var w = b1[0] - b1[4];

            var toCompU1 = Vector3.Dot(u, b1[0]);
            var toCompU2 = Vector3.Dot(u, b1[6]);

            var toCompV1 = Vector3.Dot(v, b1[0]);
            var toCompV2 = Vector3.Dot(v, b1[2]);

            var toCompW1 = Vector3.Dot(w, b1[0]);
            var toCompW2 = Vector3.Dot(w, b1[4]);

            foreach (var p in b2) {
                var resU = Vector3.Dot(u, p);
                var resV = Vector3.Dot(v, p);
                var resW = Vector3.Dot(w, p);

                bool isu = toCompU1 > resU && resU > toCompU2;
                bool isv = toCompV1 > resV && resV > toCompV2;
                bool isw = toCompW1 > resW && resW > toCompW2;
                if (isu && isv && isw) {
                    return true;
                }
            }

            return false;
        };

        /*Plane[] bounds1Planes = new Plane[] {
            new Plane(bounds1Points[0],bounds1Points[2],bounds1Points[7]),
            new Plane(bounds1Points[2],bounds1Points[5],bounds1Points[1]),
            new Plane(bounds1Points[1],bounds1Points[3],bounds1Points[4]),
            new Plane(bounds1Points[0],bounds1Points[2],bounds1Points[6]),
            new Plane(bounds1Points[3],bounds1Points[4],bounds1Points[6]),
            new Plane(bounds1Points[1],bounds1Points[3],bounds1Points[6])
        };

        Plane[] bounds2Planes = new Plane[] {
            new Plane(bounds2Points[0],bounds2Points[2],bounds2Points[7]),
            new Plane(bounds2Points[2],bounds2Points[5],bounds2Points[1]),
            new Plane(bounds2Points[1],bounds2Points[3],bounds2Points[4]),
            new Plane(bounds2Points[0],bounds2Points[2],bounds2Points[6]),
            new Plane(bounds2Points[3],bounds2Points[4],bounds2Points[6]),
            new Plane(bounds2Points[1],bounds2Points[3],bounds2Points[6])
        };*/

        //if (bounds1.ContainsAny(bounds2Points) || bounds2.ContainsAny(bounds1Points))
        //    return true;

        /*Func<Vector3[], Vector3[], bool> IsInPolygon = (poly, toTest) =>
          {
              foreach (var point in toTest) {
                  var coef = poly.Skip(1).Select((p, i) =>
                                              (point.y - poly[i].y) * (p.x - poly[i].x)
                                            - (point.x - poly[i].x) * (p.y - poly[i].y))
                                      .ToList();

                  if (coef.Any(p => p == 0))
                  {
                      return true;
                  }

                  for (int i = 1; i < coef.Count(); i++)
                  {
                      if (coef[i] * coef[i - 1] < 0)
                          return false;
                  }
              }
              return true;
          };*/
        /*public static bool IsInPolygon(Point[] poly, Point point)
        {
            var coef = poly.Skip(1).Select((p, i) =>
                                            (point.Y - poly[i].Y) * (p.X - poly[i].X)
                                          - (point.X - poly[i].X) * (p.Y - poly[i].Y))
                                    .ToList();

            if (coef.Any(p => p == 0))
                return true;

            for (int i = 1; i < coef.Count(); i++)
            {
                if (coef[i] * coef[i - 1] < 0)
                    return false;
            }
            return true;
        }*/


        /*Func<Vector3, Vector3, Bounds, bool> edgeIntersectsBounds = (point1, point2, bounds) =>
        {
            Ray ray = new Ray(point1, point2 - point1);
            if (!bounds.IntersectRay(ray))
                return false;

            ray.origin = point2;
            ray.direction = -ray.direction;
            return bounds.IntersectRay(ray);
        };

        Func<Vector3[], Bounds, bool> pointsContainIntersectingEdge = (points, bounds) =>
        {
            for (int i = 0; i < points.Length - 1; i++)
                if (points.Skip(i + 1).Any(p => edgeIntersectsBounds(points[i], p, bounds)))
                    return true;

            return false;
        };*/

        //return pointsContainIntersectingEdge(bounds2Points, bounds1) || pointsContainIntersectingEdge(bounds1Points, bounds2);
        return isInside(bounds2Points, bounds1Points) || isInside(bounds1Points, bounds2Points);
    }

    public static bool ContainsAny(this Bounds bounds, IEnumerable<Vector3> points)
    {
        return points.Any(p => bounds.Contains(p));
    }

    public static IEnumerable<Vector3> EnumeratePoints(this Bounds bounds)
    {
        yield return bounds.min;
        yield return bounds.max;
        for (int axis = 0; axis < 3; axis++)
        {
            Vector3 point = bounds.min;
            point[axis] += bounds.size[axis];
            yield return point;

            point = bounds.max;
            point[axis] -= bounds.size[axis];
            yield return point;
        }
    }
    

    
    /// <summary>
    /// from local to world space
    /// </summary>
    public static IEnumerable<Vector3> TransformPoints(this Transform transform, IEnumerable<Vector3> points)
    {
        return points.Select(p => transform.TransformPoint(p));
    }

    /// <summary>
    /// from world to local space
    /// </summary>
    public static IEnumerable<Vector3> InverseTransformPoints(this Transform transform, IEnumerable<Vector3> points)
    {
        return points.Select(p => transform.InverseTransformPoint(p));
    }

    /// <summary>
    /// Puts points from another Transform's local space into this one's.
    /// </summary>
    public static IEnumerable<Vector3> InverseTransformPoints(this Transform transform, IEnumerable<Vector3> points, Transform otherTransform)
    {
        return transform.InverseTransformPoints(otherTransform.TransformPoints(points));
    }
    

}

