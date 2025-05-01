import {X} from 'lucide-react'
import { ReactNode } from 'react';
import { useBreakpoint } from '@/hooks/use-breackpoint';

const Sidebar = ({ isOpen, setIsOpen,className, children }: {
    isOpen: boolean;
    setIsOpen: React.Dispatch<React.SetStateAction<boolean>>;
    className?: string;
    children?: ReactNode
}) => {

    const isMobile = useBreakpoint();

    return (
        <div className={`
            w-[300px] bg-[#0a0a0a] h-full fixed top-0 p-6 flex flex-col 
            transition-all duration-450 ease-in-out ${className} z-10
            ${isMobile ? "w-screen" : "w-[300px] rounded-r-2xl border-y-1 border-r-1  border-[#818181]"}
            ${isOpen ? "left-0" : isMobile ? "-left-[100vw]" : "-left-[300px]"}
        `}>
            <button 
                onClick={() => setIsOpen(false)}
                className="absolute top-6 right-6"
            >
                <X color='#818181'/>
            </button>

            {children}
        </div>
    );
};

const SidebarTrigger = ({ onClick, children }: { 
    onClick: React.MouseEventHandler<HTMLButtonElement>,
    children: ReactNode
}) => {
    return (
        <button onClick={onClick}>
            {children}
        </button>
    );
};

// Правильный экспорт
export { Sidebar, SidebarTrigger };