import React from 'react';
import { useState } from 'react';
import axios from 'axios';
import SubNavBar from './SubNavBar';


function FamousPerson() {
    const [Input, SetInput] = useState(null);
    const [Ret, setRet] = useState(true);
    const [message, setMessage] = useState("");
    const [/*response*/, setResponse] = useState(null);

    /* ai-gen start (ChatGPT-4, 2) */
    const handleSubmit = async () => {


        try {
            const response = await axios.post("http://localhost:5000/famous-person", {
                message: Input,
            });
            setMessage("Sucessfully receieved");
            setRet(true);
            console.log("Server response:", response.data);
            setResponse(response.data);

        } catch (error) {
            console.error("Error sending prompt:", error);
            setMessage("Unsuccessful, please try again");
            setRet(false);
        }
    }
    
    return (
        
        <div >
            <SubNavBar />
            <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
            <h1>Famous Person</h1>
            <p>Enter a famous person to generate a quest. This will be generated using ChatGPT</p>
            <input
                type="text"
                placeholder="Enter a famous person"
                value={Input}
                onChange={(e) => SetInput(e.target.value)}
            />
            <div style={{ marginBottom: "10px" }}></div>
            {Ret === false ? (
                      <p style={{ color: 'red' }}>{message}</p>
                    ) : (
                      <p style={{ color: 'limegreen' }}>{message}</p>
                    )}
            {/* response mechanism to user check input */}
            {/* {response && (
                    <>
                        <p><strong>Name:</strong> {response.famous_person}</p>
                    </>
                )} */}
            <button onClick={handleSubmit}>Submit</button>
            </div>
        </div>
    );
}

export default FamousPerson;