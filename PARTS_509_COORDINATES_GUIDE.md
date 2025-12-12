# Guide: Extracting Parts' 509-Vertex Graph Coordinates

**Status**: Coordinates are NOT publicly available as a standalone download file.
**Last Updated**: 2025-12-12

## Summary of Search Results

I conducted an exhaustive search for the actual vertex coordinates of Jaan Parts' 509-vertex 5-chromatic unit distance graph. Here's what I found:

### Available Resources

1. **Wolfram Language**: The graph is implemented as `GraphData["PartsGraph509"]`
   - Accessible if you have Mathematica or Wolfram Cloud access
   - Can extract coordinates using `GraphEmbedding[]` or `VertexCoordinates`

2. **arXiv Papers**:
   - **arXiv:2010.12665** - "Graph minimization, focusing on the example of 5-chromatic unit-distance graphs in the plane" by Jaan Parts
   - **arXiv:2106.11824** - "Constructing 5-chromatic unit distance graphs embedded in the Euclidean plane" by Voronov et al. (references Parts' work)

3. **Geombinatorics Journal**:
   - Parts, J. (2020). "Graph Minimization, Focusing on the Example of 5-chromatic Unit-Distance Graphs in the Plane." Geombinatorics 29(4), 137-166.

4. **GitHub Repositories**:
   - **simon-tiger/Hadwiger-Nelson-Project-Data**: Contains 517-vertex graph (not 509)
     - Files: 517.csv (edge list, NOT coordinates), 517.edge, 517.tgf
   - **vsvor/dist-graphs**: Contains Wolfram notebooks for spherical constructions

5. **Polymath16 Project**:
   - Blog threads mention vertex files were shared via Dropbox
   - Some files may have been deleted
   - Comments sections may contain download links (sites returned 403 errors when I tried to access)

### What I DID NOT Find

- ❌ No standalone `509.csv` or `509.txt` file with coordinates
- ❌ No public Google Drive or Dropbox link with the data
- ❌ No ancillary files attached to the arXiv papers
- ❌ No supplementary materials from Geombinatorics journal

## How to Get the Coordinates

### Method 1: Wolfram Language (Recommended)

If you have access to Mathematica, Wolfram Cloud, or Wolfram Programming Lab:

```mathematica
(* Load the graph *)
g = GraphData["PartsGraph509"]

(* Extract vertex coordinates *)
coords = GraphEmbedding[g, "UnitDistance"]

(* Export to CSV *)
Export["parts509_coordinates.csv", coords, "CSV"]

(* Alternative: Get as vertex coordinate rules *)
coordRules = GraphData["PartsGraph509", "VertexCoordinates"]

(* Export edges *)
edges = EdgeList[g]
Export["parts509_edges.txt", edges, "Table"]

(* Get basic info *)
VertexCount[g]  (* Should return 509 *)
EdgeCount[g]    (* Should return 2442 *)
```

**Free access**: Wolfram Cloud has a free tier at https://www.wolframcloud.com/

### Method 2: Contact the Author

**Jaan Parts**:
- No personal homepage found
- Contact info may be in the arXiv papers: https://arxiv.org/abs/2010.12665
- Contributed to Polymath16 discussions (username/email may be in blog comments)

### Method 3: Download arXiv Source Files

1. Go to https://arxiv.org/abs/2010.12665
2. Click "Other formats" or "Download source"
3. Extract the .tar.gz file
4. Check for any ancillary files (anc/ directory)
5. Check LaTeX source for embedded coordinates

**Note**: My search didn't find evidence of ancillary files, but worth checking directly.

### Method 4: Polymath16 Blog Archives

Check these threads (may need to bypass 403 errors):
- https://dustingmixon.wordpress.com/2019/03/23/polymath16-twelfth-thread-year-in-review-and-future-plans/#comment-23713
- https://dustingmixon.wordpress.com/2019/08/05/polymath16-fourteenth-thread-automated-graph-minimization/#comment-23814

Look for Dropbox/Google Drive links in the comments.

### Method 5: Reconstruct from Paper

The paper describes the construction methodology. In theory, you could:
1. Implement Parts' graph minimization algorithm
2. Start with Heule's 517-vertex graph (available on GitHub)
3. Apply the minimization procedure

**Difficulty**: High - requires deep understanding of the construction.

## Related Graphs with Available Data

### 517-Vertex Graph (GitHub)

**Repository**: https://github.com/simon-tiger/Hadwiger-Nelson-Project-Data

**Files**:
- `517.csv` - Edge list (vertex adjacencies, NOT coordinates)
- `517.edge` - Edge list format
- `517.tgf` - Trivial Graph Format

**To download**:
```bash
git clone https://github.com/simon-tiger/Hadwiger-Nelson-Project-Data.git
cd Hadwiger-Nelson-Project-Data
cat 517.csv
```

**Note**: This file contains adjacency information, not (x,y) coordinates. To get coordinates, you'd need to:
1. Use a graph layout algorithm (force-directed, etc.)
2. Or find the original unit-distance embedding

### Heule's Graphs

**Wolfram Language**:
```mathematica
GraphData["HeuleGraph510"]  (* 510 vertices *)
GraphData["HeuleGraph517"]  (* 517 vertices *)
GraphData["HeuleGraph529"]  (* 529 vertices *)
GraphData["HeuleGraph553"]  (* 553 vertices *)
```

### de Grey's Original Graph

**Wolfram Language**:
```mathematica
GraphData["deGreyGraph"]  (* 1581 vertices *)
```

## Key Facts About the 509-Vertex Graph

- **Vertices**: 509
- **Edges**: 2,442
- **Chromatic number**: 5 (not 4-colorable, is 5-colorable)
- **Author**: Jaan Parts (2020)
- **Method**: Graph minimization algorithm preserving non-4-colorability
- **Construction**: Based on Moser spindle motifs
- **Record**: Smallest known 5-chromatic unit-distance graph (as of 2022)

## Verification

Once you obtain the coordinates, verify:

```python
import numpy as np
from scipy.spatial.distance import pdist, squareform

# Load coordinates
coords = np.loadtxt('parts509_coordinates.csv', delimiter=',')

# Compute all pairwise distances
distances = squareform(pdist(coords))

# Find edges (distance = 1, within tolerance)
tolerance = 1e-6
edges = np.argwhere((distances > 1 - tolerance) & (distances < 1 + tolerance))

# Should have 2442 edges (counting each edge once)
num_edges = len(edges) // 2  # Divide by 2 since each edge appears twice
print(f"Number of edges: {num_edges}")  # Should be 2442
```

## Next Steps

1. **Try Wolfram Cloud** (free tier): https://www.wolframcloud.com/
   - Sign up for free account
   - Create a notebook
   - Run the Mathematica code above

2. **Check arXiv source files**: Download the source and inspect for data

3. **Contact Jaan Parts**: Ask directly for the coordinate file

4. **Use the 517-vertex graph**: It's close to 509 and has available edge data

## Sources

- [arXiv:2010.12665 - Parts (2020)](https://arxiv.org/abs/2010.12665)
- [arXiv:2106.11824 - Voronov et al. (2021)](https://arxiv.org/abs/2106.11824)
- [Parts Graphs - Wolfram MathWorld](https://mathworld.wolfram.com/PartsGraphs.html)
- [simon-tiger/Hadwiger-Nelson-Project-Data](https://github.com/simon-tiger/Hadwiger-Nelson-Project-Data)
- [Polymath16 Blog](https://dustingmixon.wordpress.com/category/polymath/)

## Conclusion

**The actual coordinates are NOT available as a public download file.** Your best option is:

1. **Use Wolfram Cloud** (free) to extract from `GraphData["PartsGraph509"]`
2. **Or**: Contact Jaan Parts directly
3. **Or**: Use the closely-related 517-vertex Heule graph instead
