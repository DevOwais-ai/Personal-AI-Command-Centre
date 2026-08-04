import { useEffect, useState } from "react";
import {
  createContact,
  deleteContact,
  getContacts,
  updateContact,
  type Contact,
} from "../api/contacts";

export default function Contacts() {
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [company, setCompany] = useState("");
  const [notes, setNotes] = useState("");

  useEffect(() => {
    loadContacts();
  }, []);

  async function loadContacts() {
    try {
      setLoading(true);

      const data = await getContacts();

      setContacts(data);
      setError("");
    } catch (err) {
      console.error(err);
      setError("Failed to load contacts.");
    } finally {
      setLoading(false);
    }
  }

  async function handleCreateContact(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    if (!name.trim()) {
      setError("Contact name is required.");
      return;
    }

    try {
      const newContact = await createContact({
        name: name.trim(),
        email: email.trim() || undefined,
        phone: phone.trim() || undefined,
        company: company.trim() || undefined,
        notes: notes.trim() || undefined,
      });

      setContacts((currentContacts) => [
        newContact,
        ...currentContacts,
      ]);

      setName("");
      setEmail("");
      setPhone("");
      setCompany("");
      setNotes("");
      setError("");
    } catch (err) {
      console.error(err);
      setError("Failed to create contact.");
    }
  }

  async function handleUpdateContact(contact: Contact) {
    const updatedName = window.prompt(
      "Enter contact name:",
      contact.name
    );

    if (updatedName === null) {
      return;
    }

    if (!updatedName.trim()) {
      setError("Contact name is required.");
      return;
    }

    try {
      const updatedContact = await updateContact(
        contact.id,
        {
          name: updatedName.trim(),
        }
      );

      setContacts((currentContacts) =>
        currentContacts.map((item) =>
          item.id === contact.id
            ? updatedContact
            : item
        )
      );

      setError("");
    } catch (err) {
      console.error(err);
      setError("Failed to update contact.");
    }
  }

  async function handleDeleteContact(contactId: number) {
    try {
      await deleteContact(contactId);

      setContacts((currentContacts) =>
        currentContacts.filter(
          (contact) => contact.id !== contactId
        )
      );
    } catch (err) {
      console.error(err);
      setError("Failed to delete contact.");
    }
  }

  if (loading) {
    return <div>Loading contacts...</div>;
  }

  return (
    <div>
      <h2>Contacts</h2>

      {error && <p>{error}</p>}

      <form onSubmit={handleCreateContact}>
        <div>
          <label htmlFor="contact-name">
            Name
          </label>

          <input
            id="contact-name"
            type="text"
            value={name}
            onChange={(event) =>
              setName(event.target.value)
            }
            placeholder="Contact name"
          />
        </div>

        <div>
          <label htmlFor="contact-email">
            Email
          </label>

          <input
            id="contact-email"
            type="email"
            value={email}
            onChange={(event) =>
              setEmail(event.target.value)
            }
            placeholder="Email"
          />
        </div>

        <div>
          <label htmlFor="contact-phone">
            Phone
          </label>

          <input
            id="contact-phone"
            type="text"
            value={phone}
            onChange={(event) =>
              setPhone(event.target.value)
            }
            placeholder="Phone"
          />
        </div>

        <div>
          <label htmlFor="contact-company">
            Company
          </label>

          <input
            id="contact-company"
            type="text"
            value={company}
            onChange={(event) =>
              setCompany(event.target.value)
            }
            placeholder="Company"
          />
        </div>

        <div>
          <label htmlFor="contact-notes">
            Notes
          </label>

          <textarea
            id="contact-notes"
            value={notes}
            onChange={(event) =>
              setNotes(event.target.value)
            }
            placeholder="Notes"
          />
        </div>

        <button type="submit">
          Add Contact
        </button>
      </form>

      <hr />

      {contacts.length === 0 ? (
        <p>No contacts found.</p>
      ) : (
        <div>
          {contacts.map((contact) => (
            <div key={contact.id}>
              <h3>{contact.name}</h3>

              {contact.email && (
                <p>Email: {contact.email}</p>
              )}

              {contact.phone && (
                <p>Phone: {contact.phone}</p>
              )}

              {contact.company && (
                <p>
                  Company: {contact.company}
                </p>
              )}

              {contact.notes && (
                <p>Notes: {contact.notes}</p>
              )}

              <button
                onClick={() =>
                  handleUpdateContact(contact)
                }
              >
                Edit
              </button>

              <button
                onClick={() =>
                  handleDeleteContact(contact.id)
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