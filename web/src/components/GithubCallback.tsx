import { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export default function GithubCallback() {
  const navigate = useNavigate();
  const hasFetched = useRef(false);

  useEffect(() => {
    if (hasFetched.current) return;
    hasFetched.current = true;

    const fetchToken = async () => {
      const params = new URLSearchParams(window.location.search);
      const code = params.get("code");

      if (!code) {
        console.error("Brak code w URL – prawdopodobnie wejście bez logowania");
        navigate("/");
        return;
      }

      try {
        const res = await axios.post("http://localhost:8000/api/github/login/", { code });

        // Backend zwraca access i refresh → zapisujemy je
        localStorage.setItem("token", res.data.access);
        localStorage.setItem("refresh", res.data.refresh);
        localStorage.setItem("user", JSON.stringify(res.data.user));

        navigate("/home");
      } catch (err) {
        console.error("Błąd logowania przez GitHub:", err);
        navigate("/");
      }
    };

    fetchToken();
  }, [navigate]);

  return <p>Logowanie przez GitHub...</p>;
}
