import { ReactNode } from "react"
import { NavLink } from "react-router-dom"

const NavButton = ({to, children}:{to:string, children:ReactNode}) => {


  return (
    <NavLink
          to={to}
          className={({ isActive }) =>
            isActive ? 'text-white px-4 py-1 bg-black rounded-t-xl transition-[1s]' :
          'text-white px-4 py-1 hover:bg-neutral-700 hover:rounded-full transition-[1s]'}
        >
          {children}
    </NavLink>
  )
}

export default NavButton