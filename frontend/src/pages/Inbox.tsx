import { useEffect, useState } from "react";
import {
  getInboxMessages,
  markMessageRead,
  markMessageImportant,
  type Message,
} from "../api/inbox";

export default function Inbox() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadMessages() {
      try {
        const data = await getInboxMessages();
        setMessages(data);
      } catch (err) {
        console.error(err);
        setError("Failed to load inbox messages.");
      } finally {
        setLoading(false);
      }
    }

    loadMessages();
  }, []);

  async function handleMarkRead(messageId: number) {
    try {
      const updatedMessage = await markMessageRead(messageId);

      setMessages((currentMessages) =>
        currentMessages.map((message) =>
          message.id === messageId
            ? updatedMessage
            : message
        )
      );
    } catch (err) {
      console.error(err);
      setError("Failed to mark message as read.");
    }
  }

  async function handleMarkImportant(messageId: number) {
    try {
      const updatedMessage =
        await markMessageImportant(messageId);

      setMessages((currentMessages) =>
        currentMessages.map((message) =>
          message.id === messageId
            ? updatedMessage
            : message
        )
      );
    } catch (err) {
      console.error(err);
      setError("Failed to mark message as important.");
    }
  }

  if (loading) {
    return <div>Loading inbox...</div>;
  }

  return (
    <div>
      <h2>Inbox</h2>

      {error && <p>{error}</p>}

      {messages.length === 0 ? (
        <p>No messages found.</p>
      ) : (
        <div>
          {messages.map((message) => (
            <div key={message.id}>
              <h3>
                {message.sender_name || "Unknown sender"}
              </h3>

              <p>{message.content}</p>

              <small>
                {message.platform} · AI: {message.ai_status}
              </small>

              <div>
                {!message.is_read && (
                  <button
                    onClick={() =>
                      handleMarkRead(message.id)
                    }
                  >
                    Mark Read
                  </button>
                )}

                {!message.is_important && (
                  <button
                    onClick={() =>
                      handleMarkImportant(message.id)
                    }
                  >
                    Important
                  </button>
                )}
              </div>

              <hr />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
