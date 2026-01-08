"use client";

import { useState } from "react";
import { CopilotChat } from "@copilotkit/react-ui";
import { useAddTodoItemTool } from "@/hooks/addTodoItemTool";

export default function SLChat() {
    const [todos, setTodos] = useState<string[]>([]);
    useAddTodoItemTool(todos, setTodos);

    return (
        <CopilotChat
            instructions={"You are assisting the user as best as you can. Answer in the best way possible given the data you have."}
            labels={{
                title: "Your Assistant",
                initial: "Hi! 👋 How can I assist you today?",
            }}
        />
    );
}
