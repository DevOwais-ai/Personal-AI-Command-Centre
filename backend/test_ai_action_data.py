from app.ai.factory import get_ai_provider


provider = get_ai_provider()

message = (
    "Please remind me tomorrow at 10 AM "
    "to send the client proposal."
)

analysis = provider.analyze_message(message)

print("Intent:", analysis.intent)
print("Action required:", analysis.action_required)
print("Action data:", analysis.action_data)

if analysis.action_data:
    print("Action data type:", type(analysis.action_data).__name__)