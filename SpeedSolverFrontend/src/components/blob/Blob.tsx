// components/blob/Blob.tsx
import { useEffect, useRef } from 'react';
import styles from './styles.module.css';

interface BlobProps {
  size?: number;
}

export const Blob: React.FC<BlobProps> = ({ size = 300 }) => {
  const blobRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const blob = blobRef.current;
    if (!blob) return;

    const handleMouseMove = (e: MouseEvent) => {
      const { clientX: x, clientY: y } = e;
      blob.style.left = `${x}px`;
      blob.style.top = `${y}px`;
    };

    window.addEventListener('mousemove', handleMouseMove);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);

  return (
    <div
      ref={blobRef}
      className={styles.Blob}
      style={{
        position: 'fixed',
        transform: 'translate(-50%, -50%)',
        pointerEvents: 'none',
        '--blob-size': `${size}px`,
      } as React.CSSProperties}
    />
  );
};
