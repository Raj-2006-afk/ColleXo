import { Link, useLocation } from "react-router-dom";

const Sidebar = ({ role }) => {
	const location = useLocation();

	const getNavItems = () => {
		switch (role) {
			case "student":
				return [
					{ path: "/student/dashboard", label: "Dashboard", icon: "🏠" },
					{ path: "/student/societies", label: "Societies", icon: "🎯" },
					{
						path: "/student/applications",
						label: "My Applications",
						icon: "📝",
					},
				];
			case "societyHead":
				return [
					{ path: "/society-head/dashboard", label: "Overview", icon: "📊" },
					{ path: "/society-head/society", label: "My Society", icon: "🏢" },
					{ path: "/society-head/forms", label: "Forms", icon: "📋" },
					{
						path: "/society-head/applications",
						label: "Applications",
						icon: "📬",
					},
				];
			case "admin":
				return [
					{ path: "/admin/dashboard", label: "Dashboard", icon: "📊" },
					{ path: "/admin/societies", label: "Societies", icon: "🏢" },
					{ path: "/admin/users", label: "Users", icon: "👥" },
				];
			default:
				return [];
		}
	};

	const navItems = getNavItems();

	return (
		<aside className="w-64 bg-white border-r border-gray-200 min-h-screen">
			<div className="p-6">
				<h2 className="text-lg font-semibold text-gray-800 mb-4">Navigation</h2>
				<nav className="space-y-2">
					{navItems.map((item) => {
						const isActive = location.pathname === item.path;
						return (
							<Link
								key={item.path}
								to={item.path}
								className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
									isActive
										? "bg-primary-50 text-primary-700 font-medium"
										: "text-gray-700 hover:bg-gray-50"
								}`}
							>
								<span className="text-xl">{item.icon}</span>
								<span>{item.label}</span>
							</Link>
						);
					})}
				</nav>
			</div>
		</aside>
	);
};

export default Sidebar;
