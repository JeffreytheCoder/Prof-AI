import React, { useEffect, useState } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import 'react-pdf/dist/esm/Page/TextLayer.css';
import {Button, IconButton, Container, Grid} from "@mui/material";
import { KeyboardArrowLeftRounded, KeyboardArrowRightRounded }from '@mui/icons-material';
import "../App.css"


const Slides = () => {
  useEffect(() => {
    pdfjs.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;
  });

  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [renderedPageNumber, setRenderedPageNumber] = useState(null);

  const isLoading = renderedPageNumber !== pageNumber;

  function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages);
    setPageNumber(1);
  }
  function changePage(offset) {
    setPageNumber(prevPageNumber => prevPageNumber + offset);
  }

  function previousPage() {
    changePage(-1);
  }

  function nextPage() {
    changePage(1);
  }

  return (
      <Container maxWidth="xl">
        <Grid container spacing={1}>
          <Grid item xs={8}>
            <div className="App" align="center" >
              <Document
                  file="/test.pdf"
                  onLoadSuccess={onDocumentLoadSuccess}>
                {isLoading && renderedPageNumber ? (
                    <Page
                        key={renderedPageNumber}
                        pageNumber={renderedPageNumber}
                    />
                ) : null}

                <Page
                    className={`${isLoading ? 'loadingPage' : ''}`}
                    key={pageNumber}
                    pageNumber={pageNumber}
                    onRenderSuccess={() => setRenderedPageNumber(pageNumber)}
                />
                <p>
                  Page {pageNumber || (numPages ? 1 : "--")} of {numPages || "--"}
                </p>
                <IconButton size="large" style={{color:"#5F64FA"}}
                            disabled={pageNumber <= 1} onClick={() => {
                  previousPage();
                }}>
                  <KeyboardArrowLeftRounded fontSize='large'/>
                </IconButton>
                <IconButton size="large"  style={{color:"#5F64FA"}}
                            disabled={numPages ? pageNumber >= numPages : true}
                            onClick={nextPage}
                >
                  <KeyboardArrowRightRounded fontSize='large'/>
                </IconButton>
              </Document>
            </div>
          </Grid>
          <Grid item xs={4}>
            <div>Second Container</div>
          </Grid>
        </Grid>
      </Container>
  );
};

export default Slides;
