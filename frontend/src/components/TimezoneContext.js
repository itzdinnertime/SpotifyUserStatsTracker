import React, { createContext, useState, useEffect } from 'react';

export const TimezoneContext = createContext();

export function TimezoneProvider({ children }) {
  const [timezone, setTimezone] = useState(localStorage.getItem('timezone') || 'UTC');

  useEffect(() => {
    localStorage.setItem('timezone', timezone);
  }, [timezone]);

  return (
    <TimezoneContext.Provider value={{ timezone, setTimezone }}>
      {children}
    </TimezoneContext.Provider>
  );
}