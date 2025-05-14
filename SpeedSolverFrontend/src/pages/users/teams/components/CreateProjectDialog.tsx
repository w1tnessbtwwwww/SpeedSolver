import { Button } from '@/components/ui/button';
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";

interface CreateProjectDialogProps {
  newProject: {
    title: string;
    description: string;
  };
  setNewProject: (project: { title: string; description: string }) => void;
  setIsDialogOpen: (isOpen: boolean) => void;
  handleCreateProject: () => void;
}

const CreateProjectDialog = ({ newProject, setNewProject, setIsDialogOpen, handleCreateProject }: CreateProjectDialogProps) => {
  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center p-4">
      <div className="bg-neutral-800 text-white rounded-lg p-6 w-full max-w-md">
        <h2 className="text-xl font-semibold mb-4">Создать новый проект</h2>
        <div className="space-y-4">
          <div>
            <label className="block mb-2">Название проекта</label>
            <Input
              value={newProject.title}
              onChange={(e) => setNewProject({ ...newProject, title: e.target.value })}
              className="bg-neutral-700 border-neutral-600 w-full"
            />
          </div>
          <div>
            <label className="block mb-2">Описание</label>
            <Textarea
              value={newProject.description}
              onChange={(e) => setNewProject({ ...newProject, description: e.target.value })}
              className="bg-neutral-700 border-neutral-600 w-full"
            />
          </div>
          <div className="flex justify-end gap-2">
            <Button
              onClick={() => setIsDialogOpen(false)}
              className="bg-gray-600 hover:bg-gray-700"
            >
              Отмена
            </Button>
            <Button
              onClick={handleCreateProject}
              className="bg-blue-600 hover:bg-blue-700"
            >
              Создать
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CreateProjectDialog;
