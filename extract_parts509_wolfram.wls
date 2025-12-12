#!/usr/bin/env wolframscript
(* Extract Parts' 509-vertex graph coordinates from Wolfram GraphData *)
(* Usage: wolframscript -script extract_parts509_wolfram.wls *)

Print["Loading Parts' 509-vertex 5-chromatic graph..."]

(* Load the graph *)
g = GraphData["PartsGraph509"];

If[Head[g] === GraphData,
  Print["ERROR: GraphData[\"PartsGraph509\"] not found in your Wolfram installation."];
  Print["This data may require an updated version of Mathematica or Wolfram Language."];
  Exit[1]
];

Print["Loaded successfully!"]
Print["Vertices: ", VertexCount[g]]
Print["Edges: ", EdgeCount[g]]

(* Extract coordinates with unit distance embedding *)
Print["\nExtracting vertex coordinates..."]
coords = GraphEmbedding[g, "UnitDistance"];

(* If UnitDistance doesn't work, try other embeddings *)
If[coords === $Failed || coords === {},
  Print["UnitDistance embedding failed, trying default embedding..."];
  coords = GraphEmbedding[g];
];

(* Export coordinates as CSV *)
Print["Exporting to parts509_coordinates.csv..."]
Export["parts509_coordinates.csv", coords, "CSV"];

(* Also export as table with vertex indices *)
coordsWithIndices = Table[{i, coords[[i, 1]], coords[[i, 2]]}, {i, 1, Length[coords]}];
Export["parts509_coordinates_indexed.csv", coordsWithIndices, "CSV"];

(* Export edge list *)
Print["Exporting edge list..."]
edges = EdgeList[g];
edgeData = Table[{EdgeList[g][[i, 1]], EdgeList[g][[i, 2]]}, {i, 1, Length[edges]}];
Export["parts509_edges.csv", edgeData, "CSV"];

(* Export adjacency matrix *)
Print["Exporting adjacency matrix..."]
adj = AdjacencyMatrix[g];
Export["parts509_adjacency.csv", Normal[adj], "CSV"];

(* Verify unit distances *)
Print["\nVerifying unit distances..."]
numVertices = Length[coords];
unitEdges = 0;
For[i = 1, i <= Length[edges], i++,
  edge = edges[[i]];
  v1 = VertexIndex[g, edge[[1]]];
  v2 = VertexIndex[g, edge[[2]]];
  dist = EuclideanDistance[coords[[v1]], coords[[v2]]];
  If[Abs[dist - 1.0] > 0.001,
    Print["WARNING: Edge ", edge, " has distance ", dist, " (not unit distance)"]
  ,
    unitEdges++
  ];
];
Print["Unit distance edges verified: ", unitEdges, " / ", Length[edges]]

(* Export graph visualization *)
Print["\nGenerating visualization..."]
viz = Graph[g, VertexCoordinates -> coords,
  GraphLayout -> None,
  ImageSize -> 1200,
  VertexSize -> 0.5,
  VertexStyle -> Blue,
  EdgeStyle -> Gray
];
Export["parts509_graph.pdf", viz];
Export["parts509_graph.png", viz, ImageResolution -> 300];

(* Export summary statistics *)
Print["\nGraph Statistics:"]
Print["  Vertices: ", VertexCount[g]]
Print["  Edges: ", EdgeCount[g]]
Print["  Chromatic Number: ", ChromaticNumber[g]]
Print["  Graph Diameter: ", GraphDiameter[g]]
Print["  Average Degree: ", N[2.0 * EdgeCount[g] / VertexCount[g]]]

Print["\n=== Export Complete ==="]
Print["Files created:"]
Print["  - parts509_coordinates.csv (x,y coordinates)"]
Print["  - parts509_coordinates_indexed.csv (vertex_id, x, y)"]
Print["  - parts509_edges.csv (edge list)"]
Print["  - parts509_adjacency.csv (adjacency matrix)"]
Print["  - parts509_graph.pdf (visualization)"]
Print["  - parts509_graph.png (visualization)"]
