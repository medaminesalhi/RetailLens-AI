import React, { useState } from 'react';

// Only finite downloadable video files, not endless camera streams.
export default function VideoFromIP({ onVideoReady }) {
  const [url, setUrl] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  async function load() {
    setBusy(true);
    setError('');
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 20000);
    try {
      const parsed = new URL(url);
      if (!['http:', 'https:'].includes(parsed.protocol)) throw new Error('URL HTTP(S) requise.');
      const ext = parsed.pathname.split('.').pop().toLowerCase();
      if (!['mp4', 'webm', 'avi', 'mov', 'mkv'].includes(ext)) throw new Error('Utilisez un fichier vidéo, pas un flux continu.');
      const response = await fetch(parsed.href, { signal: controller.signal });
      if (!response.ok || !response.body) throw new Error('Vidéo inaccessible.');
      const reader = response.body.getReader();
      const chunks = [];
      let size = 0;
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        size += value.byteLength;
        if (size > 100 * 1024 * 1024) {
          await reader.cancel();
          throw new Error('Vidéo supérieure à 100 Mio.');
        }
        chunks.push(value);
      }
      onVideoReady(new File(chunks, `remote.${ext}`, { type: response.headers.get('Content-Type') || 'video/mp4' }));
    } catch (err) {
      setError(err.message);
    } finally {
      clearTimeout(timeout);
      setBusy(false);
    }
  }

  return (
    <div className="bg-white p-6 rounded-xl shadow w-full max-w-md">
      <h3>Vidéo depuis une URL</h3>
      <input aria-label="URL vidéo" type="url" value={url} onChange={e => setUrl(e.target.value)} placeholder="http://192.168.1.100/video.mp4" className="w-full border p-2 my-2" />
      <button disabled={busy || !url} onClick={load} className="bg-green-600 text-white p-2 rounded">{busy ? 'Chargement…' : 'Charger la vidéo'}</button>
      {error && <p role="alert">{error}</p>}
    </div>
  );
}
