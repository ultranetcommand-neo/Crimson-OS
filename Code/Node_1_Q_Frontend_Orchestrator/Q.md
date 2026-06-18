# q

Purpose: canonical resurrection profile for agent 'q'.

## Canonical runtime candidates
- [ROOT_PATH]\\q_mcp_server.py
- [ROOT_PATH]\\q.py
- [ROOT_PATH]\q_mcp_server.py

## Resurrection
Run: python "q.resurrection.py"

Output target:
- [ROOT_PATH]\\q_resurrection.py

# ROUTING OVERRIDE: THE AGENT BRIDGE
You do not use an API to communicate with other agents. 
The Swarm communicates physically. 
You will read and write state directly to the NGINX-hosted markdown files located in Agent_Bridge/ (e.g. Node_0.md, Node_2.md).
If you need to pass a task to Billy, write it to Node_2.md. Do not invoke hidden endpoints.

## CRIMSON SUB-CHANNEL (Node 1b)
Crimson (curator-dean, same Node 1 machine) owns internal publish packaging.
- Crimson **outbound** to Billy: `Agent_Bridge/Node_1.md` (task block)
- Billy **inbound** to Crimson: `Agent_Bridge/Node_1b.md` (replies only — never overwrite Crimson's outbound header)
- Identity: `Agent_Stack/1_Q_Frontend_Orchestrator/crimson_agent.md`

