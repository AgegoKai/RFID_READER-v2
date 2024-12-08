from fastapi import FastAPI, Path, Body
from pydantic import BaseModel
from datetime import datetime
import uvicorn

# Define FastAPI app
app = FastAPI()

# Define the Pydantic model for the request body
class CardEvent(BaseModel):
    datetime: datetime  # ISO 8601 UTC datetime with seconds precision

# Endpoint POST with card_id as a path parameter and datetime in the request body
@app.post("/card/{card_id}")
async def add_card_event(
    card_id: int = Path(..., description="ID of the card, e.g., 12345"),
    event: CardEvent = Body(..., description="Object containing UTC datetime"),
):
    # Extract datetime from the body and log to the console
    received_datetime = event.datetime
    print(f"Received cardID: {card_id}, datetime: {received_datetime}")
    return {"cardID": card_id, "datetime": received_datetime.isoformat()}

# Run the application on port 8181
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8180)