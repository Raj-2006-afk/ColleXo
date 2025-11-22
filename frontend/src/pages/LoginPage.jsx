import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import PublicLayout from "../components/Layout/PublicLayout";
import useAuth from "../hooks/useAuth";

const LoginPage = () => {
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const [error, setError] = useState("");
	const [loading, setLoading] = useState(false);

	const { login } = useAuth();
	const navigate = useNavigate();

	const handleSubmit = async (e) => {
		e.preventDefault();
		setError("");
		setLoading(true);

		const result = await login(email, password);

		if (result.success) {
			switch (result.user.user_role) {
				case "admin":
					navigate("/admin/dashboard");
					break;
				case "societyHead":
					navigate("/society-head/dashboard");
					break;
				case "student":
					navigate("/student/dashboard");
					break;
				default:
					navigate("/");
			}
		} else {
			setError(result.error);
			setLoading(false);
		}
	};

	return (
		<PublicLayout>
			<div className="min-h-[calc(100vh-64px)] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
				<div className="max-w-md w-full">
					<div className="card">
						<div className="text-center mb-8">
							<h2 className="text-3xl font-bold text-gray-900 mb-2">
								Welcome Back
							</h2>
							<p className="text-gray-600">Sign in to your ColleXo account</p>
						</div>

						{error && (
							<div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
								{error}
							</div>
						)}

						<form onSubmit={handleSubmit} className="space-y-4">
							<div>
								<label className="block text-sm font-medium text-gray-700 mb-2">
									Email Address
								</label>
								<input
									type="email"
									value={email}
									onChange={(e) => setEmail(e.target.value)}
									className="input-field"
									placeholder="you@example.com"
									required
								/>
							</div>

							<div>
								<label className="block text-sm font-medium text-gray-700 mb-2">
									Password
								</label>
								<input
									type="password"
									value={password}
									onChange={(e) => setPassword(e.target.value)}
									className="input-field"
									placeholder="••••••••"
									required
								/>
							</div>

							<button
								type="submit"
								disabled={loading}
								className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
							>
								{loading ? "Signing in..." : "Sign In"}
							</button>
						</form>

						<div className="mt-6 text-center">
							<p className="text-sm text-gray-600">
								Don't have an account?{" "}
								<Link
									to="/register"
									className="text-primary-600 hover:text-primary-700 font-medium"
								>
									Register here
								</Link>
							</p>
						</div>

						<div className="mt-6 pt-6 border-t border-gray-200">
							<p className="text-xs text-gray-500 text-center mb-2">
								Demo Credentials:
							</p>
							<div className="text-xs text-gray-600 space-y-1">
								<p>
									<strong>Student:</strong> student@collexo.com / student123
								</p>
								<p>
									<strong>Society Head:</strong> john@collexo.com / head123
								</p>
								<p>
									<strong>Admin:</strong> admin@collexo.com / admin123
								</p>
							</div>
						</div>
					</div>
				</div>
			</div>
		</PublicLayout>
	);
};

export default LoginPage;
