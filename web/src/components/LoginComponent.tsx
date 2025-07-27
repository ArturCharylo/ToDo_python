// src/components/Login.tsx
import { GoogleLogin } from '@react-oauth/google';
import type { CredentialResponse } from '@react-oauth/google';
import { jwtDecode } from 'jwt-decode';
import axios from 'axios';

const LoginComponent = () => {
  const handleLogin = async (credentialResponse: CredentialResponse) => {
    const token = credentialResponse.credential;
    if (!token) return;

    interface GoogleJwtPayload {
      email?: string;
      name?: string;
      picture?: string;
      sub?: string;
    }

    const decoded = jwtDecode<GoogleJwtPayload>(token);
    console.log("Zalogowany użytkownik Google:", decoded);

    try {
      const res = await axios.post("http://localhost:8000/dj-rest-auth/google/", {
        access_token: token,
      });

      const sessionToken = res.data.key;
      sessionStorage.setItem("authToken", sessionToken);
      alert("Zalogowano!");
    } catch (error) {
      console.error("Błąd podczas logowania przez Google:", error);
    }
  };

  return (
    <div>
      <h2>Zaloguj się przez Google</h2>
      <GoogleLogin
        onSuccess={handleLogin}
        onError={() => console.log("Błąd logowania Google")}
      />
    </div>
  );
};

export default LoginComponent;
