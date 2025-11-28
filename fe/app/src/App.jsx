import { useState, useEffect } from 'react'
import './App.css'

const BE_API_URL = import.meta.env.VITE_BE_API_URL || '';

function App() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)

  const fetchUsers = async () => {
    try {
      const response = await fetch(`${BE_API_URL}/users`)
      if (response.ok) {
        const data = await response.json()
        setUsers(data)
      }
    } catch (error) {
      console.error("Failed to fetch users:", error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchUsers()
    const interval = setInterval(fetchUsers, 5000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="container">
      <h1>User Data Dashboard</h1>
      <p className="subtitle">
        Syncing data via Celery Workers...
      </p>

      {loading && users.length === 0 ? (
        <p>Loading...</p>
      ) : (
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>User Info</th>
                <th>Address</th>
                <th>Credit Card</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.uid}>
                  <td>
                    <strong>{user.name}</strong>
                    <br />
                    <span className="text-sm">{user.email}</span>
                  </td>
                  <td>
                    {user.address ? (
                      <>
                        {user.address.street_name}, {user.address.city}
                        <br />
                        <span className="tag country">{user.address.country}</span>
                      </>
                    ) : (
                      <span className="pending">Pending...</span>
                    )}
                  </td>
                  <td>
                    {user.credit_card ? (
                      <>
                        <div className="cc-number">**** **** **** {user.credit_card.cc_number.slice(-4)}</div>
                        <span className="text-sm">{user.credit_card.cc_type}</span>
                      </>
                    ) : (
                      <span className="pending">Pending...</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

export default App
