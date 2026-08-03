from app.services.action_dispatcher import dispatch_action


class FakeMessage:
    ai_processed = True
    ai_action_required = True
    ai_intent = "question"


message = FakeMessage()

result = dispatch_action(
    db=None,
    message=message,
)

print("Dispatcher result:", result)