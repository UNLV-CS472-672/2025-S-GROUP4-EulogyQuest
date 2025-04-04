import React, { useState } from "react";
import axios from "axios";
import { Router, Routes } from "react-router-dom";
import SubNavBar from "./SubNavBar";

function Generatequest() {
    const [questPrompt, setQuestPrompt] = useState("");
    const [response, setResponse] = useState("");
    const [ret, setRet] = useState(false);
    
    const handleSubmit = async () => {
        try {
            // return quest promp to server
            const response = await axios.post("http://localhost:5000/generate-quest", {
                message: questPrompt,
            });
            // log the response from the server
            console.log("Server response:", response.data);
            setRet(true); 
            setResponse("Prompt sent successfully!");

        } catch (error) {
            console.error("Error sending prompt:", error);
            setRet(false);
            setResponse("Error sending prompt. Please try again");
        }
    };

    return (
        
        <div>
            <SubNavBar />
        </div>
    );
}

export default Generatequest;
