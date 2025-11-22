const StatCard = ({ title, value, icon, color = "primary" }) => {
	const colorClasses = {
		primary: "from-primary-500 to-primary-600",
		secondary: "from-secondary-500 to-secondary-600",
		blue: "from-blue-500 to-blue-600",
		green: "from-green-500 to-green-600",
		yellow: "from-yellow-500 to-yellow-600",
		red: "from-red-500 to-red-600",
	};

	return (
		<div className="card">
			<div className="flex items-center justify-between">
				<div>
					<p className="text-sm font-medium text-gray-600 mb-1">{title}</p>
					<p className="text-3xl font-bold text-gray-900">{value}</p>
				</div>
				<div
					className={`w-12 h-12 bg-gradient-to-br ${colorClasses[color]} rounded-lg flex items-center justify-center`}
				>
					<span className="text-white text-2xl">{icon}</span>
				</div>
			</div>
		</div>
	);
};

export default StatCard;
