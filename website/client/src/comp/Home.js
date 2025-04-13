import React from "react";
import backgroundImage from "../assets/img/background_homepage.webp";

const backgroundStyle = {
    backgroundImage: `url(${backgroundImage})`,
    backgroundSize: "cover",
    backgroundPosition: "center",
    height: "100vh",
    width: "100vw",
};
function Home() {
    return (
        <div style={backgroundStyle}>
        <img src={backgroundImage} alt="Background" style={{ display: "none" }} />
        
        {/* ai-gen start (ChatGPT-4, 2) */}
        {/* Left clear section */}
        <div style={{
          position: "absolute",
          top: 0,
          left: 0,
          height: "100vh",
          width: "25vw",
          backgroundColor: "rgba(0, 0, 0, 0)",
          zIndex: 1
        }}></div>
      
        {/* Center dimmed section */}
        <div style={{
          position: "absolute",
          top: 0,
          left: "25vw",
          height: "100vh",
          width: "50vw",
          backgroundColor: "rgba(0, 0, 0, 0.66)",
          zIndex: 1
        }}></div>
      
        {/* Right clear section */}
        <div style={{
          position: "absolute",
          top: 0,
          left: "75vw",
          height: "100vh",
          width: "25vw",
          backgroundColor: "rgba(0, 0, 0, 0)",
          zIndex: 1
        }}></div>
      
        {/* Text */}
        <div style={{
          position: "absolute",
          top: "30%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          color: "white",
          zIndex: 2,
          maxWidth: "50vw",
          padding: "1rem",
          textAlign: "center"
        }}>
        {/* ai-gen end (ChatGPT-4, 2) */}

                <h1 style={{ fontSize: "3rem", textAlign: "center" }}>Welcome to Eulogy Quest</h1>
                <p>
                    This website is inspired by the popular MMORPG EverQuest. With this website, you can generate
                    quests using the name of a famous or respected individual, or by providing a custom prompt of your own.
                </p>
                <p>
                    By leveraging the power of OpenAI's ChatGPT API, we dynamically generate quests based on user input.
                    The AI can analyze a well-known person and gather information to create a detailed, accurate quest.
                    Alternatively, you can craft a quest based on someone you know personally or even a fictional character
                    of your own creation—the only limit is your imagination. The AI uses the provided details to generate quests
                    that are both imaginative and contextually relevant, ensuring each one feels personalized and unique.
                </p>
                <p>
                    This application is built using modern web technologies, including Flask, React, OpenAI's API, and more.
                    These tools work together to provide a smooth, engaging experience with highly personalized features.
                </p>
            </div>

        </div>
    );
}

export default Home;

