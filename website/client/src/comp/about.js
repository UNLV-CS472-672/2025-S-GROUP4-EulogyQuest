import React from "react";

// Write about the project here including all contributors

// This is the project description.
const projectDescription = "We've always honored our fallen. Our loved ones were given proper burial and proper eulogy. Yet, many of our friends are online today. And as we get older, some will no longer be with us.";
function About() {
    return (
        <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'flex-end', height: '20vh' }}>
            <h1>About</h1>
            <p>
                {projectDescription}
            </p>
        </div>
    );
}

export default About;