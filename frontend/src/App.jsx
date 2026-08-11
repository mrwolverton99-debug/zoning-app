import { useState, useRef } from 'react'
import axios from 'axios'
import './App.css'


const NAVY = '#1a2744'
const NAVY_LIGHT = '#243660'
const ACCENT = '#c8a951'
const GREEN = '#2d6a4f'
const GREEN_LIGHT = '#e8f5ee'
const YELLOW = '#f59e0b'
const YELLOW_LIGHT = '#fffbeb'
const RED = '#b91c1c'
const RED_LIGHT = '#fef2f2'
const GRAY = '#eef1f7'
const BORDER = '#e2e6ed'

const DISTRICT_NAMES = {
  'AG': 'Agricultural',
  'SF-E': 'Single-Family Estate',
  'SF-10': 'Single-Family Residential',
  'SF-7': 'Single-Family Residential',
  'SF-5': 'Single-Family Residential',
  'SFA': 'Single-Family Attached',
  '2F': 'Two-Family',
  'MF': 'Multifamily',
  'NO': 'Neighborhood Office',
  'CO': 'Community Office',
  'NS': 'Neighborhood Service',
  'CR': 'Community Retail',
  'LC': 'Limited Commercial',
  'HC': 'Heavy Commercial',
  'IN': 'Industrial',
  'UR': 'Urban Residential',
  'UB': 'Urban Business',
  'DT': 'Downtown',
}

const styles = {
  root: {
    fontFamily: "Georgia, serif",
    background: `#eef1f7 url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%231a2744' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
    minHeight: '100vh',
    margin: 0,
    padding: 0,
  },
  header: {
    background: NAVY,
    borderBottom: `3px solid ${ACCENT}`,
    padding: '0 32px',
    display: 'flex',
    alignItems: 'center',
    height: '64px',
    gap: '16px',
  },
  headerTitle: {
    color: 'white',
    fontSize: '18px',
    fontWeight: 'bold',
    letterSpacing: '0.5px',
    margin: 0,
  },
  headerSub: {
    color: ACCENT,
    fontSize: '12px',
    letterSpacing: '1.5px',
    textTransform: 'uppercase',
    margin: 0,
  },
  badge: {
    background: ACCENT,
    color: NAVY,
    fontSize: '10px',
    fontWeight: 'bold',
    letterSpacing: '1px',
    padding: '3px 8px',
    borderRadius: '2px',
    textTransform: 'uppercase',
  },
  main: {
    maxWidth: '1600px',
    margin: '0 auto',
    padding: '32px 32px',
  },
  searchCard: {
    background: 'white',
    border: `1px solid ${BORDER}`,
    borderTop: `3px solid ${NAVY}`,
    borderRadius: '4px',
    padding: '24px',
    marginBottom: '24px',
    boxShadow: '0 1px 4px rgba(0,0,0,0.06)',
  },
  searchLabel: {
    fontSize: '11px',
    fontWeight: 'bold',
    letterSpacing: '1.2px',
    textTransform: 'uppercase',
    color: '#64748b',
    marginBottom: '6px',
    display: 'block',
  },
  inputRow: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr auto',
    gap: '12px',
    alignItems: 'end',
  },
  input: {
    width: '100%',
    padding: '10px 14px',
    fontSize: '15px',
    border: `1px solid ${BORDER}`,
    borderRadius: '3px',
    outline: 'none',
    fontFamily: 'inherit',
    boxSizing: 'border-box',
  },
  button: {
    padding: '10px 28px',
    background: NAVY,
    color: 'white',
    border: 'none',
    borderRadius: '3px',
    fontSize: '14px',
    fontWeight: 'bold',
    letterSpacing: '0.5px',
    cursor: 'pointer',
    whiteSpace: 'nowrap',
    height: '42px',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(420px, 1fr))',
    gap: '20px',
  },
  gridFull: {
    gridColumn: '1 / -1',
  },
  card: {
    background: 'white',
    border: `1px solid ${BORDER}`,
    borderRadius: '4px',
    overflow: 'hidden',
    boxShadow: '0 1px 4px rgba(0,0,0,0.06)',
  },
  cardHeader: {
    background: NAVY,
    padding: '10px 16px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  cardTitle: {
    color: 'white',
    fontSize: '11px',
    fontWeight: 'bold',
    letterSpacing: '1.2px',
    textTransform: 'uppercase',
    margin: 0,
  },
  cardBody: {
    padding: '16px',
  },
  dataRow: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'baseline',
    padding: '6px 0',
    borderBottom: `1px solid ${BORDER}`,
  },
  dataLabel: {
    fontSize: '12px',
    color: '#64748b',
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
  },
  dataValue: {
    fontSize: '14px',
    fontWeight: '600',
    color: '#1e293b',
    textAlign: 'right',
  },
  districtBig: {
    fontSize: '48px',
    fontWeight: 'bold',
    color: NAVY,
    lineHeight: 1,
    fontFamily: 'Georgia, serif',
  },
  pill: {
    display: 'inline-block',
    padding: '3px 10px',
    borderRadius: '2px',
    fontSize: '11px',
    fontWeight: 'bold',
    letterSpacing: '0.5px',
  },
  useList: {
    listStyle: 'none',
    padding: 0,
    margin: 0,
  },
  useItem: {
    padding: '5px 0',
    fontSize: '13px',
    borderBottom: `1px solid ${BORDER}`,
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    color: '#334155',
  },
  sectionLabel: {
    fontSize: '10px',
    fontWeight: 'bold',
    letterSpacing: '1.5px',
    textTransform: 'uppercase',
    color: '#94a3b8',
    margin: '12px 0 6px',
  },
  analysisSection: {
    marginBottom: '16px',
    paddingBottom: '16px',
    borderBottom: `1px solid ${BORDER}`,
  },
analysisText: {
    fontSize: '14px',
    color: '#334155',
    lineHeight: '1.6',
    textAlign: 'left',
  },
  analysisLabel: {
    fontSize: '10px',
    fontWeight: 'bold',
    letterSpacing: '1.5px',
    textTransform: 'uppercase',
    color: '#94a3b8',
    marginBottom: '6px',
    textAlign: 'left',
  },
  bulletList: {
    margin: '4px 0 0',
    paddingLeft: '16px',
    fontSize: '13px',
    color: '#334155',
    lineHeight: '1.7',
  },
  redFlagBox: {
    background: RED_LIGHT,
    border: `1px solid #fca5a5`,
    borderRadius: '3px',
    padding: '10px 14px',
    marginBottom: '8px',
  },
  disclaimer: {
    background: GREEN_LIGHT,
    border: `1px solid #86efac`,
    borderRadius: '3px',
    padding: '10px 14px',
    fontSize: '12px',
    color: '#166534',
    gridColumn: '1 / -1',
  },
  errorBox: {
    background: RED_LIGHT,
    border: `1px solid #fca5a5`,
    borderRadius: '3px',
    padding: '12px 16px',
    color: RED,
    fontSize: '14px',
  },
  supWarning: {
    background: YELLOW_LIGHT,
    border: `1px solid #fde68a`,
    borderRadius: '3px',
    padding: '10px 14px',
    fontSize: '13px',
    color: '#92400e',
    marginTop: '8px',
  },
}

function StatusPill({ status }) {
  const config = {
    permitted_by_right: { bg: GREEN_LIGHT, color: GREEN, border: '#86efac', label: '✓ Permitted by Right' },
    requires_sup: { bg: YELLOW_LIGHT, color: '#92400e', border: '#fde68a', label: '⚠ Requires SUP' },
    prohibited: { bg: RED_LIGHT, color: RED, border: '#fca5a5', label: '✗ Prohibited' },
    requires_rezoning: { bg: RED_LIGHT, color: RED, border: '#fca5a5', label: '✗ Requires Rezoning' },
    special_standards: { bg: '#eff6ff', color: '#1e40af', border: '#93c5fd', label: '★ Special Standards' },
    development_standard: { bg: '#f0f9ff', color: '#0369a1', border: '#7dd3fc', label: '📋 Development Standard' },
  }
  const c = config[status] || config.prohibited
  return (
    <span style={{ ...styles.pill, background: c.bg, color: c.color, border: `1px solid ${c.border}` }}>
      {c.label}
    </span>
  )
}

function CollapsibleUseList({ items, color, bullet, initialShow = 5 }) {
  const [expanded, setExpanded] = useState(false)
  if (!items?.length) return null
  const visible = expanded ? items : items.slice(0, initialShow)
  const hidden = items.length - initialShow
  return (
    <>
      <ul style={styles.useList}>
        {visible.map(u => (
          <li key={u} style={{ ...styles.useItem, color: color || '#334155' }}>
            <span style={{ color: bullet, fontSize: '10px' }}>●</span> {u}
          </li>
        ))}
      </ul>
      {items.length > initialShow && (
        <button
          onClick={() => setExpanded(!expanded)}
          style={{
            background: 'none', border: `1px solid ${BORDER}`, color: '#475569', fontSize: '11px',
            cursor: 'pointer', padding: '4px 10px', letterSpacing: '0.5px', borderRadius: '3px',
            marginTop: '4px', display: 'block', width: '100%', textAlign: 'center',
          }}
        >
          {expanded ? '▲ Show less' : `▼ Show ${hidden} more`}
        </button>
      )}
    </>
  )
}

function Card({ title, children, accent, fullWidth, badge }) {
  return (
    <div style={{ ...styles.card, ...(fullWidth ? styles.gridFull : {}) }}>
      <div style={{ ...styles.cardHeader, ...(accent ? { borderBottom: `2px solid ${accent}` } : {}) }}>
        <span style={styles.cardTitle}>{title}</span>
        {badge && <span style={{ ...styles.pill, background: ACCENT, color: NAVY, fontSize: '10px' }}>{badge}</span>}
      </div>
      <div style={styles.cardBody}>{children}</div>
    </div>
  )
}

export default function App() {
  const [address, setAddress] = useState('')
  const [proposedUse, setProposedUse] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const [suggestions, setSuggestions] = useState([])
  const [showSuggestions, setShowSuggestions] = useState(false)

  const BLOCKED_TERMS = [
    'nigger', 'nigga', 'faggot', 'chink', 'spic', 'kike', 'wetback', 'retard',
    'dildo', 'penis', 'vagina',
  ]

  const validateProposedUse = (text) => {
    const lower = text.toLowerCase().trim()
    if (BLOCKED_TERMS.some(term => lower.includes(term))) {
      return "Please enter a valid proposed use description."
    }
    return null
  }

  const suggestTimer = useRef(null)

  const fetchSuggestions = (value) => {
  clearTimeout(suggestTimer.current)
  if (value.trim().length < 3) {
    setSuggestions([])
    setShowSuggestions(false)
    return
  }
  suggestTimer.current = setTimeout(async () => {
    try {
      const resp = await axios.get('http://127.0.0.1:8000/suggest', {
        params: { q: value.trim(), city: 'garland' }
      })
      setSuggestions(resp.data.suggestions || [])
      setShowSuggestions(true)
    } catch {
      setSuggestions([])
    }
    }, 300)
  }

  const handleLookup = async () => {
    if (!address.trim()) return
      setShowSuggestions(false)
      setSuggestions([])
      clearTimeout(suggestTimer.current)
    if (proposedUse.trim()) {
      const validationError = validateProposedUse(proposedUse.trim())
      if (validationError) {
        setError(validationError)
        return
      }
    }
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const params = { address: address.trim() }
      if (proposedUse.trim()) params.proposed_use = proposedUse.trim()
      const response = await axios.get('http://127.0.0.1:8000/lookup', {
        params: { ...params, city: 'garland' }
      })
      setShowSuggestions(false)
      setResult(response.data)
    } catch (err) {
      if (err.response?.status === 429) {
        setError('Too many lookups from this connection. Please try again in an hour.')
      } else {
        setError(err.response?.data?.detail || 'Address not found. Check the address and try again.')
      }
    } finally {
      setLoading(false)
    }
  }

const handlePrint = () => {
    window.print()
  }

  const handleReport = (r) => {
    const subject = encodeURIComponent(`Zoning App Issue — ${r.street_num || ''} ${r.street_name || ''}`.trim())
    const body = encodeURIComponent(
      `Address: ${r.street_num || ''} ${r.street_name || ''}\n` +
      `Zoning: ${r.base_zone || ''}\n` +
      `Sub-district: ${r.dt_subdistrict || 'N/A'}\n` +
      `Proposed use: ${proposedUse || 'N/A'}\n` +
      `\nDescribe the issue:\n`
    )
    window.open(`mailto:mwolverton@garlandtx.gov?subject=${subject}&body=${body}`)
  }

  const r = result

  return (
    <div style={styles.root}>
      <style>{`
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        @media print {
          header { background: #1a2744 !important; -webkit-print-color-adjust: exact; }
          .no-print { display: none !important; }
          body { font-size: 12px; }
  }
`}</style>
      <header style={styles.header} className="site-header">
        <div>
          <p style={styles.headerSub}>City of Garland, TX</p>
          <h1 style={styles.headerTitle}>Zoning Pre-Application Analysis</h1>
        </div>
        <span style={{ marginLeft: 'auto', ...styles.badge }}>Beta</span>
      </header>

      <main style={styles.main} className="main-content">
        <div style={styles.searchCard} className="no-print">
          <div style={styles.inputRow} className="input-row">
            <div style={{ position: 'relative' }}>
              <label style={styles.searchLabel}>Property Address</label>
              <input
                style={styles.input}
                type="text"
                value={address}
                onChange={e => {
                  setAddress(e.target.value)
                  fetchSuggestions(e.target.value)
                }}
                onKeyDown={e => {
                  if (e.key === 'Enter') { setShowSuggestions(false); handleLookup() }
                  if (e.key === 'Escape') setShowSuggestions(false)
                }}
                onBlur={() => setTimeout(() => setShowSuggestions(false), 150)}
                placeholder="e.g. 4701 Miami Dr"
              />
              {showSuggestions && suggestions.length > 0 && (
                <div style={{
                  position: 'absolute', top: '100%', left: 0, right: 0,
                  background: 'white', border: `1px solid ${BORDER}`, borderTop: 'none',
                  borderRadius: '0 0 3px 3px', boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
                  zIndex: 100, maxHeight: '240px', overflowY: 'auto',
                }}>
                  {suggestions.map(s => (
                    <div
                      key={s}
                      onMouseDown={() => {
                        setAddress(s)
                        setSuggestions([])
                        setShowSuggestions(false)
                      }}
                      style={{
                        padding: '8px 14px', fontSize: '13px', cursor: 'pointer',
                        borderBottom: `1px solid ${BORDER}`, color: '#334155',
                      }}
                      onMouseEnter={e => e.currentTarget.style.background = GRAY}
                      onMouseLeave={e => e.currentTarget.style.background = 'white'}
                    >
                      {s}
                    </div>
                  ))}
                </div>
              )}
            </div>
            <div>
              <label style={styles.searchLabel}>Proposed Use (optional)</label>
              <input
                style={styles.input}
                type="text"
                value={proposedUse}
                onChange={e => setProposedUse(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleLookup()}
                placeholder="e.g. restaurant, auto repair, laundromat"
              />
            </div>
<div style={{ display: 'flex', gap: '8px', alignItems: 'flex-end' }} className="button-row">
              <button
                style={{ ...styles.button, opacity: loading || !address ? 0.6 : 1, display: 'flex', alignItems: 'center', gap: '8px' }}
                onClick={handleLookup}
                disabled={loading || !address}
              >
                {loading ? (
                  <>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5"
                      style={{ animation: 'spin 0.8s linear infinite' }}>
                      <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
                    </svg>
                    Looking up...
                  </>
                ) : 'Look Up'}
              </button>
              <button
                onClick={() => { setResult(null); setError(null); setAddress(''); setProposedUse(''); setSuggestions([]); setShowSuggestions(false); }}
                style={{
                  padding: '10px 16px',
                  background: 'none',
                  color: '#64748b',
                  border: `1px solid ${BORDER}`,
                  borderRadius: '3px',
                  fontSize: '13px',
                  cursor: 'pointer',
                  height: '42px',
                  opacity: (result || error) ? 1 : 0,
                  pointerEvents: (result || error) ? 'auto' : 'none',
                }}
              >
                Clear
              </button>
            </div>
          </div>
        </div>

        {error && <div style={{ ...styles.errorBox, marginBottom: '20px' }}>⚠ {error}</div>}

        {r && (
          <div style={styles.grid} className="analysis-grid">
            <Card title="Parcel Information">
              <div style={styles.dataRow}>
                <span style={styles.dataLabel}>Address</span>
                <span style={styles.dataValue}>{r.street_num} {r.street_name}</span>
              </div>
              <div style={styles.dataRow}>
                <span style={styles.dataLabel}>City / ZIP</span>
                <span style={styles.dataValue}>Garland TX {r.zipcode?.trim().replace(/^(\d{5})(\d{4})$/, '$1-$2')}</span>
              </div>
              <div style={styles.dataRow}>
                <span style={styles.dataLabel}>Account No.</span>
                <span style={{ ...styles.dataValue, fontFamily: 'monospace', fontSize: '12px' }}>{r.account_num}</span>
              </div>
              <div style={{ ...styles.dataRow, borderBottom: 'none' }}>
                <span style={styles.dataLabel}>FLUM Designation</span>
                <span style={styles.dataValue}>{r.flum_designation}</span>
              </div>
              {r.geocoded_fallback && (
                <div style={{ fontSize: '11px', color: '#92400e', marginTop: '8px',
                  padding: '6px 8px', background: '#fffbeb', borderRadius: '3px',
                  border: '1px solid #fde68a' }}>
                  ⚠ Address not in DCAD — account number unavailable. Zoning and FLUM retrieved via coordinates.
                </div>
              )}
            </Card>

            <Card title="Zoning District" accent={ACCENT}>
              {r.requires_manual_review ? (
                <div style={{ ...styles.supWarning, marginTop: 0 }}>
                  <strong>⚠ Planned Development (PD) {r.pd_num && `— ${r.pd_num}`}</strong>
                  <p style={{ margin: '4px 0 0', fontSize: '13px' }}>
                    Permitted uses are governed by the specific PD ordinance, not the standard use matrix.
                    Look up the PD ordinance to confirm what is permitted.
                  </p>
                <div style={{ marginTop: '8px', display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                    <a href="https://recordsearch.garlandtx.gov/publicaccess/" target="_blank" rel="noopener noreferrer"
                      style={{ fontSize: '12px', color: '#92400e', fontWeight: 'bold' }}>
                      🔍 Search PD Ordinances →
                    </a>
                    <a href="https://maps.garlandtx.gov/cogmap/apps/webappviewer/index.html?id=3654219b16bc49b799eed665a10eeb86" target="_blank" rel="noopener noreferrer"
                      style={{ fontSize: '12px', color: '#92400e', fontWeight: 'bold' }}>
                      🗺 View on Zoning Map →
                    </a>
                    <span style={{ fontSize: '12px', color: '#92400e' }}>
                      or call Planning: 972-205-2454
                    </span>
                  </div>
                  {proposedUse && (
                    <p style={{ margin: '8px 0 0', fontSize: '12px', color: '#92400e' }}>
                      Proposed use "{proposedUse}" — verify this use is permitted under PD {r.pd_num} before proceeding.
                    </p>
                  )}
                </div>
              ) : (
                <>
                  <div style={{ display: 'flex', alignItems: 'baseline', gap: '12px', marginBottom: '12px' }}>
                    <div>
                      <span style={styles.districtBig} className="district-big">{r.is_planned_development ? 'PD' : r.base_zone}</span>
                      {DISTRICT_NAMES[r.base_zone] && (
                        <div style={{ fontSize: '13px', color: '#64748b', marginTop: '4px', letterSpacing: '0.5px' }}>
                          {DISTRICT_NAMES[r.base_zone]}
                        </div>
                      )}
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                      {r.dt_subdistrict && (
                        <span style={{ ...styles.pill, background: ACCENT, color: NAVY, fontSize: '11px' }}>
                          {r.dt_subdistrict} Sub-District
                        </span>
                      )}
                      {r.gdc_zoning && r.gdc_zoning !== r.base_zone && (
                        <span style={{ fontSize: '14px', color: '#64748b' }}>{r.gdc_zoning}</span>
                      )}
                    </div>
                  </div>
                  {r.has_existing_sup && (
                    <div style={styles.supWarning}>
                      <strong>Existing SUP on Parcel: {r.existing_sup_num}</strong>
                      <p style={{ margin: '4px 0 0', fontSize: '12px' }}>
                        A Specific Use Provision is recorded on this parcel. Verify which suite and use
                        it covers with Garland Planning before assuming coverage.
                      </p>
                    </div>
                  )}
                </>
              )}
            </Card>

            {r.proposed_use_check && (
              <Card title="Proposed Use Analysis" accent={
                r.proposed_use_check.status === 'permitted_by_right' ? '#86efac' :
                r.proposed_use_check.status === 'requires_sup' ? '#fde68a' : '#fca5a5'
              }>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
                  <div>
                    <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#1e293b' }}>
                      {r.proposed_use_check.match || proposedUse}
                    </div>
                    <div style={{ fontSize: '12px', color: '#64748b', marginTop: '2px' }}>
                      {r.proposed_use_check.category}
                    </div>
                  </div>
                  <StatusPill status={r.proposed_use_check.status} />
                </div>
                <div style={{ fontSize: '13px', color: '#475569' }}>{r.proposed_use_check.message}</div>
                {r.proposed_use_check.parking && (
                  <div style={{ marginTop: '8px', fontSize: '12px', color: '#475569',
                    background: '#f8fafc', padding: '6px 10px', borderRadius: '3px',
                    border: `1px solid ${BORDER}` }}>
                    🅿 <strong>Parking:</strong> {r.proposed_use_check.parking}
                  </div>
                )}
              </Card>
            )}

            {r.land_uses && !r.requires_manual_review && (
              <Card title={`Permitted Uses — ${r.land_uses?.subdistrict ? `DT (${r.land_uses.subdistrict})` : r.base_zone}`}>
                {r.land_uses.permitted_by_right?.length > 0 && (
                  <>
                    <div style={styles.sectionLabel}>✓ By Right</div>
                    <CollapsibleUseList items={r.land_uses.permitted_by_right} bullet={GREEN} />
                  </>
                )}
                {r.land_uses.requires_sup?.length > 0 && (
                  <>
                    <div style={{ ...styles.sectionLabel, marginTop: '16px' }}>⚠ Requires SUP</div>
                    <CollapsibleUseList items={r.land_uses.requires_sup} color="#92400e" bullet={YELLOW} />
                  </>
                )}
                {r.land_uses.special_standards?.length > 0 && (
                  <>
                    <div style={{ ...styles.sectionLabel, marginTop: '16px' }}>★ Special Standards</div>
                    <CollapsibleUseList items={r.land_uses.special_standards} color="#1e40af" bullet="#93c5fd" />
                  </>
                )}
              </Card>
            )}

            {r.ai_analysis && (
              <Card title="Pre-Application Staff Analysis" fullWidth accent={ACCENT}>
                <div style={styles.grid} className="results-grid">
                  <div>
                    <div style={styles.analysisSection}>
                      <div style={styles.analysisLabel}>Summary</div>
                      <div style={styles.analysisText}>{r.ai_analysis.summary}</div>
                    </div>
                    <div style={styles.analysisSection}>
                      <div style={styles.analysisLabel}>Approval Path</div>
                      <div style={styles.analysisText}>{r.ai_analysis.approval_path}</div>
                    </div>
                    <div style={styles.analysisSection}>
                      <div style={styles.analysisLabel}>Likely Staff Position</div>
                      <div style={styles.analysisText}>{r.ai_analysis.likely_staff_position}</div>
                    </div>
                    {r.ai_analysis.next_steps?.length > 0 && (
                      <div>
                        <div style={styles.analysisLabel}>Next Steps</div>
                        <ol style={styles.bulletList}>
                          {r.ai_analysis.next_steps.map((s, i) => <li key={i}>{s}</li>)}
                        </ol>
                      </div>
                    )}
                  </div>
                  <div>
                    {r.ai_analysis.red_flags?.length > 0 && (
                      <div style={styles.analysisSection}>
                        <div style={{ ...styles.analysisLabel, color: RED }}>⚠ Red Flags</div>
                        <div style={styles.redFlagBox}>
                          <ul style={{ ...styles.bulletList, color: RED, paddingLeft: '14px', margin: 0 }}>
                            {r.ai_analysis.red_flags.map((f, i) => <li key={i}>{f}</li>)}
                          </ul>
                        </div>
                      </div>
                    )}
                    {r.ai_analysis.key_considerations?.length > 0 && (
                      <div style={styles.analysisSection}>
                        <div style={styles.analysisLabel}>Key Considerations</div>
                        <ul style={styles.bulletList}>
                          {r.ai_analysis.key_considerations.map((c, i) => <li key={i}>{c}</li>)}
                        </ul>
                      </div>
                    )}
                    {r.ai_analysis.dimensional_flags?.length > 0 && (
                      <div>
                        <div style={styles.analysisLabel}>Dimensional Requirements</div>
                        <ul style={styles.bulletList}>
                          {r.ai_analysis.dimensional_flags.map((f, i) => <li key={i}>{f}</li>)}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
              </Card>
            )}

            {r && (
              <div style={{ ...styles.gridFull, textAlign: 'center', paddingBottom: '4px', display: 'flex', justifyContent: 'center', gap: '16px' }}>
                <button
                  onClick={handlePrint}
                  style={{ background: 'none', border: 'none', color: '#94a3b8', fontSize: '12px',
                    cursor: 'pointer', textDecoration: 'underline' }}
                >
                  🖨 Print this analysis
                </button>
                <button
                  onClick={() => handleReport(r)}
                  style={{ background: 'none', border: 'none', color: '#94a3b8', fontSize: '12px',
                    cursor: 'pointer', textDecoration: 'underline' }}
                >
                  Report an issue with this result
                </button>
              </div>
            )}
            <div style={styles.disclaimer}>
              ✓ Results appear subject to staff review and do not constitute zoning approval or compliance
              determination. Verify all information with Garland Planning & Development staff before
              submitting permit applications. 972-205-2454.
            </div>
          </div>
        )}
      </main>
    </div>
  )
}