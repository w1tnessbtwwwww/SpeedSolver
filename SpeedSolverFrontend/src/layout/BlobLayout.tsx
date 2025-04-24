import { Outlet} from 'react-router-dom';
import { Blob } from '@/components/blob/Blob';

const BlobLayout = () => {
  return (
    <>
      <Blob size={5000} />
      <Outlet />
    </>
  );
};

export default BlobLayout;
