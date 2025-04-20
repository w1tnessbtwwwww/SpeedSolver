import { Sidebar, SidebarTrigger } from "@/components/sidebar"
import { useState } from "react"


const TestPage = () => {
  const [isSideberOpen, setIsSideberOpen] = useState(false);
  const toggleIsSideberOpen = () => {setIsSideberOpen(!isSideberOpen)}
  return (
    <>
      <Sidebar
        isOpen={isSideberOpen}
        setIsOpen={setIsSideberOpen}
      />
      <SidebarTrigger onClick={toggleIsSideberOpen}>
        <button>
          Open
        </button>
      </SidebarTrigger>
    </>
  )
}

export default TestPage