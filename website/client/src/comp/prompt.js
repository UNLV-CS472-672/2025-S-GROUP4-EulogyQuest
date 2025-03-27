import React, { useState } from "react";
import axios from "axios";

function Prompt() {
    const [questPrompt, setQuestPrompt] = useState("");
    const [response, setResponse] = useState("");
    const [ret, setRet] = useState(false);
    
    const handleSubmit = async () => {
        try {
            // return quest promp to server
            const response = await axios.post("http://localhost:5000/prompt", {
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
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: "80vh" }}>
            <h1>Prompt</h1>
            <p>Write a quest prompt here</p>
            <textarea
                style={{ width: "50%", height: "100px", marginBottom: "20px" }}
                value={questPrompt}
                onChange={(e) => setQuestPrompt(e.target.value)}
                placeholder="Enter your quest prompt here..."
            />
            {ret === false ? (
                <p style={{ color: 'Red' }}>{response}</p>
            ) : (
                <p style={{ color: 'Green' }}>{response}</p>
            )}
            <button onClick={handleSubmit}>Submit</button>
        </div>
    );
}

export default Prompt;
