import React from "react";
import SubNavBar from "./SubNavBar";
import axios from 'axios';

/* ai-gen start (ChatGPT-4, 2) */
function HonoredOne() {

    const [name, setName] = React.useState("");
    const [file, setFile] = React.useState(null);
    const [text, setText] = React.useState('');
    const [message_name, setMessage_name] = React.useState("");
    const [message_logs, setMessage_logs] = React.useState('');

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
                    console.log("Response from server:", response.data);
                } catch (error) {
                    console.error("Error sending prompt:", error);
                }
            };
            reader.readAsText(file);
        } else {
            setText('Please select a valid .txt file.');
            console.error("Please select a valid .txt file.");
        }
    };


    return (
        <div>
            <SubNavBar />
            <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: "50vh", textAlign: "center" }}>
                <h1>Honored One</h1>
                <p>Please enter your Honored One's name below:</p>
                <input
                    type="text"
                    placeholder="Enter the name of the Honored One here"
                    value={name || ""}
                    onChange={(e) => setName(e.target.value)}
                    style={{ width: "300px", padding: "10px", fontSize: "16px", marginBottom: "20px" }}
                />
                <div style={{ marginTop: "20px" }}>
                    <input
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
                    <div style={{ marginTop: "20px" }}>
                        <button onClick={handleSubmit}>Submit</button>
                    </div>
            </div>
        </div>
    );
}

export default HonoredOne;
/*  ai-gen end */
