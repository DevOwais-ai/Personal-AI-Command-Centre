import { useEffect, useState } from "react";
import {
  getConversations,
  type Conversation,
} from "../api/conversations";

export default function Conversations() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadConversations() {
      try {
        const data = await getConversations();
        setConversations(data);
      } catch (err) {
        console.error(err);
        setError("Failed to load conversations.");
      } finally {
        setLoading(false);
      }
    }

    loadConversations();
  }, []);

  if (loading) {
    return <div>Loading conversations...</div>;
  }

  return (
    <div>
      <h2>Conversations</h2>

      {error && <p>{error}</p>}

      {conversations.length === 0 ? (
        <p>No conversations found.</p>
      ) : (
        <div>
          {conversations.map((conversation) => (
            <div key={conversation.id}>
              <h3>
                {conversation.title || "Untitled Conversation"}
              </h3>

              <p>
                Platform: {conversation.platform}
              </p>

              <p>
                Status: {conversation.status}
              </p>

              {conversation.last_message_at && (
                <small>
                  Last message:{" "}
                  {new Date(
                    conversation.last_message_at
                  ).toLocaleString()}
                </small>
              )}

              <hr />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}