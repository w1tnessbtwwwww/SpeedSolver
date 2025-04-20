import React, { ReactNode } from 'react'

const Card = ({children, className}:{children:ReactNode, className?:string}) => {
  return (
    <div className={`flex flex-col bg-[#0a0a0a] border-1 border-[#818181] p-6 gap-5 rounded-[12px] ${className}`}>
        {children}
    </div>
  )
}

export default Card