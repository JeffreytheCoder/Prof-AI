import React, { useState, useEffect } from "react";
import useBot from "../hooks/useBot";

const Videos = ({ transcripts, pageNum, nextPage }) => {
    const [videoIds, setVideoIds] = useState([]);
    const [videoAvailable, setVideoAvailable] = useState(false);
    const [videoURL, setVideoURL] = useState('');

    const getVideoIds = async () => {
        const videoIds = await Promise.all(transcripts.map(async (string) => {
            return await getVideoId(string);
        }));
        setVideoIds(videoIds);
    };

    useEffect(() => {
        if (transcripts.length > 0 && videoIds.length == 0) {
            getVideoIds();
        }
    }, [transcripts]);

    useEffect(() => {

    }, [videoIds])

    // const didKey = 'aGFvYm8xMDA4OUBnbWFpbC5jb20:7fGvQp8mX-XEzDMEFP4Ux'; // TESTING
    const didKey = 'amVmZnJleXplcGVuZ3l1QGcudWNsYS5lZHU:w-3Rvjr6nxt_vgPaBjVt9'; 
    const headers = {
        'Authorization': 'Basic ' + didKey,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    };
    const url = 'https://api.d-id.com/talks/';

    const getVideoId = async (string) => {
        const body = JSON.stringify({
            'source_url': 'https://create-images-results.d-id.com/google-oauth2%7C109372526500030115554/upl__E2nJb-Lv5Eln48TnI1Mf/image.jpeg',
            'script': {
                'type': 'text',
                'input': string,
                'provider': {
                    'type': 'microsoft',
                    'voice_id': 'en-US-ChristopherNeural',
                }
            },
            'config': { 'stitch': true }
        });
        return await fetch(url, {
            method: 'POST',
            headers: headers,
            body: body,
        })
            .then(res => res.json())
            .then(data => {
                // return data.id; 
                // TESTING
                if (string === transcripts[0])
                    return 'tlk_AkI7t_SHzCxWwktplRgAd'; 
                else if (string === transcripts[1])
                    return 'tlk_HMvJBSTU2ZR6_Dv1ssTyJ'; 
                else if (string === transcripts[2])
                    return 'tlk_rEOHC4V4UfOBkE5qphRe9';
                else if (string === transcripts[3])
                    return 'tlk_seMe2OGBCSv5ldIlm9ikC';
                else if (string === transcripts[4])
                    return 'tlk_At5xwd902YE5vfsEh7HP9';
                // TESTING
            })
            .catch(err => console.log(err));
    };

    if (pageNum <= videoIds.length) {
        const id = videoIds[pageNum];
        // let interval = setInterval(() => {
            fetch(url + id, {
                method: 'GET',
                headers: headers,
            })
                .then(res => res.json())
                .then(data => {
                    if (data.result_url !== undefined) {
                        // console.log(data);
                        setVideoURL(data.result_url);
                        setVideoAvailable(true);
                        // clearInterval(interval);
                    }
                })
                .catch(err => console.log(err));
        // }, 1000);
    }


    const handleVideoClick = (event) => {
        event.target.play();
    };

    const handleVideoEnded = (event) => {
        nextPage();
    };

    return (
        <div>
            {videoAvailable &&
                <video autoPlay={true} style={{ height: '100%', width: '80%' }} src={videoURL} onClick={handleVideoClick} onEnded={handleVideoEnded}>
                    <source type="video/mp4" />
                </video>
            }
        </div>
    );
};

export default Videos;