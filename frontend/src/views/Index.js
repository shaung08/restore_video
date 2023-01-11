import React, { useState, useCallback } from "react";

import CircularProgress from '@material-ui/core/CircularProgress';

import Sidebar from './sidebar/Index';
import Canvas from "./canvas/Index";
import Video from './video/Index';


function Index() {
  const [videofile, setVideofile] = useState(null)
  const [videosrc, setVideosrc] = useState(null)
  const [flag, setFlag] = useState(0)
  const [bbox, setBbox] = useState(1/1.91)
  const [crop, setCrop] = useState({ x: 0, y: 0 })
  const [rotation, setRotation] = useState(0)
  const [zoom, setZoom] = useState(1)
  const [croppedAreaPixels, setCroppedAreaPixels] = useState(null)
  const onCropComplete = useCallback((croppedArea, croppedAreaPixels) => {
    setCroppedAreaPixels(croppedAreaPixels)
  }, [])
  
  const onFileChange = async (e) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0]
      let videoDataUrl = await readFile(file)
      setVideosrc(videoDataUrl)
      setVideofile(file)
      setFlag(1)
    }
  }

  return (
    <>
    <div className="sidebar">
        <Sidebar/>
      </div>
      <div className="main-area">
        { flag===0 ? 
          <div style={{
            display: 'flex', 
            justifyContent: 'center',
            paddingTop: "200px",
            }}>
            <input type="file" onChange={onFileChange} accept=".mov,.mp4" /> 
          </div>
        : flag===1 ?
          <Canvas 
            bbox={bbox} 
            videosrc={videosrc} 
            crop={crop}
            rotation={rotation}
            zoom={zoom}
            setCrop={setCrop}
            setRotation={setRotation}
            onCropComplete={onCropComplete}
            setZoom={setZoom}
          />
        : flag===2 ?
          <div style={{
            display: 'flex', 
            justifyContent: 'center',
            paddingTop: "200px",
            }}>
            <CircularProgress/>
          </div>
        : null
        }
      </div>
      <div className="main-area-bottom">
        { flag===1 ? (
          <Video 
            set={setBbox}
            setFlag={setFlag}
            croppedAreaPixels={croppedAreaPixels} 
            videofile={videofile}
          />
         ) : (
          null
         )}
      </div>
    </>
  );
}

function readFile(file) {
  return new Promise((resolve) => {
    const reader = new FileReader()
    reader.addEventListener('load', () => resolve(reader.result), false)
    reader.readAsDataURL(file)
  })
}

export default Index;
