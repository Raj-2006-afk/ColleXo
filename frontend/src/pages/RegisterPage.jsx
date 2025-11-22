import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import PublicLayout from "../components/Layout/PublicLayout";
import useAuth from "../hooks/useAuth";

const RegisterPage = () => {
	const [name, setName] = useState("");
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const [confirmPassword, setConfirmPassword] = useState("");
	const [role, setRole] = useState("student");
	const [societyName, setSocietyName] = useState("");
	const [error, setError] = useState("");
	const [loading, setLoading] = useState(false);

	const { register } = useAuth();
	const navigate = useNavigate();

	const handleSubmit = async (e) => {
		e.preventDefault();
		setError("");

		if (password !== confirmPassword) {
			setError("Passwords do not match");
			return;
		}

		if (password.length < 6) {
			setError("Password must be at least 6 characters");
			return;
		}

		if (role === "societyHead" && !societyName.trim()) {
			setError("Society name is required for Society Head registration");
			return;
		}

		setLoading(true);

		const result = await register(name, email, password, role);

		if (result.success) {
			if (role === "student") {
				navigate("/student/dashboard");
			} else if (role === "societyHead") {
				navigate("/society-head/dashboard");
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
							Create Account
						</h2>
						<p className="text-gray-600">Join ColleXo today</p>
					</div>

					{error && (
						<div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
							{error}
						</div>
					)}

					<form onSubmit={handleSubmit} className="space-y-4">
						<div>
							<label className="block text-sm font-medium text-gray-700 mb-2">
								Register As
							</label>
							<select
								value={role}
								onChange={(e) => setRole(e.target.value)}
								className="input-field"
								required
							>
								<option value="student">Student</option>
								<option value="societyHead">Society Head / Team Lead</option>
							</select>
						</div>

						<div>
							<label className="block text-sm font-medium text-gray-700 mb-2">
								Full Name
							</label>
							<input
								type="text"
								value={name}
								onChange={(e) => setName(e.target.value)}
								className="input-field"
								placeholder="John Doe"
								required
							/>
						</div>

						{role === "societyHead" && (
							<div>
								<label className="block text-sm font-medium text-gray-700 mb-2">
									Society Name
								</label>
								<input
									type="text"
									value={societyName}
									onChange={(e) => setSocietyName(e.target.value)}
									className="input-field"
									placeholder="Tech Club"
									required
								/>
								<p className="mt-1 text-xs text-gray-500">
									You will be registered as the head of this society
								</p>
							</div>
						)}							<div>
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

							<div>
								<label className="block text-sm font-medium text-gray-700 mb-2">
									Confirm Password
								</label>
								<input
									type="password"
									value={confirmPassword}
									onChange={(e) => setConfirmPassword(e.target.value)}
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
								{loading ? "Creating account..." : "Create Account"}
							</button>
						</form>

						<div className="mt-6 text-center">
							<p className="text-sm text-gray-600">
								Already have an account?{" "}
								<Link
									to="/login"
									className="text-primary-600 hover:text-primary-700 font-medium"
								>
									Sign in here
								</Link>
							</p>
						</div>
					</div>
				</div>
			</div>
		</PublicLayout>
	);
};

export default RegisterPage;
