import axios from 'axios'
import ip from '../../../utils/ip';

function downloadVideo() {
    axios.get(`http://${ip}/api/download`, {responseType: 'blob' }
    ).then(response => {
        let blob = new Blob([response.data], { type: 'application/' })
        let link = document.createElement('a')
        link.href = URL.createObjectURL(blob)
        link.download = "output001.mp4"
        link.click()
        URL.revokeObjectURL(link.href)
    }).catch(error => {
        console.log(error)
    })
}

export default downloadVideo;