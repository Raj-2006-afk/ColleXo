import { Link } from "react-router-dom";
import PublicLayout from "../components/Layout/PublicLayout";
import useAuth from "../hooks/useAuth";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const LandingPage = () => {
	const { isAuthenticated, user } = useAuth();
	const navigate = useNavigate();

	useEffect(() => {
		if (isAuthenticated && user) {
			switch (user.user_role) {
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
					break;
			}
		}
	}, [isAuthenticated, user, navigate]);

	return (
		<PublicLayout>
			{/* Hero Section */}
			<section className="bg-gradient-to-br from-primary-600 to-primary-800 text-white">
				<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
					<div className="text-center">
						<h1 className="text-5xl font-bold mb-6">Welcome to ColleXo</h1>
						<p className="text-xl mb-8 text-primary-100 max-w-2xl mx-auto">
							The ultimate platform for managing college societies, streamlining
							recruitment, and connecting students with opportunities
						</p>
						<div className="flex justify-center space-x-4">
							<Link
								to="/register"
								className="bg-white text-primary-600 hover:bg-gray-100 px-8 py-3 rounded-lg font-semibold text-lg transition-colors"
							>
								Get Started
							</Link>
							<Link
								to="/login"
								className="border-2 border-white text-white hover:bg-white hover:text-primary-600 px-8 py-3 rounded-lg font-semibold text-lg transition-colors"
							>
								Login
							</Link>
						</div>
					</div>
				</div>
			</section>

			{/* How It Works Section */}
			<section className="py-20 bg-white">
				<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
					<h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
						How It Works
					</h2>
					<div className="grid md:grid-cols-3 gap-8">
						<div className="text-center">
							<div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
								<span className="text-3xl">🔍</span>
							</div>
							<h3 className="text-xl font-semibold mb-2">Discover Societies</h3>
							<p className="text-gray-600">
								Browse through various college societies and find the ones that
								match your interests
							</p>
						</div>
						<div className="text-center">
							<div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
								<span className="text-3xl">📝</span>
							</div>
							<h3 className="text-xl font-semibold mb-2">Apply with Forms</h3>
							<p className="text-gray-600">
								Submit applications through easy-to-use forms and track your
								application status
							</p>
						</div>
						<div className="text-center">
							<div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
								<span className="text-3xl">🎯</span>
							</div>
							<h3 className="text-xl font-semibold mb-2">Manage Recruitment</h3>
							<p className="text-gray-600">
								Society heads can efficiently manage applications and recruit
								new members
							</p>
						</div>
					</div>
				</div>
			</section>

			{/* Features Section */}
			<section className="py-20 bg-gray-50">
				<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
					<h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
						For Everyone
					</h2>
					<div className="grid md:grid-cols-3 gap-8">
						<div className="card">
							<h3 className="text-xl font-semibold mb-3 text-primary-600">
								For Students
							</h3>
							<ul className="space-y-2 text-gray-600">
								<li>✓ Explore diverse societies</li>
								<li>✓ Submit applications easily</li>
								<li>✓ Track application status</li>
								<li>✓ Get notifications</li>
							</ul>
						</div>
						<div className="card">
							<h3 className="text-xl font-semibold mb-3 text-primary-600">
								For Society Heads
							</h3>
							<ul className="space-y-2 text-gray-600">
								<li>✓ Manage society profile</li>
								<li>✓ Create recruitment forms</li>
								<li>✓ Review applications</li>
								<li>✓ Shortlist candidates</li>
							</ul>
						</div>
						<div className="card">
							<h3 className="text-xl font-semibold mb-3 text-primary-600">
								For Admins
							</h3>
							<ul className="space-y-2 text-gray-600">
								<li>✓ Oversee all societies</li>
								<li>✓ Monitor activities</li>
								<li>✓ View analytics</li>
								<li>✓ Manage users</li>
							</ul>
						</div>
					</div>
				</div>
			</section>

			{/* CTA Section */}
			<section className="bg-primary-600 text-white py-16">
				<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
					<h2 className="text-3xl font-bold mb-4">Ready to Get Started?</h2>
					<p className="text-xl mb-8 text-primary-100">
						Join thousands of students and societies already using ColleXo
					</p>
					<Link
						to="/register"
						className="bg-white text-primary-600 hover:bg-gray-100 px-8 py-3 rounded-lg font-semibold text-lg transition-colors inline-block"
					>
						Create Free Account
					</Link>
				</div>
			</section>
		</PublicLayout>
	);
};

export default LandingPage;
