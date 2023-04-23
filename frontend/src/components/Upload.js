import React, { useState } from 'react';
import { Box, Button } from '@mui/material';
import { CloudUpload as CloudUploadIcon } from '@mui/icons-material';
import { DropzoneArea } from 'material-ui-dropzone';
import useBot from '../hooks/useBot';

const ROOT_URL = 'http://localhost:8000';

const Upload = () => {
  const { uploadFile, getSlides, getTranscripts } = useBot();
  const [file, setFile] = useState(null);

  const handleChange = (files) => {
    console.log(files)
    setFile(files[0]);
  };

  const uploadfile = async () => {
    const formData = new FormData();
    formData.append('file', file);

    const res = await fetch(`${ROOT_URL}/uploadfile`, {
      method: 'POST',
      body: formData,
    });
    console.log(res)

    if (res.status !== 200) {
      console.error(res);
      // setUploaded(false);
      return false;
    } else {
      // setUploaded(true);
      return true;
    }
  };

  const handleUpload = async () => {
    console.log(file)
    if (file) {
      try {
        const uploaded = await uploadFile(file);
        console.log(uploaded)
        if (uploaded) {
          const slides = await getSlides()
          console.log(slides)
          const transcripts = await getTranscripts()
          console.log(transcripts)
        } else {
          console.log("shit")
        }
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    }
  };

  return (
    <Box>
      <DropzoneArea
        onChange={handleChange}
        acceptedFiles={['application/pdf', 'text/*']}
        maxFileSize={5000000}
        filesLimit={1}
        showPreviews={false}
      />
      <Button
        variant="contained"
        color="primary"
        onClick={() => handleUpload()}
        startIcon={<CloudUploadIcon />}
        disabled={!file}
      >
        Upload
      </Button>
    </Box>
  );
};

export default Upload;
