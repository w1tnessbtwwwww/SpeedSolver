import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { useForm } from "react-hook-form"
import { create_team } from "@/app/axios_api"
import { Button } from "@/components/ui/button"

const formSchema = z.object({
  title: z.string().min(2, {
    message: "Title must be at least 2 characters.",
  }),
  description: z.string().min(10, {
    message: "Description must be at least 10 characters.",
  }),
  organizationId: z.string().optional(),
})

interface AddTeamFormProps {
  onClose: () => void;
  onSuccess: () => void;
}

const AddTeamForm = ({ onClose, onSuccess }: AddTeamFormProps) => {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      title: "",
      description: "",
      organizationId: undefined,
    },
  })

  async function onSubmit(values: z.infer<typeof formSchema>) {
    try {
      const response = await create_team(values);
      console.log('Team created:', response);
      form.reset();
      onSuccess();
      onClose();
    } catch (error) {
      console.error('Error creating team:', error);
    }
  }

  const handleOverlayClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div 
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
      onClick={handleOverlayClick}
    >
      <div className="w-full max-w-md p-6 bg-[#0a0a0a] rounded-[10px] border-1 border-[#161616]">
        <h1 className="text-2xl font-bold text-white mb-6">Создание новой команды</h1>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            <FormField
              control={form.control}
              name="title"
              render={({ field }) => (
                <FormItem>
                  <FormLabel className="text-white">Название</FormLabel>
                  <FormControl>
                    <Input className="text-white bg-black outline-none" placeholder="DreamTeam" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="description"
              render={({ field }) => (
                <FormItem>
                  <FormLabel className="text-white">Описание</FormLabel>
                  <FormControl>
                    <textarea 
                      className="w-full min-h-[100px] rounded-md border bg-transparent px-3 py-2 text-white border-input"
                      placeholder="Команда мечты" 
                      {...field} 
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <div className="flex justify-end gap-4">
              <Button type="button" variant="outline" onClick={onClose}>
                Отмена
              </Button>
              <Button type="submit">
                Создать
              </Button>
            </div>
          </form>
        </Form>
      </div>
    </div>
  )
}

export default AddTeamForm