import React, { useEffect, useState, useMemo } from 'react';
import { useSpring, animated } from 'react-spring';
import './TextStyles.css';

const AnimatedText: React.FC = () => {
  const [text, setText] = useState('');
  const [index, setIndex] = useState(0);

  // Используем useMemo для мемоизации массива texts
  const texts = useMemo(() => ['создавайте организации.', 'создавайте команды.', 'распределяйте задачи.', 'планируйте сроки.'], []);

  useEffect(() => {
    const interval = setInterval(() => {
      setIndex((prevIndex) => (prevIndex + 1) % texts.length);
    }, 1500); // Меняйте текст каждые 1.5 секунды

    return () => clearInterval(interval);
  }, [texts.length]);

  useEffect(() => {
    setText(texts[index]);
  }, [index, texts]);

  const springProps = useSpring({
    opacity: 0.6,
    from: { opacity: 0 },
    config: { duration: 1000 },
    reset: true,
  });

  return (
    <animated.div style={springProps}>
      <h1 className='welcome-text'>{text}</h1>
    </animated.div>
  );
};

export default AnimatedText;
