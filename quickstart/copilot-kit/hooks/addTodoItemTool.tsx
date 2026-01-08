import { useFrontendTool } from "@copilotkit/react-core";

export function useAddTodoItemTool(
    todos: string[],
    setTodos: (todos: string[]) => void
) {
    useFrontendTool({
        name: "addTodoItem",
        description: "Add a new todo item to the list",
        parameters: [
            {
                name: "todoText",
                type: "string",
                description: "The text of the todo item to add",
                required: true,
            },
        ],
        handler: async ({ todoText }) => {
            console.log("adding todo...")
            console.log(todoText)
            setTodos([...todos, todoText]);
        },
    });
}