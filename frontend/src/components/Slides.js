import React, { useEffect, useState } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import 'react-pdf/dist/esm/Page/TextLayer.css';
import { Button, IconButton } from "@mui/material";
import { KeyboardArrowLeftRounded, KeyboardArrowRightRounded }from '@mui/icons-material';


const options = {
  cMapUrl: 'cmaps/',
  standardFontDataUrl: 'standard_fonts/',
};

const Slides = () => {
  useEffect(() => {
    pdfjs.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;
  });

  const [numPages, setNumPages] = useState();
  const [pageNumber, setPageNumber] = useState(1);
  const [file, setFile] = useState('/test.pdf');
  function onFileChange(event) {
    const { files } = event.target;

    if (files && files[0]) {
      setFile(files[0] || null);
    }
  }
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
            file={file}
            onLoadSuccess={onDocumentLoadSuccess}
            options={options}
          >
            <Page pageNumber={pageNumber}>
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
            </Page>
          </Document>
    </div>
  );
};

export default Slides;
