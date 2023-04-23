import Slides from './components/Slides';
import Upload from './components/Upload'
import {Slide} from "@mui/material";

const routes = [
  {
    path: '/',
    children: [
      {
        path: '',
        element: <Upload />,
      },
      {
        path: 'classroom',
        element: <Slides />,
      },
    ],
  },
];

export default routes;
