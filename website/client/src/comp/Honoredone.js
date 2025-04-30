import React from "react";
import SubNavBar from "./SubNavBar";
import { useState } from 'react';
import axios from 'axios';
import honoredBackground from "../assets/img/MoH-US-Army-shopped_2.jpg"
import "./Generatequest.css"

/* ai-gen start (ChatGPT-4, 2) */
function HonoredOne() {

    const [name, setName] = React.useState("");
    const [file, setFile] = React.useState(null);
    const [text, setText] = React.useState('');
    const [Ret, setRet] = useState(true);
    const [message, setMessage] = React.useState("");

    const handleSubmit = async () => {
        if (!name) {
            console.error("Please input a name.");
        }

        if (file) {
            const reader = new FileReader();
            reader.onload = async (e) => {
                const fileContent = e.target.result;
                setText(fileContent);

                try {
                    const response = await axios.post("http://localhost:5000/honored_one", {
                        message_name: name,
                        message_logs: fileContent,
                    });
                    console.log("Response from server:", response.data)
                    setMessage("Sucessfully receieved");
                    setRet(true);;
                } catch (error) {
                    console.error("Error sending prompt:", error);
                    setMessage("Unsuccessful, please try again");
                    setRet(false);
                }
            };
            reader.readAsText(file);
        } else {
            setText('Please select a valid .txt file.');
            console.error("Please select a valid .txt file.");
        }
    };

    const backgroundStyle1 = {
        position: "absolute",
        backgroundImage: `url(${honoredBackground})`,
        backgroundSize: "contain",
        backgroundPosition: "center",
        height: "60vh",
        width: "60vw", 
        top: "20vh",
        right: "47vw",
    };

    const backgroundStyle2 = {
        position: "absolute",
        backgroundImage: `url(${honoredBackground})`,
        backgroundSize: "contain",
        backgroundPosition: "center",
        height: "60vh",
        width: "60vw", 
        top: "20vh",
        left: "49.5vw",
    };


    return (
        <div>
            <div style={backgroundStyle1}>
            </div>
            <div style={backgroundStyle2}>
            </div>
                <SubNavBar />
                <div style={{ position: "relative", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: "50vh", textAlign: "center", zIndex: 10, top: "25vh" }}>
                    <h1 style={{ fontSize: "3.5rem", fontFamily: "Georgia, serif" }}>Honored One</h1>
                    <div style = {{marginTop: "30px"}}></div>
                        <p style={{ fontSize: "1.7rem", fontFamily: "Helvetica, Arial, sans-serif" }}>PLEASE ENTER YOU HONORED ONE'S NAME BELOW:</p> 
                    <div style = {{marginTop: "25px"}}></div>
                    <input
                    
                        type="text"
                        placeholder="Name of Honored One"
                        value={name || ""}
                        onChange={(e) => setName(e.target.value)}
                        style={{ width: "500px", padding: "10px", fontSize: "24px", marginBottom: "20px" }}
                    />
                    <div style={{ marginTop: "20px", }}>
                        <input
                        style={{ display: "block", marginLeft: "7vw", padding: "15px", fontSize: "28px", marginBottom: "20px" }}
                            type="file"
                            accept=".txt"
                            onChange={(e) => {
                                if (e.target.files.length > 0) {
                                    console.log("File selected:", e.target.files[0].name);
                                    setFile(e.target.files[0]);
                                }
                            }}
                        />
                    </div>
                            {Ret === false ? (
                            <p style={{ color: 'red' }}>{message}</p>
                        ) : (
                            message && <p style={{ color: 'limegreen' }}>{message}</p>
                        )}
                        <div style={{ marginTop: "20px"}}>
                            <button 
                                className= "quest-button"
                                onClick={handleSubmit} 
                            >
                                Submit
                            </button>
                        </div>
                </div>
            
        </div>
    );
}

export default HonoredOne;
/*  ai-gen end */
