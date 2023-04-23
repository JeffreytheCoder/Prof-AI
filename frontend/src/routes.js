import Slides from './components/Slides';
import Upload from './components/Upload'

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
