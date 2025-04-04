import React from 'react';
import { useState } from 'react';
import axios from 'axios';
import SubNavBar from './SubNavBar';


function FamousPerson() {
    const [famousPerson, setFamousPerson] = useState(null);

    /* ai-gen start (ChatGPT-4, 2) */
    const handleSubmit = async () => {
        try {
            const response = await axios.post("http://localhost:5000/famous-person", {
                message: famousPerson,
            });
            console.log("Server response:", response.data);
            setFamousPerson(response.data); // Update the state with the response data
        } catch (error) {
            console.error("Error sending prompt:", error);
        }
    }
    
    return (
        
        <div >
            <SubNavBar />
            <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
            <h1>Famous Person</h1>
            <p>Enter a famous person to generate a quest. This will be generated using ChatGPT</p>
            <p>{famousPerson}</p> {/* displays name, shows if character (incase we dont wanna add multiple different 
            questlines for the same character*/}
            <input
                type="text"
                placeholder="Enter a famous person"
                value={famousPerson || ""}
                onChange={(e) => setFamousPerson(e.target.value)}
            />
            <div style={{ marginBottom: "10px" }}></div>
            <button onClick={handleSubmit}>Submit</button>
            </div>
        </div>
    );
}

export default FamousPerson;