import React from "react"
import "./PrimaryButton.css"

interface PrimaryButtonProps {
    text: string;
    onClick?: () => void;
    className?: string;
  }

export const PrimaryButton: React.FC<PrimaryButtonProps> = ({ text, onClick, className }) => {
    return (
      <button className={`primaryButton ${className || ''}`} onClick={onClick}>
        {text}
      </button>
    );
  };