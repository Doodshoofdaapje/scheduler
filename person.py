class Person:

    def __init__(self, name, preferences):
        self._name = name
        self._preferences = preferences
        self._assigned_tasks = []
        self._unlucky_count = 0

    @property
    def name(self):
        return self._name
    
    @property
    def preferences(self):
        return self._preferences
    
    @property
    def unlucky_count(self):
        return self._unlucky_count

    def print(self):
        print(self._name + " has preferences ")
        print(self._preferences)

    def assign_task(self, task):
        self._assigned_tasks.append(task)
        if task not in self._preferences:
            print(self._name + " got unlucky with " + task)
            self._unlucky_count += 1
            return 1
        self._preferences.remove(task)
        return 0

    def print_assignment(self):
        tasks_as_string = " ".join(self._assigned_tasks)
        print(self._name + " has shifts: " + tasks_as_string)
