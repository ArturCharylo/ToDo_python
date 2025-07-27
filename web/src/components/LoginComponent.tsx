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

    function getCookie(name: string) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }

    try {
      // 1. Pobranie CSRF tokena
      await axios.get("http://localhost:8000/csrf/", {
        withCredentials: true,
      });

      // 2. Logowanie z tokenem Google
      const res = await axios.post(
        "http://localhost:8000/accounts/google/login/",
        { access_token: token },
        {
          withCredentials: true,
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
          },
        }
      );

      // 3. Zapisz token sesji (jeśli używasz tokenów)
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
