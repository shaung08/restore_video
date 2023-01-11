import React from 'react'
import Cropper from 'react-easy-crop'

function CropVideo({bbox, videosrc, crop, rotation, zoom, setCrop, setRotation, onCropComplete, setZoom}) {
  return (
    <div>
      <div>
        <Cropper
          video={videosrc}
          crop={crop}
          rotation={rotation}
          zoom={zoom}
          aspect={bbox}
          onCropChange={setCrop}
          onRotationChange={setRotation}
          onCropComplete={onCropComplete}
          onZoomChange={setZoom}
        />
      </div>
    </div>
  )
}

export default CropVideo; 