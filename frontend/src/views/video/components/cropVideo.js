import axios from 'axios'
import ip from '../../../utils/ip';

function getCroppedvideo(bbox, videofile, setFlag) {
    let data = new FormData()
    data.append('file', videofile)
    data.append("filename", "output.mp4")
    data.append("coordinate", JSON.stringify(bbox))
    setFlag(2)
    axios.post(`http://${ip}/api/upload`, data, {
        headers: { 'Content-Type': 'multipart/form-data' }
    }).then(response => {
        setFlag(1)
        console.log(response.data)
    })
}

export default getCroppedvideo;