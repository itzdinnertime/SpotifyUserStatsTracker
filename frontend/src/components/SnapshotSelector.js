import { useState, useEffect } from 'react';

function SnapshotSelector({ snapshotId, setSnapshotId }) {
    const [snapshots, setSnapshots] = useState([]);

    useEffect(() => {
        fetch('http://localhost:8000/api/stats/snapshots')
        .then(res => res.json())
        .then(data => {
            setSnapshots(data);
            // If no snapshot selected, default to latest
            if (!snapshotId && data.length > 0) {
                setSnapshotId(data[0].id);
            }
        })
        .catch(err => {
            // Handle error if needed
        });
    // Add snapshotId and setSnapshotId to dependencies
    },  [snapshotId, setSnapshotId]);

    return (
        <div style={{ marginBottom: '1rem' }}>
            <label htmlFor="snapshot-select" style={{ marginRight: '0.5rem' }}>
                Snapshot:
            </label>
            <select
                id="snapshot-select"
                value={snapshotId || (snapshots[0] && snapshots[0].id) || ''}
                onChange={e => setSnapshotId(Number(e.target.value))}
                style={{ padding: '0.3rem', borderRadius: '6px' }}
            >
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