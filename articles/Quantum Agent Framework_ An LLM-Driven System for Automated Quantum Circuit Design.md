# Quantum Agent Framework: An LLM-Driven System for Automated Quantum Circuit Design

This research introduces Quantum Agent, a large language model (LLM)-based system designed for autonomous creation of quantum programs using OpenQASM. The system utilizes a Python-based code generator that adapts to varying qubit configurations and incorporates test cases to verify both the structural correctness and functional accuracy of generated quantum circuits. The framework supports both in-context few-shot learning and Retrieval-Augmented Generation (RAG)-based tool invocation, providing flexible learning and execution capabilities. A constraint is imposed on the maximum qubit count, limiting it to twelve, to ensure computational feasibility during simulations.

The system’s performance was evaluated using a curated dataset named QCircuitNet [24], which contains a range of foundational quantum problems expressed through natural language instructions accompanied by mathematical representations in LaTeX.  Specifically, the following problem types were selected for testing:

Complex Multi-Algorithm Challenges: To gauge QAgent’s abilities in handling sophisticated tasks, we developed composite problems that integrate multiple fundamental quantum algorithms.  For example, in the “bg” task, the user poses a question requiring the simultaneous application of both the Bernstein-Vazirani (bv) algorithm and Grover’s algorithm (gr). This composite multi-quantum-algorithm dataset includes problems combining two, three, or four distinct algorithms. The following table details all the multi-algorithm tasks and the algorithms needed to solve them:

• bg: Bernstein-Vazirani, Grover
• pg: Phase Estimation, Grover
• bw: Bernstein-Vazirani, W-state
• pw: Phase Estimation, W-state
• dw: Deutsch-Jozsa, W-state
• bpg: Bernstein-Vazirani, Phase Estimation, Grover
• dgw: Deutsch-Jozsa, Grover, W-state
• bdg: Bernstein-Vazirani, Deutsch-Jozsa, Grover
• pgw: Phase Estimation, Grover, W-state
• bpw: Bernstein-Vazirani, Phase Estimation, W-state
• bdgw: Bernstein-Vazirani, Deutsch-Jozsa, Grover, W-state
• bpgw: Bernstein-Vazirani, Phase Estimation, Grover, W-state
• dpgw: Deutsch-Jozsa, Phase Estimation, Grover, W-state
• bdpw: Bernstein-Vazirani, Deutsch-Jozsa, Phase Estimation, W-state
• bdpg: Bernstein-Vazirani, Deutsch-Jozsa, Phase Estimation, Grover

This dataset provides a controlled yet demanding environment for assessing whether an LLM-driven agent can accurately deduce and systematically break down intricate composite inquiries into the necessary quantum components. By encompassing combinations from two to four algorithms, the dataset progressively increases the level of reasoning required while maintaining clear, interpretable answers for evaluation.  Detailed explanations for each task are available in the associated GitHub repository.

Url:https://arxiv.org/html/2508.20134v1