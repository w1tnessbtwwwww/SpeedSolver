import { Button } from '@/components/ui/button';
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";

interface CreateSubtaskDialogProps {
  newSubtask: {
    title: string;
    description: string;
    deadline_date: string;
  };
  setNewSubtask: (subtask: { title: string; description: string; deadline_date: string }) => void;
  setIsSubtaskDialogOpen: (isOpen: boolean) => void;
  handleCreateSubtask: () => void;
  selectedTaskId: string | null;
}

const CreateSubtaskDialog = ({ newSubtask, setNewSubtask, setIsSubtaskDialogOpen, handleCreateSubtask, selectedTaskId }: CreateSubtaskDialogProps) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
      <div className="bg-neutral-800 text-white rounded-lg p-6 w-full max-w-md">
        <h2 className="text-xl font-semibold mb-4">
          {selectedTaskId ? 'Создать подзадачу' : 'Создать задачу'}
        </h2>
        <div className="space-y-4 mt-4">
          <div>
            <label className="block mb-2">Название подзадачи <span className="text-red-500">*</span></label>
            <Input
              value={newSubtask.title}
              onChange={(e) => setNewSubtask({ ...newSubtask, title: e.target.value })}
              className="bg-neutral-700 border-neutral-600 w-full"
              required
            />
          </div>
          <div>
            <label className="block mb-2">Описание <span className="text-red-500">*</span></label>
            <Textarea
              value={newSubtask.description}
              onChange={(e) => setNewSubtask({ ...newSubtask, description: e.target.value })}
              className="bg-neutral-700 border-neutral-600 w-full"
              required
            />
          </div>
          <div>
            <label className="block mb-2">Срок выполнения <span className="text-red-500">*</span></label>
            <Input
              type="datetime-local"
              value={newSubtask.deadline_date}
              onChange={(e) => setNewSubtask({ ...newSubtask, deadline_date: e.target.value })}
              className="bg-neutral-700 border-neutral-600 w-full"
              required
            />
            <p className="text-xs text-gray-400 mt-1">
              Время будет сохранено в формате GMT
            </p>
          </div>
          <div className="flex justify-end gap-2">
            <Button
              onClick={() => setIsSubtaskDialogOpen(false)}
              className="bg-gray-600 hover:bg-gray-700"
            >
              Отмена
            </Button>
            <Button
              onClick={() => {
                if (!newSubtask.title.trim()) {
                  alert('Введите название задачи');
                  return;
                }
                if (!newSubtask.description.trim()) {
                  alert('Введите описание задачи');
                  return;
                }
                if (!newSubtask.deadline_date) {
                  alert('Укажите срок выполнения');
                  return;
                }
                handleCreateSubtask();
              }}
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

export default CreateSubtaskDialog;
