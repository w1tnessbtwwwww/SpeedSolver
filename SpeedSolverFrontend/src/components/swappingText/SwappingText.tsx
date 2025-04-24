import { useEffect, useState, useMemo } from 'react';
import { useSpring, animated } from 'react-spring';
import './TextStyles.css';

const AnimatedText = ({strings}:{strings:string[]}) => {
  const [text, setText] = useState('');
  const [index, setIndex] = useState(0);

  const texts = useMemo(() => strings, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setIndex((prevIndex) => (prevIndex + 1) % texts.length);
    }, 1500);

    return () => clearInterval(interval);
  }, [texts.length]);

  useEffect(() => {
    setText(texts[index]);
  }, [index, texts]);

  const springProps = useSpring({
    opacity: 1, // Changed from 0.6 to 1
    from: { opacity: 0 },
    config: { duration: 800 }, // Slightly faster animation
    reset: true,
  });

  return (
    <animated.div style={springProps} className="relative z-10"> {/* Added z-index and relative positioning */}
      <h1 className='welcome-text'>{text}</h1>
    </animated.div>
  );
};

export default AnimatedText;
