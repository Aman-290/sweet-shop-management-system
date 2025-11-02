// WebSocket hook for real-time updates
import { useEffect, useRef, useCallback } from 'react'

const WS_URL = 'ws://127.0.0.1:8000/ws'

export const useWebSocket = (onMessage) => {
  const ws = useRef(null)
  const reconnectTimeout = useRef(null)

  const connect = useCallback(() => {
    try {
      ws.current = new WebSocket(WS_URL)

      ws.current.onopen = () => {
        console.log('✅ WebSocket connected')
      }

      ws.current.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data)
          onMessage(message)
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error)
        }
      }

      ws.current.onerror = (error) => {
        console.error('WebSocket error:', error)
      }

      ws.current.onclose = () => {
        console.log('❌ WebSocket disconnected. Reconnecting in 3s...')
        // Auto-reconnect after 3 seconds
        reconnectTimeout.current = setTimeout(connect, 3000)
      }
    } catch (error) {
      console.error('Failed to connect WebSocket:', error)
      // Retry connection after 3 seconds
      reconnectTimeout.current = setTimeout(connect, 3000)
    }
  }, [onMessage])

  useEffect(() => {
    connect()

    return () => {
      if (reconnectTimeout.current) {
        clearTimeout(reconnectTimeout.current)
      }
      if (ws.current) {
        ws.current.close()
      }
    }
  }, [connect])

  return ws
}
