import { ReactNode } from "react"
import { NavLink } from "react-router-dom"

const NavButton = ({to, children, className}:{to:string, children:ReactNode, className?:string}) => {


  return (
    <NavLink
          to={to}
          className={({ isActive }) =>
            isActive ? `text-white pb-2 px-4 py-1 bg-black rounded-t-xl transition-[1s] ${className}` :
          `text-white px-6 py-1 my-1 hover:bg-neutral-700 hover:rounded-full transition-[1s] ${className}`}
        >
          {children}
    </NavLink>
  )
}

export default NavButton