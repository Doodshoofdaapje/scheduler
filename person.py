class Person:

    def __init__(self, name, preferences):
        self.name = name
        self.preferences = preferences
        self.assigned_tasks = []
        self.unlucky_count = 0

    def print(self):
        print(self.name + " has preferences ")
        print(self.preferences)

    def assign_task(self, task):
        self.assigned_tasks.append(task)
        if task not in self.preferences:
            self.unlucky_count += 1
            return
        self.preferences.remove(task)

    def print_assignment(self):
        tasks_as_string = " ".join(self.assigned_tasks)
        print(self.name + " has shifts: " + tasks_as_string)
