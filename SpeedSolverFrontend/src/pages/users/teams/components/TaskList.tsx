import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { ChevronRight, ChevronDown, Plus, X } from 'lucide-react';
import Card from '@/components/card/Card';

interface TaskAuthor {
  id: string;
  profile: {
    fullname: string;
  };
}

interface Task {
  id: string;
  title: string;
  description: string;
  created_at: string;
  deadline_date: string;
  author: TaskAuthor;
  child_objectives: Task[];
  parent_objectiveId: string | null;
}

interface TaskListProps {
  selectedProject: {
    id: string;
    title: string;
  };
  projectTasks: Task[];
  setSelectedProject: (project: any) => void;
  setSelectedTaskId: (taskId: string) => void;
  setIsSubtaskDialogOpen: (isOpen: boolean) => void;
}

const TaskList = ({ selectedProject, projectTasks, setSelectedProject, setSelectedTaskId, setIsSubtaskDialogOpen }: TaskListProps) => {
  const [expandedTasks, setExpandedTasks] = useState<{ [key: string]: boolean }>({});

  const toggleTaskExpansion = (taskId: string) => {
    setExpandedTasks(prev => ({
      ...prev,
      [taskId]: !prev[taskId]
    }));
  };

  const renderTasks = (tasks: Task[], level = 0) => {
    return (
      <div className={`ml-${level * 4}`}>
        {tasks.map(task => (
          <div key={task.id} className="mb-2">
            <div
              className="flex items-center p-2 bg-neutral-700 rounded cursor-pointer hover:bg-neutral-600"
              onClick={() => toggleTaskExpansion(task.id)}
            >
              {expandedTasks[task.id] ? <ChevronDown className="w-4 h-4 mr-2" /> : <ChevronRight className="w-4 h-4 mr-2" />}
              <div className="flex-1">
                <h3 className="font-medium">{task.title}</h3>
                <p className="text-sm text-gray-300">{task.description}</p>
                <div className="flex gap-4 mt-1 text-xs text-gray-400">
                  <p>Автор: {task.author.profile.fullname}</p>
                  <p>Создано: {new Date(task.created_at).toLocaleDateString()}</p>
                  <p>Срок: {new Date(task.deadline_date).toLocaleDateString()}</p>
                </div>
              </div>
              <Button
                onClick={(e) => {
                  e.stopPropagation();
                  setSelectedTaskId(task.id);
                  setIsSubtaskDialogOpen(true);
                }}
                className="bg-green-600 hover:bg-green-700"
                size="sm"
              >
                <Plus className="w-4 h-4 mr-1" />
              </Button>
            </div>
            {expandedTasks[task.id] && task.child_objectives.length > 0 && (
              <div className="ml-4 my-2 border-l border-neutral-600">
                {renderTasks(task.child_objectives, level + 1)}
              </div>
            )}
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="mt-6">
      <Card>
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-white text-lg font-semibold">Задачи {selectedProject.title}</h2>
          <Button
            onClick={() => setSelectedProject(null)}
            className="bg-transparent hover:bg-neutral-700"
          >
            <X/>
          </Button>
        </div>
        <div className="space-y-2">
          {projectTasks.length > 0 ? (
            <div className="text-white">
              {renderTasks(projectTasks)}
            </div>
          ) : (
            <p className="text-center text-gray-400">Нет задач</p>
          )}
        </div>
      </Card>
    </div>
  );
};

export default TaskList;
