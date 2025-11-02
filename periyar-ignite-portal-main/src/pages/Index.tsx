import { useState } from 'react';
import { LoginPage } from '@/components/LoginPage';
import { Dashboard } from '@/components/Dashboard';

const Index = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [lscNumber, setLscNumber] = useState('');

  const handleLogin = (lsc: string) => {
    setLscNumber(lsc);
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setLscNumber('');
  };

  if (isLoggedIn) {
    return <Dashboard lscNumber={lscNumber} onLogout={handleLogout} />;
  }

  return <LoginPage onLogin={handleLogin} />;
};

export default Index;
