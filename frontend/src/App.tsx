import { BrowserRouter, Route, Routes } from "react-router-dom";

import Login from "./pages/Login";
import AppLayout from "./layouts/AppLayout";
import Dashboard from "./pages/Dashboard";
import Inbox from "./pages/Inbox";
import Conversations from "./pages/Conversations";
import Tasks from "./pages/Tasks";
import Appointments from "./pages/Appointments";
import Contacts from "./pages/Contacts";
import Reminders from "./pages/Reminders";

// function Inbox() {
//   return <h2>Inbox</h2>;
// }

// function Conversations() {
//   return <h2>Conversations</h2>;
// }

// function Tasks() {
//   return <h2>Tasks</h2>;
// }

// function Reminders() {
//   return <h2>Reminders</h2>;
// }

// function Appointments() {
//   return <h2>Appointments</h2>;
// }

// function Contacts() {
//   return <h2>Contacts</h2>;
// }

function NotFound() {
  return <h2>Page Not Found</h2>;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/login" element={<Login />} />
        
        <Route element={<AppLayout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/inbox" element={<Inbox />} />
          <Route path="/conversations" element={<Conversations />} />
          <Route path="/tasks" element={<Tasks />} />
          <Route path="/reminders" element={<Reminders />} />
          <Route path="/appointments" element={<Appointments />} />
          <Route path="/contacts" element={<Contacts />} />
        </Route>

        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}
