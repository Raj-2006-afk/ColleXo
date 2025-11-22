const StatusPill = ({ status }) => {
	const getStatusStyles = () => {
		switch (status) {
			case "pending":
				return "bg-yellow-100 text-yellow-700";
			case "shortlisted":
				return "bg-blue-100 text-blue-700";
			case "accepted":
				return "bg-green-100 text-green-700";
			case "rejected":
				return "bg-red-100 text-red-700";
			case "published":
				return "bg-green-100 text-green-700";
			case "draft":
				return "bg-gray-100 text-gray-700";
			default:
				return "bg-gray-100 text-gray-700";
		}
	};

	return (
		<span
			className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusStyles()}`}
		>
			{status.charAt(0).toUpperCase() + status.slice(1)}
		</span>
	);
};

export default StatusPill;
