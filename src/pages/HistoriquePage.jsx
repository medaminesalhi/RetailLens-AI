// src/pages/HistoriquePage.jsx
import React, { useEffect, useState } from 'react';
import { apiRequest, mediaUrl } from '../api';

export default function HistoriquePage() {
  const [videos, setVideos] = useState([]);
  const [images, setImages] = useState([]);
  const [error, setError] = useState('');

  // Exemple de fetch historique depuis votre API
  useEffect(() => {
    // 1) Récupérer historique images
    apiRequest('history-images/')
      .then(data => setImages(data))
      .catch(err => setError(err.message));

    // 2) Récupérer historique vidéos
    apiRequest('history-videos/')
      .then(data => setVideos(data))
      .catch(err => setError(err.message));
  }, []);

  return (
    <section className="p-8">
      <h2 className="text-2xl font-bold mb-4">📚 Historique</h2>
      {error && <p role="alert" className="text-red-700">{error}</p>}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Colonne Images */}
        <div>
          <h3 className="text-xl mb-2">Images analysées</h3>
          {!images.length && !error && <p>Aucune image à afficher.</p>}
          {images.map((img, i) => (
            <div key={img.id || i} className="mb-4 p-4 bg-gray-50 rounded shadow">
              <img src={mediaUrl(img.image_path)} alt="Image analysée" className="w-full rounded" />
              <p><strong>Catégories :</strong> {img.categories.join(', ')}</p>
              <p><strong>OCR :</strong> {img.ocr_text.join(', ')}</p>
            </div>
          ))}
        </div>

        {/* Colonne Vidéos */}
        <div>
          <h3 className="text-xl mb-2">Vidéos analysées</h3>
          {!videos.length && !error && <p>Aucune vidéo à afficher.</p>}
          {videos.map((vid, i) => (
            <div key={vid.id || i} className="mb-6 p-4 bg-gray-50 rounded shadow">
              <video src={mediaUrl(vid.video_url)} controls className="w-full rounded mb-2" />
              {vid.truncated && <p>Analyse partielle (120 images maximum).</p>}
              <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                {vid.frames.map((f, j) => (
                  <div key={j}>
                    <img src={mediaUrl(f.frame)} alt={`Frame ${j}`} className="w-full rounded" />
                    <p className="text-sm"><strong>{f.yolo.join(', ')}</strong></p>
                    <p className="text-xs">{f.ocr.join(', ')}</p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
