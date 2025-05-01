import { useState, useRef, forwardRef, useImperativeHandle } from "react";
import { Eye, EyeClosed } from 'lucide-react';
import styles from './PasswordInput.module.css';

export interface PasswordInputRef {
  value: string;
  focus: () => void;
}

const PasswordInput = forwardRef<PasswordInputRef, React.InputHTMLAttributes<HTMLInputElement>>((props, ref) => {
  const [showPassword, setShowPassword] = useState(false);
  const [isFocused, setIsFocused] = useState(false);
  const inputField = useRef<HTMLInputElement>(null);

  const toggleShowPassword = (e: React.MouseEvent) => {
    e.preventDefault();
    setShowPassword(c => !c);
  };

  const handleFocus = () => {
    setIsFocused(true);
  };

  const handleBlur = () => {
    setIsFocused(false);
  };

  useImperativeHandle(ref, () => ({
    get value() {
      return inputField.current ? inputField.current.value : '';
    },
    focus() {
      if (inputField.current) {
        inputField.current.focus();
      }
    },
  }));

  return (
    <div className={`${styles.container} border-2 ${isFocused ? 'border-[gray]' : ''}`}>
      <input
        {...props}
        ref={inputField}
        className="!border-none"
        type={showPassword ? 'text' : 'password'}
        placeholder="Пароль"
        onFocus={handleFocus}
        onBlur={handleBlur}
      />
      <button type="button" onClick={toggleShowPassword}>
        {showPassword ? <Eye /> : <EyeClosed />}
      </button>
    </div>
  );
});

export default PasswordInput;