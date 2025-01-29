import React from "react"
import "./PrimaryButton.css"

export const PrimaryButton: React.FC<{ text: string, onClick?: () => void }> = ({ text, onClick }) => {
    return (
        <button className="primaryButton" onClick={onClick}>
            {text}
        </button>
    )    
}