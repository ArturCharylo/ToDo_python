import { GoogleOAuthProvider } from '@react-oauth/google';
import Login from '../components/LoginComponent';

const App = () => {
  return (
    <GoogleOAuthProvider clientId="453582868828-5coj2343a3k59i3rqc6frqk2a93oh86g.apps.googleusercontent.com">
      <Login />
    </GoogleOAuthProvider>
  );
};

export default App;
