import './App.css';
import Slides from './components/Slides';
import ButtonAppBar from "./components/Navbar"
import React from 'react';
import {AppBar, Container, IconButton, Box, Paper} from "@mui/material";

function App() {
  return (
      <div>
          <ButtonAppBar></ButtonAppBar>
          <Paper>
              <Slides />
          </Paper>
          <Container>
          </Container>
      </div>

  );
}

export default App;
