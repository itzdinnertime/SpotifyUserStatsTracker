import { useState, useEffect } from 'react';

function SnapshotSelector({ snapshotId, setSnapshotId }) {
    const [snapshots, setSnapshots] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('http://localhost:8000/api/stats/snapshots')
        .then(res => res.json())
        .then(data => {
            setSnapshots(data);
            setLoading(false);
        })
        .catch(err => {
            setLoading(false);
        });
 },  []);

 return (
     <div style={{ marginBottom: '1rem' }}>
      <label htmlFor="snapshot-select" style={{ marginRight: '0.5rem' }}>
        Snapshot:
      </label>
      <select
        id="snapshot-select"
        value={snapshotId || ''}
        onChange={e => setSnapshotId(e.target.value ? Number(e.target.value) : null)}
        style={{ padding: '0.3rem', borderRadius: '6px' }}
      >
        <option value="">Latest</option>
        {snapshots.map(s => (
          <option key={s.id} value={s.id}>
            {s.created_at ? new Date(s.created_at).toLocaleString() : `Snapshot ${s.id}`}
          </option>
        ))}
      </select>
    </div>
  );
}

export default SnapshotSelector;