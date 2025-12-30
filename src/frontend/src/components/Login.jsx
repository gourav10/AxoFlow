import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axoflowLogo from '../assets/axoflow_logo.png';
import { authAPI } from '../services/api';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Call the backend API
      const response = await authAPI.login(email, password);

      // Navigate to home on successful login
      navigate('/home');
    } catch (err) {
      // Display error message
      setError(err.message || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-blue-500 flex items-center justify-center p-8">
      <div className="bg-white rounded-3xl shadow-2xl flex w-full max-w-6xl overflow-hidden" style={{ minHeight: '600px' }}>
        {/* Left Side - Branding */}
        <div className="w-1/2 bg-gradient-to-br from-blue-400 to-blue-600 p-12 flex flex-col justify-between text-white relative">
          <div>
            <h1 className="text-4xl font-light leading-relaxed mb-4">
              Tired of manual<br />
              job applications?<br />
              <span className="font-bold text-blue-200">AxoFlow</span><br />
              automates it for you.
            </h1>
          </div>

          <div className="flex flex-col items-center justify-center flex-grow">
            <div className="w-64 h-64 bg-white rounded-3xl shadow-2xl flex items-center justify-center transform hover:scale-105 transition-transform duration-300 overflow-hidden">
              <img src={axoflowLogo} alt="AxoFlow Logo" className="w-full h-full object-cover" />
            </div>
          </div>
        </div>

        {/* Right Side - Sign-in Form */}
        <div className="w-1/2 bg-gray-50 p-12 flex flex-col justify-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-12">
            Sign-in
          </h2>

          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
                <span className="block sm:inline">{error}</span>
              </div>
            )}

            <div>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-0 py-3 border-0 border-b-2 border-gray-300 bg-transparent focus:border-blue-500 focus:ring-0 outline-none transition text-gray-700 placeholder-gray-400"
                placeholder="Email"
                required
                disabled={loading}
              />
            </div>

            <div>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-0 py-3 border-0 border-b-2 border-gray-300 bg-transparent focus:border-blue-500 focus:ring-0 outline-none transition text-gray-700 placeholder-gray-400"
                placeholder="Password"
                required
                disabled={loading}
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-4 rounded-lg font-semibold hover:bg-blue-700 transition duration-200 shadow-md hover:shadow-lg mt-8 disabled:bg-blue-400 disabled:cursor-not-allowed"
            >
              {loading ? 'Logging in...' : 'Login'}
            </button>
          </form>

          <div className="mt-8 text-center">
            <p className="text-gray-600">
              Don't have an account?{' '}
              <Link to="/signup" className="text-blue-600 hover:text-blue-700 font-semibold">
                Signup Here
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
