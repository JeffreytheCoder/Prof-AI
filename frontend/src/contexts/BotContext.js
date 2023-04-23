import { createContext, useState } from 'react';

const ROOT_URL = 'http://localhost:8000';

const initialState = {
  slides: new Blob(),
  transcripts: [],
};

const BotContext = createContext({
  ...initialState,
  getSlides: (formData) => null,
});

export const BotProvider = (props) => {
  const { children } = props;
  const [slides, setSlides] = useState(new Blob());
  const [transcripts, setTranscripts] = useState([]);

  const getSlides = async (formData) => {
    const res = await fetch(`${ROOT_URL}/slides`, {
      headers: {
        'Content-Type': 'application/json',
      },
      method: 'POST',
      body: formData,
    });

    if (res.status !== 200) {
      throw new Error('fileToSlides returned an error');
    }

    const blob = await res.blob();
    setSlides(blob);
  };

  return (
    <BotContext.Provider
      value={{
        slides,
        transcripts,
        getSlides,
      }}
    >
      {children}
    </BotContext.Provider>
  );
};

export default BotContext;
