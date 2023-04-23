import React, { useState } from 'react';
import { Box, Button, Typography, LinearProgress, Divider } from '@mui/material';
import { CloudUpload as CloudUploadIcon } from '@mui/icons-material';
import { DropzoneArea } from 'material-ui-dropzone';
import useBot from '../hooks/useBot';
import PsychologyRoundedIcon from '@mui/icons-material/PsychologyRounded';
import Face2RoundedIcon from '@mui/icons-material/Face2Rounded';
import { useNavigate } from 'react-router-dom';

const ROOT_URL = 'http://localhost:8000';

const Upload = () => {
  const { uploadFile, getSlides, getTranscripts, slides, transcripts } = useBot();
  const [file, setFile] = useState(null);
  const [trained, setTrained] = useState(false)
  const [progress, setProgress] = useState(0)
  const navigate = useNavigate();

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

  const train = async () => {
    console.log("start training!")
    console.log(file)
    if (file) {
      try {
        const uploaded = await uploadFile(file);
        setProgress(20);
        console.log(uploaded)
        if (uploaded) {
          const slides = await getSlides()
          console.log(slides)
          setProgress(60);

          const transcripts = await getTranscripts()
          console.log(transcripts)
          setProgress(100);

          if (slides && transcripts) {
            setTrained(true)
          }
        } else {
          console.log("shit")
        }
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    }
  };

  const goToClassroom = async () => {
    if (trained) {
      navigate('/classroom')
    } else {
      console.error("Not trained")
    }
  }

  return (
    <Box display="flex" flexDirection="column" alignItems="center">
      <Typography variant="h4" fontWeight="600">Turn any textbook into your personal AI professor 👩‍🏫</Typography>
      <Box my={5} mb={3} style={{width: '60%', color: "grey"}}>
        <DropzoneArea
          onChange={handleChange}
          acceptedFiles={['application/pdf', 'text/*']}
          maxFileSize={5000000}
          filesLimit={1}
          showPreviews={false}
          dropzoneText={"Drag & drop or click here to upload your textbook (in PDF)"}
          fullWidth={true}
          color="grey"
          style={{fontSize: '16px', width: '80%', color: 'grey'}}
        />
      </Box>
      <Button
        variant="contained"
        color="primary"
        onClick={() => train()}
        startIcon={<PsychologyRoundedIcon />}
        disabled={!file}
      >
        Train
      </Button>
      <Box mt={4} mb={2} width="100%" display="flex" justifyContent="center">
        <Divider style={{width:'50%'}} />
      </Box>
      <Box my={2} mb={4} width="40%" >
        <Typography variant="h6" fontWeight="600">Training progress</Typography>
        <Box mt={2} mb={1}>
          <LinearProgress variant="determinate" value={progress} fullWidth />
        </Box>
        <Typography variant="body2" color="grey">
          {progress == 0 ? "Waiting for you to upload your textbook..." :
          (progress < 20 ? "Uploading you textbook..." : 
          (progress < 60 ? "Generating slides from your textbook..." 
            : "Making your AI professor talk..."))}
        </Typography>
      </Box>
      <Button
        variant="contained"
        color="primary"
        onClick={() => goToClassroom()}
        startIcon={<Face2RoundedIcon />}
        disabled={!trained}
      >
        See your AI professor
      </Button>
    </Box>
  );
};

export default Upload;
