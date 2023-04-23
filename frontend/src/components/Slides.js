import React, { useEffect, useState } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import 'react-pdf/dist/esm/Page/TextLayer.css';
import { Button, IconButton } from "@mui/material";
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
    <div className="App" align="center">
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
              <IconButton size="large" color="inherit"
                          disabled={pageNumber <= 1} onClick={() => {
                previousPage();
              }}>
                <KeyboardArrowLeftRounded />
              </IconButton>
              <IconButton size="large" color="inherit"
                          disabled={numPages ? pageNumber >= numPages : true}
                          onClick={nextPage}
              >
                <KeyboardArrowRightRounded />
              </IconButton>
          </Document>
    </div>
  );
};

export default Slides;
