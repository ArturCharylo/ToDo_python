import { GoogleOAuthProvider } from '@react-oauth/google';
import Login from '../components/LoginComponent';

const App = () => {
  const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;

  return (
    <GoogleOAuthProvider clientId={clientId}>
      <Login />
    </GoogleOAuthProvider>
  );
};

export default App;