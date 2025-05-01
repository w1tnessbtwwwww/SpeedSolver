import { useState, useEffect } from "react"

const MOBILE_BREAKPOINT = 768

export function useBreakpoint(breakpoint = MOBILE_BREAKPOINT) {
  const [isMobile, setIsMobile] = useState<boolean>(false)

  useEffect(() => {
    const mql = window.matchMedia(`(max-width: ${breakpoint - 1}px)`)
    
    const onChange = () => {
      setIsMobile(window.innerWidth < breakpoint)
    }
    
    mql.addEventListener("change", onChange)
    setIsMobile(window.innerWidth < breakpoint)
    
    return () => mql.removeEventListener("change", onChange)
  }, [breakpoint])

  return isMobile
}