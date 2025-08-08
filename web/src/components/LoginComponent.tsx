import { GoogleLogin, type CredentialResponse } from '@react-oauth/google';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

const LoginComponent = () => {

  const navigate = useNavigate()

  const handleLogin = async (credencialResponse: CredentialResponse) => {
    try {
      interface DecodedToken {
        email?: string;
        name?: string;
        [key: string]: unknown;
      }
      const decoded: DecodedToken = jwtDecode(credencialResponse.credential || "");
      // decoded will have fields like email, name, etc.
      await axios.post('http://localhost:8000/api/add_user/', {
        email: decoded.email,
        username: decoded.name, // or decoded.email if you want email as username
        credentials: credencialResponse.credential
      });
      localStorage.setItem('token', credencialResponse.credential || '');
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        console.error("Błąd podczas logowania:", error.response.data);
      } else {
        console.error("Błąd podczas logowania:", error);
      }
    }
    navigate("/home");
  };

  const handleGitHubLogin = async () => {
    const clientId = "OV23liMbdbPZIZnCbi9G";
    const redirectUri = "http://localhost:5173/github-callback";
    const scope = "read:user user:email";
    window.location.href = `https://github.com/login/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scope}`;
  };
  return (
    <div>
      <h2>Zaloguj się przez Google</h2>
      <GoogleLogin
        onSuccess={(credencialResponse) => {
          handleLogin(credencialResponse);
        }}
        onError={() => console.log("Błąd logowania Google")}
      />
      <button onClick={handleGitHubLogin}>
        Zaloguj się przez GitHub
      </button>
    </div>
  );
};

export default LoginComponent;
