import React from 'react';

const VideoUploader = ({ onVideoReady }) => {

  const handleVideoChange = (e) => {
    const file = e.target.files[0];
    onVideoReady(file);
  };

  return (
    <div className="bg-white border rounded-xl p-6 shadow w-full max-w-md mx-auto">
      <h3 className="text-lg font-medium mb-4">📁 Uploader un fichier vidéo</h3>
      <input
        type="file"
        accept="video/*"
        onChange={handleVideoChange}
        className="w-full border px-4 py-2 rounded"
      />
    </div>
  );
};

export default VideoUploader;
