class IterativeEngine:
    def __init__(self) -> None:
        pass

    async def initial_planning(self):
        """
        Goal of initial_planning phase is to create tasks for specific agents given goal and summary of previous step.
        During this phase agents with role=manager plan tasks
        """
        pass

    async def tasks_decomposition(self):
        """
        Goal of tasks_decomposition phase is to create execution plan for each task in form of list of actions with dependencies.
        During this phase agents for each tasks
        - Retrieve and summarize related information using search
        - Add it to the task
        - Decompose task to smaller tasks for developer workers
        """
        pass

    async def tasks_execution(self):
        """
        Goal of tasks_execution phase is to execute task on specific agents. During this phase code will be written and commit to git repos
        """
        pass

    async def iteration_review(self):
        """
        Goal of iteration_review phase is to create summary of current iteration to provide text report that should consists of
        - comparison between current result and target result
        - summary of received errors
        """
        pass
