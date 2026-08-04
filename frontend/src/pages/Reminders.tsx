import { useEffect, useState } from "react";

import {
  createReminder,
  getReminders,
  type Reminder,
} from "../api/reminders";

import {
  getAppointments,
  type Appointment,
} from "../api/appointments";

export default function Reminders() {
  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [appointments, setAppointments] = useState<Appointment[]>([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [title, setTitle] = useState("");
  const [remindAt, setRemindAt] = useState("");
  const [notificationChannel, setNotificationChannel] =
    useState("dashboard");

  const [appointmentId, setAppointmentId] = useState("");

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    try {
      setLoading(true);

      const [remindersData, appointmentsData] =
        await Promise.all([
          getReminders(),
          getAppointments(),
        ]);

      setReminders(remindersData);
      setAppointments(appointmentsData);
      setError("");
    } catch (err) {
      console.error(err);
      setError("Failed to load reminders or appointments.");
    } finally {
      setLoading(false);
    }
  }

  async function handleCreateReminder(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    if (!title.trim()) {
      setError("Reminder title is required.");
      return;
    }

    if (!remindAt) {
      setError("Reminder date and time are required.");
      return;
    }

    if (!appointmentId) {
      setError("Please select an appointment.");
      return;
    }

    try {
      const newReminder = await createReminder(
        Number(appointmentId),
        {
          title: title.trim(),
          remind_at: new Date(remindAt).toISOString(),
          notification_channel: notificationChannel,
        }
      );

      setReminders((currentReminders) => [
        ...currentReminders,
        newReminder,
      ]);

      setTitle("");
      setRemindAt("");
      setNotificationChannel("dashboard");
      setAppointmentId("");
      setError("");
    } catch (err) {
      console.error(err);
      setError("Failed to create reminder.");
    }
  }

  if (loading) {
    return <div>Loading reminders...</div>;
  }

  return (
    <div>
      <h2>Reminders</h2>

      {error && <p>{error}</p>}

      <form onSubmit={handleCreateReminder}>
        <div>
          <label htmlFor="reminder-title">
            Title
          </label>

          <input
            id="reminder-title"
            type="text"
            value={title}
            onChange={(event) =>
              setTitle(event.target.value)
            }
            placeholder="Reminder title"
          />
        </div>

        <div>
          <label htmlFor="reminder-appointment">
            Appointment
          </label>

          <select
            id="reminder-appointment"
            value={appointmentId}
            onChange={(event) =>
              setAppointmentId(event.target.value)
            }
          >
            <option value="">
              Select an appointment
            </option>

            {appointments.map((appointment) => (
              <option
                key={appointment.id}
                value={appointment.id}
              >
                {appointment.title} —{" "}
                {new Date(
                  appointment.start_at
                ).toLocaleString()}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="reminder-time">
            Remind At
          </label>

          <input
            id="reminder-time"
            type="datetime-local"
            value={remindAt}
            onChange={(event) =>
              setRemindAt(event.target.value)
            }
          />
        </div>

        <div>
          <label htmlFor="notification-channel">
            Notification Channel
          </label>

          <select
            id="notification-channel"
            value={notificationChannel}
            onChange={(event) =>
              setNotificationChannel(event.target.value)
            }
          >
            <option value="dashboard">
              Dashboard
            </option>

            <option value="email">
              Email
            </option>

            <option value="whatsapp">
              WhatsApp
            </option>
          </select>
        </div>

        <button type="submit">
          Create Reminder
        </button>
      </form>

      <hr />

      {reminders.length === 0 ? (
        <p>No reminders found.</p>
      ) : (
        <div>
          {reminders.map((reminder) => (
            <div key={reminder.id}>
              <h3>{reminder.title}</h3>

              <p>
                Remind At:{" "}
                {new Date(
                  reminder.remind_at
                ).toLocaleString()}
              </p>

              <p>
                Channel:{" "}
                {reminder.notification_channel}
              </p>

              <p>
                Status: {reminder.status}
              </p>

              {reminder.sent_at && (
                <p>
                  Sent At:{" "}
                  {new Date(
                    reminder.sent_at
                  ).toLocaleString()}
                </p>
              )}

              <hr />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}