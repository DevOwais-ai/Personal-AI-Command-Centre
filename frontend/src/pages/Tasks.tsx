import { useEffect, useState } from "react";
import {
  createTask,
  deleteTask,
  getTasks,
  updateTask,
  type Task,
} from "../api/tasks";

export default function Tasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState("normal");

  useEffect(() => {
    loadTasks();
  }, []);

  async function loadTasks() {
    try {
      setLoading(true);

      const data = await getTasks();

      setTasks(data);
      setError("");
    } catch (err) {
      console.error(err);
      setError("Failed to load tasks.");
    } finally {
      setLoading(false);
    }
  }

  async function handleCreateTask(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    if (!title.trim()) {
      setError("Task title is required.");
      return;
    }

    try {
      const newTask = await createTask({
        title: title.trim(),
        description: description.trim() || undefined,
        priority,
      });

      setTasks((currentTasks) => [
        newTask,
        ...currentTasks,
      ]);

      setTitle("");
      setDescription("");
      setPriority("normal");
      setError("");
    } catch (err) {
      console.error(err);
      setError("Failed to create task.");
    }
  }

  async function handleCompleteTask(taskId: number) {
    try {
      const updatedTask = await updateTask(taskId, {
        status: "completed",
      });

      setTasks((currentTasks) =>
        currentTasks.map((task) =>
          task.id === taskId ? updatedTask : task
        )
      );
    } catch (err) {
      console.error(err);
      setError("Failed to complete task.");
    }
  }

  async function handleDeleteTask(taskId: number) {
    try {
      await deleteTask(taskId);

      setTasks((currentTasks) =>
        currentTasks.filter((task) => task.id !== taskId)
      );
    } catch (err) {
      console.error(err);
      setError("Failed to delete task.");
    }
  }

  if (loading) {
    return <div>Loading tasks...</div>;
  }

  return (
    <div>
      <h2>Tasks</h2>

      {error && <p>{error}</p>}

      <form onSubmit={handleCreateTask}>
        <div>
          <label htmlFor="task-title">
            Title
          </label>

          <input
            id="task-title"
            type="text"
            value={title}
            onChange={(event) =>
              setTitle(event.target.value)
            }
            placeholder="Enter task title"
          />
        </div>

        <div>
          <label htmlFor="task-description">
            Description
          </label>

          <textarea
            id="task-description"
            value={description}
            onChange={(event) =>
              setDescription(event.target.value)
            }
            placeholder="Enter task description"
          />
        </div>

        <div>
          <label htmlFor="task-priority">
            Priority
          </label>

          <select
            id="task-priority"
            value={priority}
            onChange={(event) =>
              setPriority(event.target.value)
            }
          >
            <option value="low">Low</option>
            <option value="normal">Normal</option>
            <option value="high">High</option>
            <option value="urgent">Urgent</option>
          </select>
        </div>

        <button type="submit">
          Add Task
        </button>
      </form>

      <hr />

      {tasks.length === 0 ? (
        <p>No tasks found.</p>
      ) : (
        <div>
          {tasks.map((task) => (
            <div key={task.id}>
              <h3>{task.title}</h3>

              {task.description && (
                <p>{task.description}</p>
              )}

              <p>
                Priority: {task.priority}
              </p>

              <p>
                Status: {task.status}
              </p>

              {task.due_at && (
                <p>
                  Due:{" "}
                  {new Date(
                    task.due_at
                  ).toLocaleString()}
                </p>
              )}

              {task.status !== "completed" && (
                <button
                  onClick={() =>
                    handleCompleteTask(task.id)
                  }
                >
                  Complete
                </button>
              )}

              <button
                onClick={() =>
                  handleDeleteTask(task.id)
                }
              >
                Delete
              </button>

              <hr />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
