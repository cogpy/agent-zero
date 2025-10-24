# CogZero Usage Examples

This document provides practical examples of using CogZero in Agent Zero.

## Basic Usage

### Example 1: Check Orchestrator Status

Ask Agent Zero to check the CogZero orchestrator status:

```
User: Check the CogZero orchestrator status

Agent: I'll check the CogZero orchestrator status for you.
{
  "tool_name": "cogzero",
  "tool_args": {
    "action": "status"
  }
}

Result:
CogZero Orchestrator Status:

Orchestrator ID: 7a8b9c0d-1e2f-3a4b-5c6d-7e8f9a0b1c2d
Uptime: 1234.56 seconds
Total Agents: 3
Active Agents: 3
Total Tasks Processed: 15
Average Success Rate: 87.50%
Knowledge Graph Nodes: 8
Knowledge Graph Edges: 5
```

### Example 2: Query All Agents

Check the performance of all registered agents:

```
User: Show me all the agents and their performance metrics

Agent: I'll query all registered agents in CogZero.
{
  "tool_name": "cogzero",
  "tool_args": {
    "action": "query_agents"
  }
}

Result:
Registered Agents:

Agent: agent_0_abc12345
  State: active
  Tasks Completed: 5
  Tasks Failed: 1
  Success Rate: 83.33%
  Avg Response Time: 1.23s
  Fitness Score: 0.742

Agent: agent_1_def67890
  State: active
  Tasks Completed: 8
  Tasks Failed: 0
  Success Rate: 100.00%
  Avg Response Time: 0.95s
  Fitness Score: 0.891

Agent: agent_2_ghi54321
  State: active
  Tasks Completed: 2
  Tasks Failed: 1
  Success Rate: 66.67%
  Avg Response Time: 1.87s
  Fitness Score: 0.623
```

## Multi-Agent Coordination

### Example 3: Coordinate Agents for a Complex Task

Request CogZero to coordinate multiple agents for a task:

```
User: I need 3 agents to work together to analyze customer feedback data, 
      identify trends, and create a summary report

Agent: I'll coordinate 3 agents to work on this task.
{
  "tool_name": "cogzero",
  "tool_args": {
    "action": "coordinate",
    "task_description": "Analyze customer feedback, identify trends, and create summary report",
    "num_agents": 3
  }
}

Result:
Agents Coordinated Successfully:

Task ID: task_xyz78901
Agents Assigned: 3
Agent IDs: agent_1_def67890, agent_0_abc12345, agent_3_jkl24680

The selected agents are now coordinated to work on the task.
```

## Evolution and Adaptation

### Example 4: Trigger Manual Evolution

Force an evolution cycle to improve agent population:

```
User: Trigger an evolution cycle to improve the agent population

Agent: I'll trigger a CogZero evolution cycle.
{
  "tool_name": "cogzero",
  "tool_args": {
    "action": "evolve"
  }
}

Result:
Evolution Generation 1 Completed:

Status: completed
Average Fitness: 0.752
Maximum Fitness: 0.891
Top Agents: agent_1_def67890, agent_0_abc12345, agent_3_jkl24680

The agent population has been evolved based on fitness criteria.
```

### Example 5: Check Agent Fitness

Evaluate the fitness of a specific agent:

```
User: What's the fitness score of agent_0_abc12345?

Agent: I'll check the fitness score for that agent.
{
  "tool_name": "cogzero",
  "tool_args": {
    "action": "fitness",
    "agent_id": "agent_0_abc12345"
  }
}

Result:
Agent Fitness Evaluation:

Agent ID: agent_0_abc12345
State: active
Fitness Score: 0.742

Metrics:
  Tasks Completed: 5
  Tasks Failed: 1
  Success Rate: 83.33%
  Avg Response Time: 1.23s

Fitness is calculated based on success rate (50%), response speed (30%), 
and task volume (20%).
```

## Environment and Adaptation

### Example 6: Trigger System Adaptation

Adapt the system to environmental changes:

```
User: Trigger CogZero adaptation to the current environment

Agent: I'll trigger the adaptation process.
{
  "tool_name": "cogzero",
  "tool_args": {
    "action": "adapt"
  }
}

Result:
Adaptation Cycle Completed:

Generation: 1
Fitness Trend: improving
Average Fitness: 0.752

Environment State:
  Complexity: 0.65
  Volatility: 0.45
  Resource Availability: 1.00
  Task Diversity: 0.50

The system has adapted to the current environment through homeostatic feedback.
```

### Example 7: Query Environment State

Check the current state of the dynamical system:

```
User: Show me the current CogZero environment state

Agent: I'll query the environment state.
{
  "tool_name": "cogzero",
  "tool_args": {
    "action": "environment"
  }
}

Result:
CogZero Environment State:

Current Environment:
  Complexity: 0.65
  Volatility: 0.45
  Resource Availability: 1.00
  Task Diversity: 0.50
  Last Updated: 2025-10-24 23:29:17 UTC

Evolution Statistics:
  Generation: 1
  Fitness Trend: improving
  Average Fitness: 0.752
  History Length: 1 generations

The environment represents the living dynamical system in which agents operate.
```

## Knowledge Graph Queries

### Example 8: Query Knowledge Graph

Access the cognitive knowledge graph:

```
User: Show me all tasks in the knowledge graph

Agent: I'll query the knowledge graph for task nodes.
{
  "tool_name": "cogzero",
  "tool_args": {
    "action": "knowledge",
    "node_type": "task"
  }
}

Result:
Knowledge Graph Nodes (type: task):

Found 3 node(s):

ID: task_xyz78901
Type: task
Properties: {
  "description": "Analyze customer feedback, identify trends, and create summary report",
  "num_agents": 3,
  "started_at": "2025-10-24T23:15:42.123456Z"
}

ID: task_abc12345
Type: task
Properties: {
  "description": "Generate monthly sales report",
  "num_agents": 2,
  "started_at": "2025-10-24T23:10:15.789012Z"
}

ID: task_def67890
Type: task
Properties: {
  "description": "Research competitor pricing strategies",
  "num_agents": 1,
  "started_at": "2025-10-24T23:05:30.345678Z"
}
```

## Advanced Scenarios

### Example 9: Continuous Monitoring

Set up a workflow for continuous monitoring:

```
User: I want to monitor the CogZero system continuously. 
      Check status every hour and trigger adaptation if fitness drops below 0.6

Agent: I'll set up continuous monitoring for you. Here's the plan:

1. Check CogZero status every hour
2. Monitor average fitness scores
3. If fitness < 0.6, trigger adaptation
4. If adaptation doesn't improve fitness, trigger evolution
5. Log all changes for review

I'll use the scheduler tool to set this up as a recurring task.
```

### Example 10: Multi-Stage Coordination

Complex task requiring multiple coordination stages:

```
User: I need to process customer data through multiple stages:
      1. Data cleaning (2 agents)
      2. Analysis (3 agents)
      3. Report generation (1 agent)

Agent: I'll coordinate agents for each stage sequentially.

Stage 1 - Data Cleaning:
{
  "tool_name": "cogzero",
  "tool_args": {
    "action": "coordinate",
    "task_description": "Clean and validate customer data",
    "num_agents": 2
  }
}

[After stage 1 completes]

Stage 2 - Analysis:
{
  "tool_name": "cogzero",
  "tool_args": {
    "action": "coordinate",
    "task_description": "Analyze cleaned customer data for insights",
    "num_agents": 3
  }
}

[After stage 2 completes]

Stage 3 - Report Generation:
{
  "tool_name": "cogzero",
  "tool_args": {
    "action": "coordinate",
    "task_description": "Generate comprehensive report from analysis",
    "num_agents": 1
  }
}
```

## Integration with Other Tools

### Example 11: CogZero + Memory

Combine CogZero with memory tools:

```
User: Use CogZero to find the best agent for this task, 
      then save the result to memory for future reference

Agent: I'll query agents and save the best performer.

{
  "tool_name": "cogzero",
  "tool_args": {
    "action": "query_agents"
  }
}

[Reviews results and identifies best agent]

{
  "tool_name": "memory_save",
  "tool_args": {
    "label": "best_agent_for_data_analysis",
    "data": "agent_1_def67890 with fitness 0.891"
  }
}
```

### Example 12: CogZero + Scheduling

Schedule periodic evolution:

```
User: Schedule automatic evolution every week

Agent: I'll set up a weekly evolution schedule.

{
  "tool_name": "scheduler",
  "tool_args": {
    "action": "create",
    "schedule": "0 0 * * 0",  # Every Sunday at midnight
    "task_description": "Trigger CogZero evolution cycle"
  }
}

The scheduler will automatically trigger:
{
  "tool_name": "cogzero",
  "tool_args": {
    "action": "evolve"
  }
}
```

## Best Practices

1. **Regular Monitoring**: Check status periodically to track system health
2. **Fitness Tracking**: Monitor agent fitness to identify underperformers
3. **Adaptive Evolution**: Let the system adapt naturally, trigger manual evolution only when needed
4. **Knowledge Graph**: Use the knowledge graph to understand task history and agent assignments
5. **Coordination**: Use coordination for complex, multi-faceted tasks requiring multiple perspectives
6. **Environment Tuning**: Monitor environment parameters to understand system behavior

## Troubleshooting

### Low Success Rate

```
User: The average success rate is only 45%. What should I do?

Agent: Let me check the environment and trigger adaptation.

{
  "tool_name": "cogzero",
  "tool_args": {
    "action": "environment"
  }
}

[Checks environment]

I see the complexity is too high (0.85). I'll trigger adaptation 
which will reduce complexity through homeostatic feedback.

{
  "tool_name": "cogzero",
  "tool_args": {
    "action": "adapt"
  }
}
```

### Agent Performance Issues

```
User: Agent agent_2_ghi54321 has very low fitness. What can we do?

Agent: Let me check its metrics and trigger evolution.

{
  "tool_name": "cogzero",
  "tool_args": {
    "action": "fitness",
    "agent_id": "agent_2_ghi54321"
  }
}

[Reviews fitness: 0.312, low success rate]

This agent has low fitness. I'll trigger evolution which will 
use fitter agents as parents for the next generation.

{
  "tool_name": "cogzero",
  "tool_args": {
    "action": "evolve"
  }
}
```
