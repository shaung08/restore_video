import React from "react";

import Button from '@material-ui/core/Button'
import Box from '@material-ui/core/Box';
import ButtonGroup from '@material-ui/core/ButtonGroup';

import downloadVideo from './components/downloadVideo';
import getCroppedvideo from './components/cropVideo';

function Bbox ({set, setFlag, croppedAreaPixels, videofile}) {
  
  const buttons = [
      <Button
        onClick={() => (set(1/1.91))}
      >
        1:1.91
      </Button>,
      <Button
        onClick={() => set(16/9)}
      >
        9: 16
      </Button>,
      <Button
      onClick={() => getCroppedvideo(croppedAreaPixels, videofile, setFlag)}
      >
      crop vidoe
      </Button>,
      <Button
        onClick={downloadVideo}
      >
         download
      </Button>
  ];

    return  (
      <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        '& > *': {
          m: 1,
        },
      }}
    >

      <ButtonGroup size="large" aria-label="large button group">
        {buttons}
      </ButtonGroup>
    </Box>

    )
}

export default Bbox;