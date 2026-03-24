import { useState } from 'react'
import axios from 'axios'

const NAVY = '#1a2744'
const NAVY_LIGHT = '#243660'
const ACCENT = '#c8a951'
const GREEN = '#2d6a4f'
const GREEN_LIGHT = '#e8f5ee'
const YELLOW = '#f59e0b'
const YELLOW_LIGHT = '#fffbeb'
const RED = '#b91c1c'
const RED_LIGHT = '#fef2f2'
const GRAY = '#f8f9fb'
const BORDER = '#e2e6ed'

const styles = {
  root: {
    fontFamily: "Georgia, serif",
    background: '#f4f6fa',
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
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '32px 24px',
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
    gridTemplateColumns: '1fr 1fr',
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
  analysisLabel: {
    fontSize: '10px',
    fontWeight: 'bold',
    letterSpacing: '1.5px',
    textTransform: 'uppercase',
    color: '#94a3b8',
    marginBottom: '6px',
  },
  analysisText: {
    fontSize: '14px',
    color: '#334155',
    lineHeight: '1.6',
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
  }
  const c = config[status] || config.prohibited
  return (
    <span style={{ ...styles.pill, background: c.bg, color: c.color, border: `1px solid ${c.border}` }}>
      {c.label}
    </span>
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

  const handleLookup = async () => {
    if (!address.trim()) return
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const params = { address: address.trim() }
      if (proposedUse.trim()) params.proposed_use = proposedUse.trim()
      const response = await axios.get('http://127.0.0.1:8000/lookup', { params })
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Address not found. Check the address and try again.')
    } finally {
      setLoading(false)
    }
  }

  const r = result

  return (
    <div style={styles.root}>
      {/* Header */}
      <header style={styles.header}>
        <div>
          <p style={styles.headerSub}>City of Garland, TX</p>
          <h1 style={styles.headerTitle}>Zoning Pre-Application Analysis</h1>
        </div>
        <span style={{ marginLeft: 'auto', ...styles.badge }}>Beta</span>
      </header>

      <main style={styles.main}>
        {/* Search */}
        <div style={styles.searchCard}>
          <div style={styles.inputRow}>
            <div>
              <label style={styles.searchLabel}>Property Address</label>
              <input
                style={styles.input}
                type="text"
                value={address}
                onChange={e => setAddress(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleLookup()}
                placeholder="e.g. 4701 Miami Dr"
              />
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
            <button
              style={{ ...styles.button, opacity: loading || !address ? 0.6 : 1 }}
              onClick={handleLookup}
              disabled={loading || !address}
            >
              {loading ? 'Looking up...' : 'Look Up'}
            </button>
          </div>
        </div>

        {error && <div style={{ ...styles.errorBox, marginBottom: '20px' }}>⚠ {error}</div>}

        {r && (
          <div style={styles.grid}>

            {/* Parcel Info */}
            <Card title="Parcel Information">
              <div style={styles.dataRow}>
                <span style={styles.dataLabel}>Address</span>
                <span style={styles.dataValue}>{r.street_num} {r.street_name}</span>
              </div>
              <div style={styles.dataRow}>
                <span style={styles.dataLabel}>City / ZIP</span>
                <span style={styles.dataValue}>Garland TX {r.zipcode?.trim()}</span>
              </div>
              <div style={styles.dataRow}>
                <span style={styles.dataLabel}>Account No.</span>
                <span style={{ ...styles.dataValue, fontFamily: 'monospace', fontSize: '12px' }}>{r.account_num}</span>
              </div>
              <div style={{ ...styles.dataRow, borderBottom: 'none' }}>
                <span style={styles.dataLabel}>FLUM Designation</span>
                <span style={styles.dataValue}>{r.flum_designation}</span>
              </div>
            </Card>

            {/* Zoning District */}
            <Card title="Zoning District" accent={ACCENT}>
              {r.requires_manual_review ? (
                <div style={{ ...styles.supWarning, marginTop: 0 }}>
                  <strong>⚠ Planned Development (PD)</strong>
                  <p style={{ margin: '4px 0 0', fontSize: '13px' }}>
                    This parcel is zoned PD. Permitted uses are governed by the specific PD ordinance.
                    Contact Garland Planning staff for review.
                  </p>
                </div>
              ) : (
                <>
                  <div style={{ display: 'flex', alignItems: 'baseline', gap: '12px', marginBottom: '12px' }}>
                    <span style={styles.districtBig}>{r.base_zone}</span>
                    {r.gdc_zoning && r.gdc_zoning !== r.base_zone && (
                      <span style={{ fontSize: '14px', color: '#64748b' }}>{r.gdc_zoning}</span>
                    )}
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

            {/* Proposed Use Check */}
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
              </Card>
            )}

            {/* Permitted Uses */}
            {r.land_uses && !r.requires_manual_review && (
              <Card title={`Permitted Uses — ${r.base_zone}`}>
                {r.land_uses.permitted_by_right?.length > 0 && (
                  <>
                    <div style={styles.sectionLabel}>✓ By Right</div>
                    <ul style={styles.useList}>
                      {r.land_uses.permitted_by_right.map(u => (
                        <li key={u} style={styles.useItem}>
                          <span style={{ color: GREEN, fontSize: '10px' }}>●</span> {u}
                        </li>
                      ))}
                    </ul>
                  </>
                )}
                {r.land_uses.requires_sup?.length > 0 && (
                  <>
                    <div style={{ ...styles.sectionLabel, marginTop: '16px' }}>⚠ Requires SUP</div>
                    <ul style={styles.useList}>
                      {r.land_uses.requires_sup.map(u => (
                        <li key={u} style={{ ...styles.useItem, color: '#92400e' }}>
                          <span style={{ color: YELLOW, fontSize: '10px' }}>●</span> {u}
                        </li>
                      ))}
                    </ul>
                  </>
                )}
                {r.land_uses.special_standards?.length > 0 && (
                  <>
                    <div style={{ ...styles.sectionLabel, marginTop: '16px' }}>★ Special Standards</div>
                    <ul style={styles.useList}>
                      {r.land_uses.special_standards.map(u => (
                        <li key={u} style={{ ...styles.useItem, color: '#1e40af' }}>
                          <span style={{ color: '#93c5fd', fontSize: '10px' }}>●</span> {u}
                        </li>
                      ))}
                    </ul>
                  </>
                )}
              </Card>
            )}

            {/* AI Analysis */}
            {r.ai_analysis && (
              <Card title="Pre-Application Staff Analysis" fullWidth accent={ACCENT}>
                <div style={styles.grid}>
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

            {/* Disclaimer */}
            <div style={styles.disclaimer}>
              ✓ Results appear subject to staff review and do not constitute zoning approval or compliance
              determination. Verify all information with Garland Planning & Development staff before
              submitting permit applications. 972-205-2500.
            </div>

          </div>
        )}
      </main>
    </div>
  )
}