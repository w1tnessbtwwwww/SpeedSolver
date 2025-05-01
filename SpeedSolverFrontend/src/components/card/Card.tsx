import { ReactNode } from 'react';

const Card = ({
  children,
  className = '',
  style
}: {
  children: ReactNode;
  className?: string;
  style?: "highlight";
}) => {
  const baseClass = "flex flex-col w-full p-6 gap-5 rounded-[12px] border transition-all duration-700 ease-in-out";
  const defaultStyle = "bg-[#0a0a0a] border-[#818181]";
  
  const highlightStyle = `
    bg-[linear-gradient(90deg,_#0a0a0a_70%,_#8F297A_100%)]
    bg-[length:200%_100%]
    bg-[position:0%_0%]
    hover:bg-[position:100%_0%]
    border-[#818181]
    hover:border-[#8F297A]
  `;

  const combinedClass = `${baseClass} ${style === "highlight" ? highlightStyle : defaultStyle} ${className}`;

  return (
    <div className={combinedClass}>
      {children}
    </div>
  );
};

export default Card;
