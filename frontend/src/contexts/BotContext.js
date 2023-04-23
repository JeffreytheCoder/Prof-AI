import { createContext, useState, useEffect } from 'react';

const ROOT_URL = 'http://localhost:8000';

const initialState = {
  file: new Blob(),
  uploaded: false,
  slides: "",
  transcripts: [],
};

const BotContext = createContext({
  ...initialState,
  uploadFile: () => Promise.resolve(),
  getSlides: () => Promise.resolve(),
  getTranscripts: () => Promise.resolve(),
});

export const BotProvider = (props) => {
  const { children } = props;
  const [file, setFile] = useState(new Blob());
  const [uploaded, setUploaded] = useState(false);
  const [slides, setSlides] = useState("");
  const [transcripts, setTranscripts] = useState([]);

  useEffect(() => {
    const slides = localStorage.getItem('slides');
    const transcriptsStr = localStorage.getItem('transcripts');
    // console.log(slides, transcriptsStr); 
    if (slides) {
      setSlides(slides);
    }
    if (transcriptsStr.length > 0) {
      const transcripts = transcriptsStr.split("@@@");
      // console.log(typeof transcripts)
      setTranscripts(transcripts);
    }
    // console.log(slides, transcripts)
  }, [])

  const uploadFile = async (inputFile) => {
    setFile(inputFile);
    const formData = new FormData();
    formData.append('file', inputFile);

    const res = await fetch(`${ROOT_URL}/uploadfile`, {
      method: 'POST',
      body: formData,
    });

    if (res.status !== 200) {
      console.error(res);
      setUploaded(false);
      return false;
    } else {
      setUploaded(true);
      return true;
    }
  };

  const getSlides = async () => {
    const res = await fetch(`${ROOT_URL}/slides`, {
      method: 'GET',
    });

    if (res.status !== 200) {
      throw new Error('fileToSlides returned an error');
    }

    const json = await res.json();
    setSlides(json.content);
    localStorage.setItem('slides', json.content);

    return json.content
  };

  const getTranscripts = async () => {
    const res = await fetch(`${ROOT_URL}/transcripts`, {
      method: 'GET',
    });

    if (res.status !== 200) {
      throw new Error('fileToSlides returned an error');
    }

    const json = await res.json();
    setTranscripts(json.content);
    localStorage.setItem('transcripts', json.content.join("@@@"));

    return json.content
  };

  return (
    <BotContext.Provider
      value={{
        slides,
        transcripts,
        uploaded,
        file,
        uploadFile,
        getTranscripts,
        getSlides,
      }}
    >
      {children}
    </BotContext.Provider>
  );
};

export default BotContext;
