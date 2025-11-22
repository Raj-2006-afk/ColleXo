import { Link } from "react-router-dom";
import useAuth from "../hooks/useAuth";

const Navbar = () => {
	const { user, logout, isAuthenticated } = useAuth();

	return (
		<nav className="bg-white shadow-sm border-b border-gray-200">
			<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
				<div className="flex justify-between h-16">
					<div className="flex items-center">
						<Link to="/" className="flex items-center space-x-2">
							<div className="w-10 h-10 bg-gradient-to-br from-primary-600 to-primary-700 rounded-lg flex items-center justify-center">
								<span className="text-white font-bold text-xl">C</span>
							</div>
							<span className="text-2xl font-bold text-gray-900">ColleXo</span>
						</Link>
					</div>

					<div className="flex items-center space-x-4">
						{!isAuthenticated ? (
							<>
								<Link
									to="/login"
									className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
								>
									Login
								</Link>
								<Link to="/register" className="btn-primary text-sm">
									Get Started
								</Link>
							</>
						) : (
							<>
								<span className="text-sm text-gray-600">
									Welcome,{" "}
									<span className="font-medium text-gray-900">
										{user?.user_name}
									</span>
								</span>
								<span className="px-2 py-1 text-xs font-medium rounded-full bg-primary-100 text-primary-700">
									{user?.user_role}
								</span>
								<button
									onClick={logout}
									className="text-gray-700 hover:text-red-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
								>
									Logout
								</button>
							</>
						)}
					</div>
				</div>
			</div>
		</nav>
	);
};

export default Navbar;
