import { GoogleLogin } from '@react-oauth/google';
import { useNavigate } from 'react-router-dom';

const LoginComponent = () => {

  const navigate = useNavigate()
  return (
    <div>
      <h2>Zaloguj się przez Google</h2>
      <GoogleLogin
        onSuccess={() => {
          navigate("/")
        }}
        onError={() => console.log("Błąd logowania Google")}
      />
    </div>
  );
};

export default LoginComponent;
