import { NavLink } from "react-router-dom";

const navigation = [
  { name: "Dashboard", path: "/" },
  { name: "Inbox", path: "/inbox" },
  { name: "Conversations", path: "/conversations" },
  { name: "Tasks", path: "/tasks" },
  { name: "Reminders", path: "/reminders" },
  { name: "Appointments", path: "/appointments" },
  { name: "Contacts", path: "/contacts" },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <h2>AI Command Center</h2>
      </div>

      <nav className="sidebar-nav">
        {navigation.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              isActive ? "nav-link active" : "nav-link"
            }
          >
            {item.name}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
