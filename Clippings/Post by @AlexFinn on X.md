You NEED to be building loops with Grok Bot. They’re incredible

It feels like Grok Bot was purpose built for looping more than any other agent

All you do is tell your main agent to tell another agent to loop on a task every 5 minutes, and monitor it while it goes

This is way better than /loop because you now have a bot with specialized tools/skill monitoring another bot with specialized tools/skills rather than a bot monitoring itself which is typically how /loop works

And because you have that separate bot orchestrating the whole thing, you can use intelligence to improve the loop while it works towards its goal

For instance, I’ve had a bot looping on building a project the last 24 hours. My main orchestrator agent is watching the engineer agent. I asked the orchestrator agent to reflect every 30 minutes on the work the engineer is doing, and figure out 1 way to improve the work that is going on to get us closer to the goal

Now the whole loop is autonomously self improving

You can’t do this with /loop in other agents, because it’s just a bot monitoring itself, which will never render good self improvement results. You need a separate bot with different context and perspectives making that judgement

Super easy to set up. Just make sure you have your main orchestrator bot, then another specialized bot that has tools/context that match your objective.

For instance, if you are going to loop on an engineering project, just make sure the specialized agent has good engineering best practices in its description

Then go to your orchestrator and say ‘talk to \*your other bot\* and have them loop every 5 minutes on this task. Make sure they stay on target. Every 30 minutes please review their work and come up with a way to improve the process’

If you can’t think of anything to loop on, try these use cases:

1\. Engineering loop to build a cool 3D game  
2\. Research loop to put together a detailed report  
3\. Social media loop to find breaking news the moment it happens and take action on it  
4\. Local AI loop that loads up and benchmarks different local models on your hardware

Really really powerful use case