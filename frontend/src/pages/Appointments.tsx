import { useEffect, useState } from "react";
import {
  createAppointment,
  deleteAppointment,
  getAppointments,
  updateAppointment,
  type Appointment,
} from "../api/appointments";

export default function Appointments() {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [startAt, setStartAt] = useState("");
  const [endAt, setEndAt] = useState("");
  const [location, setLocation] = useState("");

  useEffect(() => {
    loadAppointments();
  }, []);

  async function loadAppointments() {
    try {
      setLoading(true);

      const data = await getAppointments();

      setAppointments(data);
      setError("");
    } catch (err) {
      console.error(err);
      setError("Failed to load appointments.");
    } finally {
      setLoading(false);
    }
  }

  async function handleCreateAppointment(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    if (!title.trim()) {
      setError("Appointment title is required.");
      return;
    }

    if (!startAt || !endAt) {
      setError("Start and end times are required.");
      return;
    }

    const start = new Date(startAt);
    const end = new Date(endAt);

    if (end <= start) {
      setError("End time must be after start time.");
      return;
    }

    try {
      const newAppointment = await createAppointment({
        title: title.trim(),
        description: description.trim() || undefined,
        start_at: start.toISOString(),
        end_at: end.toISOString(),
        location: location.trim() || undefined,
      });

      setAppointments((currentAppointments) => [
        ...currentAppointments,
        newAppointment,
      ]);

      setTitle("");
      setDescription("");
      setStartAt("");
      setEndAt("");
      setLocation("");
      setError("");
    } catch (err) {
      console.error(err);
      setError("Failed to create appointment.");
    }
  }

  async function handleCancelAppointment(
    appointmentId: number
  ) {
    try {
      const updatedAppointment = await updateAppointment(
        appointmentId,
        {
          status: "cancelled",
        }
      );

      setAppointments((currentAppointments) =>
        currentAppointments.map((appointment) =>
          appointment.id === appointmentId
            ? updatedAppointment
            : appointment
        )
      );
    } catch (err) {
      console.error(err);
      setError("Failed to cancel appointment.");
    }
  }

  async function handleDeleteAppointment(
    appointmentId: number
  ) {
    try {
      await deleteAppointment(appointmentId);

      setAppointments((currentAppointments) =>
        currentAppointments.filter(
          (appointment) =>
            appointment.id !== appointmentId
        )
      );
    } catch (err) {
      console.error(err);
      setError("Failed to delete appointment.");
    }
  }

  if (loading) {
    return <div>Loading appointments...</div>;
  }

  return (
    <div>
      <h2>Appointments</h2>

      {error && <p>{error}</p>}

      <form onSubmit={handleCreateAppointment}>
        <div>
          <label htmlFor="appointment-title">
            Title
          </label>

          <input
            id="appointment-title"
            type="text"
            value={title}
            onChange={(event) =>
              setTitle(event.target.value)
            }
            placeholder="Appointment title"
          />
        </div>

        <div>
          <label htmlFor="appointment-description">
            Description
          </label>

          <textarea
            id="appointment-description"
            value={description}
            onChange={(event) =>
              setDescription(event.target.value)
            }
            placeholder="Appointment description"
          />
        </div>

        <div>
          <label htmlFor="appointment-start">
            Start
          </label>

          <input
            id="appointment-start"
            type="datetime-local"
            value={startAt}
            onChange={(event) =>
              setStartAt(event.target.value)
            }
          />
        </div>

        <div>
          <label htmlFor="appointment-end">
            End
          </label>

          <input
            id="appointment-end"
            type="datetime-local"
            value={endAt}
            onChange={(event) =>
              setEndAt(event.target.value)
            }
          />
        </div>

        <div>
          <label htmlFor="appointment-location">
            Location
          </label>

          <input
            id="appointment-location"
            type="text"
            value={location}
            onChange={(event) =>
              setLocation(event.target.value)
            }
            placeholder="Location"
          />
        </div>

        <button type="submit">
          Create Appointment
        </button>
      </form>

      <hr />

      {appointments.length === 0 ? (
        <p>No appointments found.</p>
      ) : (
        <div>
          {appointments.map((appointment) => (
            <div key={appointment.id}>
              <h3>{appointment.title}</h3>

              {appointment.description && (
                <p>{appointment.description}</p>
              )}

              <p>
                Start:{" "}
                {new Date(
                  appointment.start_at
                ).toLocaleString()}
              </p>

              <p>
                End:{" "}
                {new Date(
                  appointment.end_at
                ).toLocaleString()}
              </p>

              {appointment.location && (
                <p>
                  Location: {appointment.location}
                </p>
              )}

              <p>
                Status: {appointment.status}
              </p>

              {appointment.status !== "cancelled" && (
                <button
                  onClick={() =>
                    handleCancelAppointment(
                      appointment.id
                    )
                  }
                >
                  Cancel
                </button>
              )}

              <button
                onClick={() =>
                  handleDeleteAppointment(
                    appointment.id
                  )
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
