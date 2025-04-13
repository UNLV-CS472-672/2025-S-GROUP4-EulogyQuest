import React from "react";
import { useNavigate } from "react-router-dom";
import famousBG from "../assets/img/Famous_person.jpg";
import honoredBG from "../assets/img/Honored_one.jpg";
import "./Generatequest.css";

/* ai-gen start (ChatGPT-4, 2) */
function Generatequest() {
  const navigate = useNavigate();

  return (
    <div className="split-container">
      {/* Famous Person Section */}
      <div
        className="split-section left-section"
        style={{ backgroundImage: `url(${famousBG})` }}
      >
        <div className="section-title-container">
          <h2 className="section-title">Famous Person Quest</h2>
        </div>
        <p className="section-description">
          Generate a quest inspired by a public figure, celebrity, or historical icon.
          Simply enter a name and let the magic unfold.
        </p>
        <button
          className="quest-button"
          onClick={() => navigate("/famous-person")}
        >
          Start Famous Quest
        </button>
      </div>

      {/* Honored One Section */}
      <div
        className="split-section right-section"
        style={{ backgroundImage: `url(${honoredBG})` }}
      >
        <div className="section-title-container">
        <h2 className="section-title">Honored One Quest</h2>
        </div>
        <p className="section-description">
          Create a heartfelt or imaginative quest based on a loved one, friend, or someone meaningful to you.
        </p>
        <button
          className="quest-button"
          onClick={() => navigate("/honored-one")}
        >
          Start Honored Quest
        </button>
      </div>
    </div>
  );
}
/* ai-gen end (ChatGPT-4, 2) */

export default Generatequest;
