import React, { useState, useEffect } from 'react';
import styles from './QuestViewer.module.css';


export default function QuestViewer({ filename = 'last-quest.json' }) {
  const [quest, setQuest] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchQuest = () =>
      fetch(`/quests/${filename}`)
        .then(res => {
          if (!res.ok) throw new Error(`HTTP ${res.status}`);
          return res.json();
        })
        .then(setQuest)
        .catch(setError);

    fetchQuest();
    const timer = setInterval(fetchQuest, 60000);
    return () => clearInterval(timer);
  }, [filename]);

  if (error) {
    return <div className={styles.error}>Error loading quest: {error.message}</div>;
  }
  if (!quest) {
    return <div className={styles.loading}>Loading quest…</div>;
  }

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>{quest.title}</h2>
      <ol className={styles.steps}>
        {quest.steps.map((step, idx) => (
          <li key={idx} className={styles.stepItem}>{step}</li>
        ))}
      </ol>
    </div>
  );
}
