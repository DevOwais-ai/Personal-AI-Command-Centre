import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { getCurrentUser } from "../api/auth";
import { getInboxStats } from "../api/inbox";
import { getTasks, type Task } from "../api/tasks";
import {
  getAppointments,
  type Appointment,
} from "../api/appointments";
import {
  getReminders,
  type Reminder,
} from "../api/reminders";

import type { User } from "../types/auth";

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null);

  const [inboxStats, setInboxStats] = useState({
    total: 0,
    unread: 0,
    important: 0,
  });

  const [tasks, setTasks] = useState<Task[]>([]);
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [reminders, setReminders] = useState<Reminder[]>([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [
          currentUser,
          stats,
          taskData,
          appointmentData,
          reminderData,
        ] = await Promise.all([
          getCurrentUser(),
          getInboxStats(),
          getTasks(),
          getAppointments(),
          getReminders(),
        ]);

        setUser(currentUser);
        setInboxStats(stats);
        setTasks(taskData);
        setAppointments(appointmentData);
        setReminders(reminderData);
      } catch (err) {
        console.error("Failed to load dashboard:", err);
        setError("Failed to load dashboard data.");
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  if (loading) {
    return <div>Loading dashboard...</div>;
  }

  const pendingTasks = tasks.filter(
    (task) => task.status !== "completed"
  );

  const upcomingAppointments = appointments.filter(
    (appointment) => appointment.status !== "cancelled"
  );

  const pendingReminders = reminders.filter(
    (reminder) => reminder.status === "pending"
  );

  return (
    <div>
      <h2>Dashboard</h2>

      <p>
        Welcome{user?.name ? `, ${user.name}` : ""}.
      </p>

      {error && <p>{error}</p>}

      <div className="dashboard-grid">
        <div className="dashboard-card">
          <h3>Inbox</h3>
          <p>Total: {inboxStats.total}</p>
          <p>Unread: {inboxStats.unread}</p>
          <p>Important: {inboxStats.important}</p>

          <Link to="/inbox">
            Open Inbox
          </Link>
        </div>

        <div className="dashboard-card">
          <h3>Tasks</h3>
          <p>
            Pending tasks: {pendingTasks.length}
          </p>

          <Link to="/tasks">
            Manage Tasks
          </Link>
        </div>

        <div className="dashboard-card">
          <h3>Appointments</h3>
          <p>
            Upcoming: {upcomingAppointments.length}
          </p>

          <Link to="/appointments">
            Manage Appointments
          </Link>
        </div>

        <div className="dashboard-card">
          <h3>Reminders</h3>
          <p>
            Pending: {pendingReminders.length}
          </p>

          <Link to="/reminders">
            View Reminders
          </Link>
        </div>

        <div className="dashboard-card">
          <h3>Conversations</h3>
          <p>
            Manage your conversations.
          </p>

          <Link to="/conversations">
            Open Conversations
          </Link>
        </div>

        <div className="dashboard-card">
          <h3>Contacts</h3>
          <p>
            Manage your contacts.
          </p>

          <Link to="/contacts">
            Open Contacts
          </Link>
        </div>
      </div>
    </div>
  );
}
