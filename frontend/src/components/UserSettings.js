import React, { useState, useEffect } from 'react';
import { getUserSettings, updateUserSettings } from '../services/api';

const UserSettings = () => {
  const [settings, setSettings] = useState({
    email_notifications: true,
    learning_style: 'visual',
    difficulty_preference: 'balanced'
  });

  useEffect(() => {
    const fetchSettings = async () => {
      const userSettings = await getUserSettings();
      setSettings(userSettings);
    };
    fetchSettings();
  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setSettings(prevSettings => ({
      ...prevSettings,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await updateUserSettings(settings);
      alert('Settings updated successfully!');
    } catch (error) {
      console.error('Error updating settings:', error);
      alert('Failed to update settings. Please try again.');
    }
  };

  return (
    <div className="max-w-2xl mx-auto mt-8">
      <h1 className="text-3xl font-bold mb-6">User Settings</h1>
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="flex items-center">
            <input
              type="checkbox"
              name="email_notifications"
              checked={settings.email_notifications}
              onChange={handleChange}
              className="mr-2"
            />
            Receive email notifications
          </label>
        </div>
        <div>
          <label className="block mb-2">Learning Style Preference:</label>
          <select
            name="learning_style"
            value={settings.learning_style}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          >
            <option value="visual">Visual</option>
            <option value="auditory">Auditory</option>
            <option value="reading">Reading/Writing</option>
            <option value="kinesthetic">Kinesthetic</option>
          </select>
        </div>
        <div>
          <label className="block mb-2">Difficulty Preference:</label>
          <select
            name="difficulty_preference"
            value={settings.difficulty_preference}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          >
            <option value="easy">Easy</option>
            <option value="balanced">Balanced</option>
            <option value="challenging">Challenging</option>
          </select>
        </div>
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
          Save Settings
        </button>
      </form>
    </div>
  );
};

export default UserSettings;