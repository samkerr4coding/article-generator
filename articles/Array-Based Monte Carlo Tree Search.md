# Array-Based Monte Carlo Tree Search

This document details a novel approach to Monte Carlo Tree Search (MCTS) that utilizes array-based node organization for enhanced efficiency and scalability. The core innovation lies in separating action and state nodes into distinct arrays, coupled with a hierarchical structure that leverages the inherent ordering of actions. This method significantly improves performance, particularly in scenarios involving continuous dynamical systems and unbounded noise.

## Overview

The proposed algorithm organizes the search tree by layering nodes within arrays. Action and state nodes are stored in separate arrays, allowing for efficient access and reduced memory footprint. This structure is visualized in Figure 4 for the initial iterations of a search over a simple three-action, three-state system. The nodes within each layer are ordered chronologically based on their creation time, with children from different parent nodes intermixed. This contrasts with traditional MCTS implementations that often store all state and action nodes within a single, monolithic array.

## Data Structure and Organization

The fundamental data structure is comprised of multiple arrays, each representing a layer of the search tree.  Each layer’s array is indexed by depth, and within each layer, action nodes and state nodes are stored in parallel.  The key advantage is the inherent ordering of actions, which allows for predictable node expansion.

*   **Depth and `curStateIdx`:** These variables represent the current position within the tree search. `depth` indicates the current search layer, and `curStateIdx` represents the index of the current state within that layer.
*   **`actionValues`, `actionVisits`, `stateVisits`:** These global arrays track the values and visit counts for each action and state, respectively.
*   **`numActionsAtDepth`, `childActionNodes`:** These arrays store the number of actions available at each depth and the indices of the child action nodes, respectively.
*   **`stateNodes` and `childStateNodes`:** These are the core arrays, holding all state nodes and their child state nodes, respectively.

The size of each array increases with depth. At depth 1, all three possible actions from the root node are fully explored.  Four additional state nodes are added to the first layer, totaling nine, three for each of the three actions. These state nodes, in turn, can have three children, and so on. This hierarchical structure, motivated by the bounded branching of actions, significantly reduces memory usage and improves cache locality.

## Action Node Selection

The selection of the next action is governed by Algorithm 2. Given the current `depth` and `curActionIdx`, the algorithm retrieves the indices of the child action nodes (i.e., the column in `childActionNodes` corresponding to the selected action).

1.  **Unvisited Child Check:** The algorithm checks if any unvisited child actions exist using the `untriedAction` flag.
2.  **Sampling:** If unvisited actions are found (`untriedAction` is true), a random untried action is selected.
3.  **Best UCT Action:** If no unvisited actions exist, the action with the highest UCT value is chosen.

## State Node Selection

The selection of the next state node is handled by Algorithm 3, which addresses the complexities introduced by the unordered nature of state nodes.

1.  **`childStateNodes` Array:** This array stores the child state nodes for each state node.
2.  **Assumed Branching (`N_{S,l}`):**  The algorithm assumes a maximum level of state branching (`N_{S,l}`) at each layer (`l`). This value represents the maximum number of child states that can be generated from a given state.
3.  **Initializations:** The `childStateNodes` array is populated with entries initialized to a flag value, indicating that no child state has yet been tried.
4.  **Retrieval:** The algorithm retrieves the first `N_{S,l}` child state indices from the column corresponding to the current action node. Any unassigned state is initialized to point to the last possible state in the layer, set to `NaN` to avoid matching issues.
5.  **Match Index Determination:** The algorithm attempts to find the child state that best matches the generated state. The `matchIdx` is determined by the index of the state within the `childStateNodes` array that has the maximum number of matching dimensions. The `matchFlag` is set to true only if all dimensions of the generated state match the corresponding dimensions of the child state.
6.  **Indexing and Updates:** The algorithm then updates the `childStateNodes` array and the `stateNodes` array based on the `matchFlag`. `nextStateIdx` is calculated, and the number of state nodes in the layer and the current column of the `childStateNodes` array are incremented.
7. **Algorithm 3 - Predictable Child State Selection**
    1. `childStateIdxs = childStateNodes ( depth ).column( curActionIdx ) ;` retrieves the indices of the child state nodes
    2. `childStates = stateNodes ( depth )[ childStateIdxs ] ;` retrieves the child state nodes
    3. for i = 1 ​ … ​ N S , l i=1\ldots N_{S,l} do 4  `stateMatches [i] = Σ \Sigma ( childStates [i] == generatedState ) ;` calculates the number of matching dimensions
    5  `int8 matchIdx = maxIndex( stateMatches ) ;` finds the index with the most matches
    6  `bool matchFlag = stateMatches [ matchIdx ] == size( generatedState ) ;` checks if all dimensions match
    7  `int8 idxInChildArray = matchIdx * matchFlag + childStateNodes ( depth )[ N S , l N_{S,l} , curActionIdx ] * ! untriedAction ;` calculates the index in the child array
    8  `int8 nextStateIdx = childStateNodes ( depth )[ matchIdx , curStateIdx ] * matchFlag + numStatesAtDepth ( depth ) * ! matchFlag ;` calculates the next state index
    9  `childStateNodes ( depth )[ nextStateIdx , curActionIdx ] = nextStateIdx ;` updates the child state nodes
    10  `stateNodes ( depth )[ nextStateIdx ] = generatedState ;` sets the new state node
    11  `childStateNodes ( depth )[ N S , l N_{S,l} , curActionIdx ] += ! matchFlag ;` increments the count of child state nodes
    12  `numStatesAtDepth ( depth ) += ! matchFlag ;` increments the count of states at the current depth
    13 return `nextStateIdx ;`

## Conclusion

The array-based approach to MCTS offers significant advantages in terms of efficiency, memory usage, and scalability, particularly when dealing with continuous dynamical systems and unbounded noise. By carefully organizing the search tree and leveraging the inherent ordering of actions, this method provides a robust and performant solution for complex decision-making problems.
Url:https://arxiv.org/html/2508.20140v1