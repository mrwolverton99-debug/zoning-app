import { useState } from 'react'
import axios from 'axios'

function StatusBadge({ status }) {
  const styles = {
    permitted_by_right: { background: '#dcfce7', color: '#166534', border: '1px solid #86efac' },
    requires_sup: { background: '#fef9c3', color: '#854d0e', border: '1px solid #fde047' },
    special_standards: { background: '#dbeafe', color: '#1e40af', border: '1px solid #93c5fd' },
    prohibited: { background: '#fee2e2', color: '#991b1b', border: '1px solid #fca5a5' },
  }
  const labels = {
    permitted_by_right: '✓ Permitted by Right',
    requires_sup: '⚠ Requires SUP',
    special_standards: '★ Special Standards Apply',
    prohibited: '✗ Prohibited',
  }
  const s = styles[status] || styles.prohibited
  return (
    <span style={{ ...s, padding: '4px 10px', borderRadius: '4px', fontSize: '13px', fontWeight: 'bold' }}>
      {labels[status] || status}
    </span>
  )
}

function App() {
  const [address, setAddress] = useState('')
  const [proposedUse, setProposedUse] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleLookup = async () => {
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const params = { address }
      if (proposedUse.trim()) params.proposed_use = proposedUse.trim()
      const response = await axios.get('http://127.0.0.1:8000/lookup', { params })
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: '680px', margin: '60px auto', fontFamily: 'sans-serif', padding: '0 20px' }}>
      <h1 style={{ fontSize: '24px', marginBottom: '4px' }}>Garland Zoning Lookup</h1>
      <p style={{ color: '#666', marginBottom: '24px', fontSize: '14px' }}>Enter a Garland TX address to look up zoning and permitted uses.</p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginBottom: '16px' }}>
        <input
          type="text"
          value={address}
          onChange={(e) => setAddress(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleLookup()}
          placeholder="Property address — e.g. 4701 MIAMI DR"
          style={{ padding: '10px', fontSize: '15px', border: '1px solid #ccc', borderRadius: '4px' }}
        />
        <div style={{ display: 'flex', gap: '8px' }}>
          <input
            type="text"
            value={proposedUse}
            onChange={(e) => setProposedUse(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleLookup()}
            placeholder="Proposed use (optional) — e.g. restaurant, auto repair"
            style={{ flex: 1, padding: '10px', fontSize: '15px', border: '1px solid #ccc', borderRadius: '4px' }}
          />
          <button
            onClick={handleLookup}
            disabled={loading || !address}
            style={{ padding: '10px 20px', fontSize: '15px', background: '#2563eb', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', whiteSpace: 'nowrap' }}
          >
            {loading ? 'Looking up...' : 'Look Up'}
          </button>
        </div>
      </div>

      {error && (
        <div style={{ background: '#fee2e2', border: '1px solid #fca5a5', borderRadius: '4px', padding: '12px', color: '#991b1b', marginBottom: '16px' }}>
          {error}
        </div>
      )}

      {result && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>

          {/* Header */}
          <div style={{ border: '1px solid #e5e7eb', borderRadius: '8px', padding: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <div style={{ fontSize: '13px', color: '#666' }}>Address</div>
              <div style={{ fontWeight: 'bold', fontSize: '16px' }}>{result.street_num} {result.street_name}, Garland TX {result.zipcode}</div>
              <div style={{ fontSize: '13px', color: '#666', marginTop: '4px' }}>Account: {result.account_num}</div>
            </div>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '13px', color: '#666' }}>Zoning District</div>
              <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#2563eb' }}>{result.base_zone}</div>
            </div>
          </div>

          {/* PD warning */}
          {result.requires_manual_review && (
            <div style={{ background: '#fef3c7', border: '1px solid #f59e0b', borderRadius: '8px', padding: '16px', color: '#92400e' }}>
              <strong>⚠ Planned Development (PD) — Manual Review Required</strong>
              <p style={{ margin: '4px 0 0', fontSize: '14px' }}>This parcel is zoned PD. Permitted uses are governed by the specific PD ordinance and cannot be determined automatically. Contact Garland Planning staff for review.</p>
            </div>
          )}

          {/* Proposed use check */}
          {result.proposed_use_check && (
            <div style={{ border: '1px solid #e5e7eb', borderRadius: '8px', padding: '16px' }}>
              <div style={{ fontSize: '13px', color: '#666', marginBottom: '8px' }}>Proposed Use Check</div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <div style={{ fontWeight: 'bold' }}>{result.proposed_use_check.match || proposedUse}</div>
                  <div style={{ fontSize: '13px', color: '#666' }}>{result.proposed_use_check.category}</div>
                </div>
                <StatusBadge status={result.proposed_use_check.status} />
              </div>
              <div style={{ marginTop: '10px', fontSize: '14px', color: '#444' }}>{result.proposed_use_check.message}</div>
            </div>
          )}

          {/* Permitted uses */}
          {result.land_uses && (
            <div style={{ border: '1px solid #e5e7eb', borderRadius: '8px', padding: '16px' }}>
              <div style={{ fontSize: '15px', fontWeight: 'bold', marginBottom: '12px' }}>Permitted Uses in {result.base_zone}</div>

              {result.land_uses.permitted_by_right.length > 0 && (
                <div style={{ marginBottom: '12px' }}>
                  <div style={{ fontSize: '13px', fontWeight: 'bold', color: '#166534', marginBottom: '6px' }}>✓ Permitted by Right</div>
                  <ul style={{ margin: 0, paddingLeft: '20px', fontSize: '14px', lineHeight: '1.8' }}>
                    {result.land_uses.permitted_by_right.map(u => <li key={u}>{u}</li>)}
                  </ul>
                </div>
              )}

              {result.land_uses.requires_sup.length > 0 && (
                <div style={{ marginBottom: '12px' }}>
                  <div style={{ fontSize: '13px', fontWeight: 'bold', color: '#854d0e', marginBottom: '6px' }}>⚠ Requires SUP</div>
                  <ul style={{ margin: 0, paddingLeft: '20px', fontSize: '14px', lineHeight: '1.8' }}>
                    {result.land_uses.requires_sup.map(u => <li key={u}>{u}</li>)}
                  </ul>
                </div>
              )}

              {result.land_uses.special_standards.length > 0 && (
                <div>
                  <div style={{ fontSize: '13px', fontWeight: 'bold', color: '#1e40af', marginBottom: '6px' }}>★ Special Standards Apply</div>
                  <ul style={{ margin: 0, paddingLeft: '20px', fontSize: '14px', lineHeight: '1.8' }}>
                    {result.land_uses.special_standards.map(u => <li key={u}>{u}</li>)}
                  </ul>
                </div>
              )}
            </div>
          )}

          {/* Disclaimer */}
          <div style={{ padding: '12px', background: '#f0fdf4', border: '1px solid #86efac', borderRadius: '4px', fontSize: '13px', color: '#166534' }}>
            ✓ Results appear subject to staff review and do not constitute zoning approval or compliance determination. Verify all information with Garland Planning staff before submitting permit applications.
          </div>

        </div>
      )}
    </div>
  )
}

export default App
