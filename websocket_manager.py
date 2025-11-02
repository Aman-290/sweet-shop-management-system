"""WebSocket connection manager for real-time updates."""

from typing import List
from fastapi import WebSocket


class ConnectionManager:
    """Manages WebSocket connections and broadcasts messages."""

    def __init__(self):
        """Initialize the connection manager with an empty list of active connections."""
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept and register a new WebSocket connection.

        Args:
            websocket: The WebSocket connection to register.
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection from the active list.

        Args:
            websocket: The WebSocket connection to remove.
        """
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """Broadcast a message to all connected clients.

        Args:
            message: Dictionary containing the event type and data to broadcast.
        """
        # Remove disconnected clients
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for connection in disconnected:
            self.active_connections.remove(connection)


# Global instance
manager = ConnectionManager()
