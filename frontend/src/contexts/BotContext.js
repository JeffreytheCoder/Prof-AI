import { createContext, useState } from 'react';

const ROOT_URL = 'http://localhost:8000';

const initialState = {
  file: new Blob(),
  uploaded: false,
  slides: new Blob(),
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
  const [slides, setSlides] = useState(new Blob());
  const [transcripts, setTranscripts] = useState([]);

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

    const blob = await res.blob();
    setSlides(blob);

    return blob
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
