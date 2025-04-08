import React from "react";
import SubNavBar from "./SubNavBar";

/* ai-gen start (ChatGPT-4, 2) */
function HonoredOne() {

    const [name, setName] = React.useState("");
    const [file, setFile] = React.useState(null);

    const handleSubmit = () => {
        console.log("Submitted name:", name);
        console.log("Submitted file:", file.name);
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